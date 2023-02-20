#ifndef DEFINES_H_
#define DEFINES_H_

#include "ap_int.h"
#include "ap_fixed.h"
#include "nnet_utils/nnet_types.h"
#include <cstddef>
#include <cstdio>

//hls-fpga-machine-learning insert numbers
#define N_INPUT_1_1 252
#define N_SIZE_1_2 18
#define N_SIZE_2_2 14
#define N_SIZE_3_2 1
#define OUT_HEIGHT_3 8
#define OUT_WIDTH_3 6
#define N_FILT_3 3
#define N_SIZE_1_6 144
#define N_LAYER_7 20
#define N_LAYER_10 1

//hls-fpga-machine-learning insert layer-precision
typedef ap_uint<10> input_t;
typedef ap_fixed<20,8> conv_accum_t;
typedef ap_fixed<15,8> layer3_t;
typedef ap_fixed<10,0> weight3_t;
typedef ap_uint<1> bias3_t;
typedef ap_ufixed<10,4,AP_RND,AP_SAT,AP_SAT> layer5_t;
typedef ap_fixed<18,8> relu1_table_t;
typedef ap_fixed<22,8> dense1_accum_t;
typedef ap_fixed<14,8> layer7_t;
typedef ap_fixed<14,2> weight7_t;
typedef ap_uint<1> bias7_t;
typedef ap_uint<1> layer7_index;
typedef ap_ufixed<10,4,AP_RND,AP_SAT,AP_SAT> layer9_t;
typedef ap_fixed<18,8> relu2_table_t;
typedef ap_fixed<17,8> output_accum_t;
typedef ap_fixed<17,8> layer10_t;
typedef ap_fixed<12,2> weight10_t;
typedef ap_uint<1> bias10_t;
typedef ap_uint<1> layer10_index;
typedef ap_ufixed<16,8> result_t;
typedef ap_fixed<18,8> relu3_table_t;

#endif
