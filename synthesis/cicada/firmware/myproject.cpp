//
//    rfnoc-hls-neuralnet: Vivado HLS code for neural-net building blocks
//
//    Copyright (C) 2017 EJ Kreinar
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//********************
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <hls_math.h>

#include <fstream>
#include <iomanip>
#include <string>
//************
#include <iostream>

#include "myproject.h"
#include "parameters.h"

const uint16_t NRegionsPerLink = 7; // Bits 8-21, 22-39, 40-55,..., 104-119, keeping ranges (7, 0) and (127, 120) unused
const uint16_t MaxRegions = N_CH_IN * NRegionsPerLink;

void myproject(ap_uint<128> link_in[N_CH_IN], ap_uint<128> link_out[N_CH_OUT]) {
    // ALGO UNPACK START

    // !!! Retain these 4 #pragma directives below in your algo_unpacked implementation !!!
    #pragma HLS ARRAY_PARTITION variable=link_in complete dim=0
    #pragma HLS ARRAY_PARTITION variable=link_out complete dim=0
    #pragma HLS INTERFACE ap_ctrl_hs port=return
    
    // null algo specific pragma: avoid fully combinatorial algo by specifying min latency
    // otherwise algorithm clock input (ap_clk) gets optimized away
    #pragma HLS latency min=4

    static bool first = true; //true to print 
    region_t centr_region[NR_CNTR_REG];
#pragma HLS ARRAY_PARTITION variable=centr_region complete dim=1
    regionLoop: for(int iRegion = 0; iRegion < NR_CNTR_REG; iRegion++) {
#pragma HLS UNROLL
            if(iRegion > MaxRegions) {
                    fprintf(stderr, "Too many regions - aborting");
                    exit(1);
            }
            int link_idx = iRegion / NRegionsPerLink;
            int bitLo = ((iRegion - link_idx * NRegionsPerLink) % NRegionsPerLink) * 16 + 8;
            int bitHi = bitLo + 15;
            uint16_t region_raw = link_in[link_idx].range(bitHi, bitLo);
            centr_region[iRegion].et = (region_raw & 0x3FF >> 0);   // 10 bits
            centr_region[iRegion].eg_veto = (region_raw & 0x7FF) >> 10;   // 1 bit
            centr_region[iRegion].tau_veto = (region_raw & 0xFFF) >> 11;   // 1 bit
            centr_region[iRegion].rloc_phi = (region_raw & 0x3FFF) >> 12;   // 2 bit
            centr_region[iRegion].rloc_eta = (region_raw & 0xFFFF) >> 14;   // 2 bit
            //cout << "Calo region " << " ET: " << centr_region[iRegion].et << " Eta: " << centr_region[iRegion].rloc_eta << " Phi: " << centr_region[iRegion].rloc_phi << " EG veto: " << centr_region[iRegion].eg_veto << " Tau veto: " << centr_region[iRegion].tau_veto << endl;
    }
    //cout<<"Got all regions"<<endl;

    input_t Inputs[N_INPUT_1_1];
    result_t layer6_out[N_LAYER_6];

    //hls-fpga-machine-learning insert IO
    #pragma HLS ARRAY_RESHAPE variable=Inputs complete dim=0
    #pragma HLS ARRAY_PARTITION variable=layer6_out complete dim=0
    #pragma HLS INTERFACE ap_vld port=Inputs,layer6_out 
    #pragma HLS DATAFLOW 

    // Unpack calo ET values in et_calo array
    for (int idx = 0; idx < NR_CNTR_REG; idx++) {
#pragma HLS UNROLL
            Inputs[idx] = centr_region[idx].et;
    }
    
#ifndef __SYNTHESIS__
    static bool loaded_weights = false;
    if (!loaded_weights) {
        //hls-fpga-machine-learning insert load weights
        nnet::load_weights_from_txt<weight2_t, 3780>(w2, "w2.txt");
        nnet::load_weights_from_txt<bias2_t, 15>(b2, "b2.txt");
        nnet::load_weights_from_txt<qbn_1_scale_t, 15>(s4, "s4.txt");
        nnet::load_weights_from_txt<qbn_1_bias_t, 15>(b4, "b4.txt");
        nnet::load_weights_from_txt<weight6_t, 15>(w6, "w6.txt");
        nnet::load_weights_from_txt<bias6_t, 1>(b6, "b6.txt");
        loaded_weights = true;
    }
#endif

    // ****************************************
    // NETWORK INSTANTIATION
    // ****************************************

    //hls-fpga-machine-learning insert layers

    layer2_t layer2_out[N_LAYER_2];
    #pragma HLS ARRAY_PARTITION variable=layer2_out complete dim=0
    nnet::dense<input_t, layer2_t, config2>(Inputs, layer2_out, w2, b2); // Dense_1

    layer4_t layer4_out[N_LAYER_2];
    #pragma HLS ARRAY_PARTITION variable=layer4_out complete dim=0
    nnet::normalize<layer2_t, layer4_t, config4>(layer2_out, layer4_out, s4, b4); // QBN_1

    layer5_t layer5_out[N_LAYER_2];
    #pragma HLS ARRAY_PARTITION variable=layer5_out complete dim=0
    nnet::relu<layer4_t, layer5_t, relu_config5>(layer4_out, layer5_out); // Activation_1

    nnet::dense<layer5_t, result_t, config6>(layer5_out, layer6_out, w6, b6); // Out

    link_out[0].range(119, 8) = layer6_out;
}
