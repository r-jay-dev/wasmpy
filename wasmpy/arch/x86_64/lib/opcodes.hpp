#ifndef OPCODES_H
#define OPCODES_H

#include "nativelib.hpp"

bytes decodeOperation(bytes buf, size_t offset);
bytes ret_v32(uint64_t errorPageAddr);
bytes ret_v64(uint64_t errorPageAddr);
bytes ret_void(uint64_t errorPageAddr);

extern bytes drop_32;
extern bytes drop_64;

extern bytes local32;
extern bytes local64;
extern bytes param_32;
extern bytes param_64;
extern bytes initStack;
extern bytes param_32_linux_0;
extern bytes param_32_linux_1;
extern bytes param_32_linux_2_win_1;
extern bytes param_32_linux_3_win_0;
extern bytes param_32_linux_4_win_2;
extern bytes param_32_linux_5_win_3;
extern bytes param_64_linux_0;
extern bytes param_64_linux_1;
extern bytes param_64_linux_2_win_1;
extern bytes param_64_linux_3_win_0;
extern bytes param_64_linux_4_win_2;
extern bytes param_64_linux_5_win_3;

#endif
