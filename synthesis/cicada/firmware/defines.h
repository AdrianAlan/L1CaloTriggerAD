#ifndef DEFINES_H_
#define DEFINES_H_

#include "ap_int.h"
#include "ap_fixed.h"
#include "nnet_utils/nnet_types.h"
#include <cstddef>
#include <cstdio>

//hls-fpga-machine-learning insert numbers
#define N_INPUT_1_1 252
#define N_CH_IN 36
#define NR_CNTR_REG 252
#define N_LAYER_2 15
#define N_CH_OUT 1
#define N_LAYER_6 1

//hls-fpga-machine-learning insert layer-precision
typedef ap_ufixed<10,10> inputs_accum_t;
typedef ap_ufixed<10,10> input_t;
typedef ap_fixed<20,18> dense_1_accum_t;
typedef ap_fixed<20,18> layer2_t;
typedef ap_fixed<2,1> weight2_t;
typedef ap_uint<1> bias2_t;
typedef ap_uint<1> layer2_index;
typedef ap_fixed<20,10> qbn_1_accum_t;
typedef ap_fixed<20,10> layer4_t;
typedef ap_fixed<16,6> qbn_1_scale_t;
typedef ap_fixed<16,6> qbn_1_bias_t;
typedef ap_ufixed<5,2,AP_RND,AP_SAT,AP_SAT> layer5_t;
typedef ap_fixed<18,8> Activation_1_table_t;
typedef ap_fixed<16,5> out_accum_t;
typedef ap_fixed<16,5> result_t;
typedef ap_fixed<4,1> weight6_t;
typedef ap_uint<1> bias6_t;
typedef ap_uint<1> layer6_index;

#endif
