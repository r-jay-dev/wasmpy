import json
import os
import re
import types


NONE = 0
ALL = 0
features = [
    "MUTABLE_GLOBALS",
    "SATURATING_FLOAT_TO_INT",
    "SIGN_EXTENSION",
    "MULTI_VALUE",
    "REFERENCE_TYPES",
    "BULK_MEMORY",
    "SIMD",
]

for i, f in enumerate(features):
    globals()[f] = 1 << i
    ALL |= 1 << i

__all__ = ["enable", "disable", "ALL", "NONE"] + features
enabled_features = NONE

opcodes = {}
consumes = {}
signatures = {}
with open(os.path.join(os.path.dirname(__file__), "opcodes.json")) as fp:
    data = json.load(fp)
    for group in data["opcodes"]:
        opcodes.update(
            dict(
                zip(
                    (i[0] for i in group["instructions"]),
                    (i + group["offset"] for i in range(len(group["instructions"]))),
                )
            )
        )

    for k, v in data["consumes"].items():
        consumes[opcodes[k]] = v

    for group in data["opcodes"]:
        signatures.update(
            dict(
                zip(
                    (opcodes[i[0]] for i in group["instructions"]),
                    (i[1:] for i in group["instructions"]),
                )
            )
        )


def create_module(module: dict) -> object:
    """Convert module outlined by dict into WebAssemblyModule object."""
    WebAssemblyModule = type("WebAssemblyModule", (types.ModuleType,), {})
    props = []
    for e in module["exports"]:
        if isinstance(e["obj"], list):

            def get(self, e=e):
                return e["obj"][1][0]

            prop = property(get)

            if e["obj"][0] == "mut":

                def set(self, val, e=e):
                    e["obj"][1][0] = val

                prop = prop.setter(set)

            setattr(WebAssemblyModule, e["name"], prop)

        else:
            setattr(WebAssemblyModule, e["name"], e["obj"])

        props.append(e["name"])

    if module["start"] is not None:
        setattr(WebAssemblyModule, "__call__", module["start"])
        obj = WebAssemblyModule("module")
        obj()

    else:
        obj = WebAssemblyModule("module")

    for prop in props:
        obj.__dict__.update({prop: getattr(obj, prop)})

    obj.__dict__.update({"_internal": module})

    return obj


def enable(flag: int) -> None:
    """Mark features as enabled."""
    global enabled_features
    if flag == NONE:
        enabled_features = 0

    else:
        enabled_features |= flag


def disable(flag: int) -> None:
    """Mark features as disabled."""
    global enabled_features
    enabled_features = ~(~enabled_features | flag)


def expand_bytes(n: int, bits: int = 32) -> list:
    """Convert integer to little endian byte representation."""
    r = []
    for _ in range(bits // 8):
        r.append(n & 255)
        n >>= 8

    return r


def sanitize(name: str) -> str:
    """Convert name to valid Python identifier."""
    name = name.strip()
    if name.isidentifier():
        return name

    name = re.sub(r"\W+", "_", name)
    if not name[0].isidentifier():
        name = "_" + name

    return name
