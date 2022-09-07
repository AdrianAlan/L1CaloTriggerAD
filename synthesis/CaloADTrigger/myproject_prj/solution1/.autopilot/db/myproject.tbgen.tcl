set moduleName myproject
set isTopModule 1
set isTaskLevelControl 1
set isCombinational 0
set isDatapathOnly 0
set isFreeRunPipelineModule 0
set isPipelined 1
set pipeline_type dataflow
set FunctionProtocol ap_ctrl_hs
set isOneStateSeq 0
set ProfileFlag 0
set StallSigGenFlag 0
set isEnableWaveformDebug 1
set C_modelName {myproject}
set C_modelType { void 0 }
set C_modelArgList {
	{ link_in_0_V int 128 regular {pointer 0}  }
	{ link_in_1_V int 128 regular {pointer 0}  }
	{ link_in_2_V int 128 regular {pointer 0}  }
	{ link_in_3_V int 128 regular {pointer 0}  }
	{ link_in_4_V int 128 regular {pointer 0}  }
	{ link_in_5_V int 128 regular {pointer 0}  }
	{ link_in_6_V int 128 regular {pointer 0}  }
	{ link_in_7_V int 128 regular {pointer 0}  }
	{ link_in_8_V int 128 regular {pointer 0}  }
	{ link_in_9_V int 128 regular {pointer 0}  }
	{ link_in_10_V int 128 regular {pointer 0}  }
	{ link_in_11_V int 128 regular {pointer 0}  }
	{ link_in_12_V int 128 regular {pointer 0}  }
	{ link_in_13_V int 128 regular {pointer 0}  }
	{ link_in_14_V int 128 regular {pointer 0}  }
	{ link_in_15_V int 128 regular {pointer 0}  }
	{ link_in_16_V int 128 regular {pointer 0}  }
	{ link_in_17_V int 128 regular {pointer 0}  }
	{ link_in_18_V int 128 regular {pointer 0}  }
	{ link_in_19_V int 128 regular {pointer 0}  }
	{ link_in_20_V int 128 regular {pointer 0}  }
	{ link_in_21_V int 128 regular {pointer 0}  }
	{ link_in_22_V int 128 regular {pointer 0}  }
	{ link_in_23_V int 128 regular {pointer 0}  }
	{ link_in_24_V int 128 regular {pointer 0}  }
	{ link_in_25_V int 128 regular {pointer 0}  }
	{ link_in_26_V int 128 regular {pointer 0}  }
	{ link_in_27_V int 128 regular {pointer 0}  }
	{ link_in_28_V int 128 regular {pointer 0}  }
	{ link_in_29_V int 128 regular {pointer 0}  }
	{ link_in_30_V int 128 regular {pointer 0}  }
	{ link_in_31_V int 128 regular {pointer 0}  }
	{ link_in_32_V int 128 regular {pointer 0}  }
	{ link_in_33_V int 128 regular {pointer 0}  }
	{ link_in_34_V int 128 regular {pointer 0}  }
	{ link_in_35_V int 128 regular {pointer 0}  }
	{ link_out_0_V int 128 regular {pointer 2}  }
}
set C_modelArgMapList {[ 
	{ "Name" : "link_in_0_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 0,"up" : 0,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_1_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 1,"up" : 1,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_2_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 2,"up" : 2,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_3_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 3,"up" : 3,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_4_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 4,"up" : 4,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_5_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 5,"up" : 5,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_6_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 6,"up" : 6,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_7_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 7,"up" : 7,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_8_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 8,"up" : 8,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_9_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 9,"up" : 9,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_10_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 10,"up" : 10,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_11_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 11,"up" : 11,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_12_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 12,"up" : 12,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_13_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 13,"up" : 13,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_14_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 14,"up" : 14,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_15_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 15,"up" : 15,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_16_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 16,"up" : 16,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_17_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 17,"up" : 17,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_18_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 18,"up" : 18,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_19_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 19,"up" : 19,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_20_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 20,"up" : 20,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_21_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 21,"up" : 21,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_22_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 22,"up" : 22,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_23_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 23,"up" : 23,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_24_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 24,"up" : 24,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_25_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 25,"up" : 25,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_26_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 26,"up" : 26,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_27_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 27,"up" : 27,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_28_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 28,"up" : 28,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_29_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 29,"up" : 29,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_30_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 30,"up" : 30,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_31_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 31,"up" : 31,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_32_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 32,"up" : 32,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_33_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 33,"up" : 33,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_34_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 34,"up" : 34,"step" : 2}]}]}]} , 
 	{ "Name" : "link_in_35_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READONLY", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_in.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 35,"up" : 35,"step" : 2}]}]}]} , 
 	{ "Name" : "link_out_0_V", "interface" : "wire", "bitwidth" : 128, "direction" : "READWRITE", "bitSlice":[{"low":0,"up":127,"cElement": [{"cName": "link_out.V","cData": "uint128","bit_use": { "low": 0,"up": 127},"cArray": [{"low" : 0,"up" : 0,"step" : 2}]}]}]} ]}
# RTL Port declarations: 
set portNum 45
set portList { 
	{ link_in_0_V sc_in sc_lv 128 signal 0 } 
	{ link_in_1_V sc_in sc_lv 128 signal 1 } 
	{ link_in_2_V sc_in sc_lv 128 signal 2 } 
	{ link_in_3_V sc_in sc_lv 128 signal 3 } 
	{ link_in_4_V sc_in sc_lv 128 signal 4 } 
	{ link_in_5_V sc_in sc_lv 128 signal 5 } 
	{ link_in_6_V sc_in sc_lv 128 signal 6 } 
	{ link_in_7_V sc_in sc_lv 128 signal 7 } 
	{ link_in_8_V sc_in sc_lv 128 signal 8 } 
	{ link_in_9_V sc_in sc_lv 128 signal 9 } 
	{ link_in_10_V sc_in sc_lv 128 signal 10 } 
	{ link_in_11_V sc_in sc_lv 128 signal 11 } 
	{ link_in_12_V sc_in sc_lv 128 signal 12 } 
	{ link_in_13_V sc_in sc_lv 128 signal 13 } 
	{ link_in_14_V sc_in sc_lv 128 signal 14 } 
	{ link_in_15_V sc_in sc_lv 128 signal 15 } 
	{ link_in_16_V sc_in sc_lv 128 signal 16 } 
	{ link_in_17_V sc_in sc_lv 128 signal 17 } 
	{ link_in_18_V sc_in sc_lv 128 signal 18 } 
	{ link_in_19_V sc_in sc_lv 128 signal 19 } 
	{ link_in_20_V sc_in sc_lv 128 signal 20 } 
	{ link_in_21_V sc_in sc_lv 128 signal 21 } 
	{ link_in_22_V sc_in sc_lv 128 signal 22 } 
	{ link_in_23_V sc_in sc_lv 128 signal 23 } 
	{ link_in_24_V sc_in sc_lv 128 signal 24 } 
	{ link_in_25_V sc_in sc_lv 128 signal 25 } 
	{ link_in_26_V sc_in sc_lv 128 signal 26 } 
	{ link_in_27_V sc_in sc_lv 128 signal 27 } 
	{ link_in_28_V sc_in sc_lv 128 signal 28 } 
	{ link_in_29_V sc_in sc_lv 128 signal 29 } 
	{ link_in_30_V sc_in sc_lv 128 signal 30 } 
	{ link_in_31_V sc_in sc_lv 128 signal 31 } 
	{ link_in_32_V sc_in sc_lv 128 signal 32 } 
	{ link_in_33_V sc_in sc_lv 128 signal 33 } 
	{ link_in_34_V sc_in sc_lv 128 signal 34 } 
	{ link_in_35_V sc_in sc_lv 128 signal 35 } 
	{ link_out_0_V_i sc_in sc_lv 128 signal 36 } 
	{ link_out_0_V_o sc_out sc_lv 128 signal 36 } 
	{ ap_clk sc_in sc_logic 1 clock -1 } 
	{ ap_rst sc_in sc_logic 1 reset -1 active_high_sync } 
	{ ap_start sc_in sc_logic 1 start -1 } 
	{ link_out_0_V_o_ap_vld sc_out sc_logic 1 outvld 36 } 
	{ ap_done sc_out sc_logic 1 predone -1 } 
	{ ap_ready sc_out sc_logic 1 ready -1 } 
	{ ap_idle sc_out sc_logic 1 done -1 } 
}
set NewPortList {[ 
	{ "name": "link_in_0_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_0_V", "role": "default" }} , 
 	{ "name": "link_in_1_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_1_V", "role": "default" }} , 
 	{ "name": "link_in_2_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_2_V", "role": "default" }} , 
 	{ "name": "link_in_3_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_3_V", "role": "default" }} , 
 	{ "name": "link_in_4_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_4_V", "role": "default" }} , 
 	{ "name": "link_in_5_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_5_V", "role": "default" }} , 
 	{ "name": "link_in_6_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_6_V", "role": "default" }} , 
 	{ "name": "link_in_7_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_7_V", "role": "default" }} , 
 	{ "name": "link_in_8_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_8_V", "role": "default" }} , 
 	{ "name": "link_in_9_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_9_V", "role": "default" }} , 
 	{ "name": "link_in_10_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_10_V", "role": "default" }} , 
 	{ "name": "link_in_11_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_11_V", "role": "default" }} , 
 	{ "name": "link_in_12_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_12_V", "role": "default" }} , 
 	{ "name": "link_in_13_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_13_V", "role": "default" }} , 
 	{ "name": "link_in_14_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_14_V", "role": "default" }} , 
 	{ "name": "link_in_15_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_15_V", "role": "default" }} , 
 	{ "name": "link_in_16_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_16_V", "role": "default" }} , 
 	{ "name": "link_in_17_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_17_V", "role": "default" }} , 
 	{ "name": "link_in_18_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_18_V", "role": "default" }} , 
 	{ "name": "link_in_19_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_19_V", "role": "default" }} , 
 	{ "name": "link_in_20_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_20_V", "role": "default" }} , 
 	{ "name": "link_in_21_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_21_V", "role": "default" }} , 
 	{ "name": "link_in_22_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_22_V", "role": "default" }} , 
 	{ "name": "link_in_23_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_23_V", "role": "default" }} , 
 	{ "name": "link_in_24_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_24_V", "role": "default" }} , 
 	{ "name": "link_in_25_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_25_V", "role": "default" }} , 
 	{ "name": "link_in_26_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_26_V", "role": "default" }} , 
 	{ "name": "link_in_27_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_27_V", "role": "default" }} , 
 	{ "name": "link_in_28_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_28_V", "role": "default" }} , 
 	{ "name": "link_in_29_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_29_V", "role": "default" }} , 
 	{ "name": "link_in_30_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_30_V", "role": "default" }} , 
 	{ "name": "link_in_31_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_31_V", "role": "default" }} , 
 	{ "name": "link_in_32_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_32_V", "role": "default" }} , 
 	{ "name": "link_in_33_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_33_V", "role": "default" }} , 
 	{ "name": "link_in_34_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_34_V", "role": "default" }} , 
 	{ "name": "link_in_35_V", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_in_35_V", "role": "default" }} , 
 	{ "name": "link_out_0_V_i", "direction": "in", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_out_0_V", "role": "i" }} , 
 	{ "name": "link_out_0_V_o", "direction": "out", "datatype": "sc_lv", "bitwidth":128, "type": "signal", "bundle":{"name": "link_out_0_V", "role": "o" }} , 
 	{ "name": "ap_clk", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "clock", "bundle":{"name": "ap_clk", "role": "default" }} , 
 	{ "name": "ap_rst", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "reset", "bundle":{"name": "ap_rst", "role": "default" }} , 
 	{ "name": "ap_start", "direction": "in", "datatype": "sc_logic", "bitwidth":1, "type": "start", "bundle":{"name": "ap_start", "role": "default" }} , 
 	{ "name": "link_out_0_V_o_ap_vld", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "outvld", "bundle":{"name": "link_out_0_V", "role": "o_ap_vld" }} , 
 	{ "name": "ap_done", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "predone", "bundle":{"name": "ap_done", "role": "default" }} , 
 	{ "name": "ap_ready", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "ready", "bundle":{"name": "ap_ready", "role": "default" }} , 
 	{ "name": "ap_idle", "direction": "out", "datatype": "sc_logic", "bitwidth":1, "type": "done", "bundle":{"name": "ap_idle", "role": "default" }}  ]}

set RtlHierarchyInfo {[
	{"ID" : "0", "Level" : "0", "Path" : "`AUTOTB_DUT_INST", "Parent" : "", "Child" : ["1", "2", "4", "5", "6", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58"],
		"CDFG" : "myproject",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1",
		"Pipeline" : "Dataflow", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "1",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "14", "EstimateLatencyMax" : "16",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "1",
		"InDataflowNetwork" : "0",
		"HasNonBlockingOperation" : "0",
		"InputProcess" : [
			{"ID" : "1", "Name" : "Block_codeRepl320123_proc_U0", "ReadyCount" : "Block_codeRepl320123_proc_U0_ap_ready_count"},
			{"ID" : "6", "Name" : "Block_codeRepl320123320129_proc72_U0", "ReadyCount" : "Block_codeRepl320123320129_proc72_U0_ap_ready_count"}],
		"OutputProcess" : [
			{"ID" : "6", "Name" : "Block_codeRepl320123320129_proc72_U0"}],
		"Port" : [
			{"Name" : "link_in_0_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_0_V"}]},
			{"Name" : "link_in_1_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_1_V"}]},
			{"Name" : "link_in_2_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_2_V"}]},
			{"Name" : "link_in_3_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_3_V"}]},
			{"Name" : "link_in_4_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_4_V"}]},
			{"Name" : "link_in_5_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_5_V"}]},
			{"Name" : "link_in_6_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_6_V"}]},
			{"Name" : "link_in_7_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_7_V"}]},
			{"Name" : "link_in_8_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_8_V"}]},
			{"Name" : "link_in_9_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_9_V"}]},
			{"Name" : "link_in_10_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_10_V"}]},
			{"Name" : "link_in_11_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_11_V"}]},
			{"Name" : "link_in_12_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_12_V"}]},
			{"Name" : "link_in_13_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_13_V"}]},
			{"Name" : "link_in_14_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_14_V"}]},
			{"Name" : "link_in_15_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_15_V"}]},
			{"Name" : "link_in_16_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_16_V"}]},
			{"Name" : "link_in_17_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_17_V"}]},
			{"Name" : "link_in_18_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_18_V"}]},
			{"Name" : "link_in_19_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_19_V"}]},
			{"Name" : "link_in_20_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_20_V"}]},
			{"Name" : "link_in_21_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_21_V"}]},
			{"Name" : "link_in_22_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_22_V"}]},
			{"Name" : "link_in_23_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_23_V"}]},
			{"Name" : "link_in_24_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_24_V"}]},
			{"Name" : "link_in_25_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_25_V"}]},
			{"Name" : "link_in_26_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_26_V"}]},
			{"Name" : "link_in_27_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_27_V"}]},
			{"Name" : "link_in_28_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_28_V"}]},
			{"Name" : "link_in_29_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_29_V"}]},
			{"Name" : "link_in_30_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_30_V"}]},
			{"Name" : "link_in_31_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_31_V"}]},
			{"Name" : "link_in_32_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_32_V"}]},
			{"Name" : "link_in_33_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_33_V"}]},
			{"Name" : "link_in_34_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_34_V"}]},
			{"Name" : "link_in_35_V", "Type" : "None", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "1", "SubInstance" : "Block_codeRepl320123_proc_U0", "Port" : "link_in_35_V"}]},
			{"Name" : "link_out_0_V", "Type" : "OVld", "Direction" : "IO",
				"SubConnect" : [
					{"ID" : "6", "SubInstance" : "Block_codeRepl320123320129_proc72_U0", "Port" : "link_out_0_V"}]},
			{"Name" : "w2_V", "Type" : "Memory", "Direction" : "I",
				"SubConnect" : [
					{"ID" : "2", "SubInstance" : "dense_resource_ap_ufixed_ap_fixed_config2_U0", "Port" : "w2_V"}]}]},
	{"ID" : "1", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.Block_codeRepl320123_proc_U0", "Parent" : "0",
		"CDFG" : "Block_codeRepl320123_proc",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "1",
		"VariableLatency" : "0", "ExactLatency" : "0", "EstimateLatencyMin" : "0", "EstimateLatencyMax" : "0",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "1",
		"HasNonBlockingOperation" : "0",
		"Port" : [
			{"Name" : "link_in_0_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_1_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_2_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_3_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_4_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_5_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_6_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_7_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_8_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_9_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_10_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_11_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_12_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_13_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_14_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_15_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_16_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_17_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_18_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_19_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_20_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_21_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_22_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_23_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_24_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_25_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_26_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_27_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_28_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_29_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_30_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_31_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_32_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_33_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_34_V", "Type" : "None", "Direction" : "I"},
			{"Name" : "link_in_35_V", "Type" : "None", "Direction" : "I"}]},
	{"ID" : "2", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.dense_resource_ap_ufixed_ap_fixed_config2_U0", "Parent" : "0", "Child" : ["3"],
		"CDFG" : "dense_resource_ap_ufixed_ap_fixed_config2_s",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1",
		"Pipeline" : "Rewind", "UnalignedPipeline" : "0", "RewindPipeline" : "1", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "8", "EstimateLatencyMax" : "9",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "1",
		"HasNonBlockingOperation" : "0",
		"Port" : [
			{"Name" : "data_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "1", "DependentChan" : "13"},
			{"Name" : "w2_V", "Type" : "Memory", "Direction" : "I"}]},
	{"ID" : "3", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.dense_resource_ap_ufixed_ap_fixed_config2_U0.w2_V_U", "Parent" : "2"},
	{"ID" : "4", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.normalize_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_U0", "Parent" : "0",
		"CDFG" : "normalize_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_s",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "1",
		"VariableLatency" : "0", "ExactLatency" : "0", "EstimateLatencyMin" : "0", "EstimateLatencyMax" : "0",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "1",
		"HasNonBlockingOperation" : "0",
		"Port" : [
			{"Name" : "p_read", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "14"},
			{"Name" : "p_read1", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "15"},
			{"Name" : "p_read2", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "16"},
			{"Name" : "p_read3", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "17"},
			{"Name" : "p_read4", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "18"},
			{"Name" : "p_read5", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "19"},
			{"Name" : "p_read6", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "20"},
			{"Name" : "p_read7", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "21"},
			{"Name" : "p_read8", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "22"},
			{"Name" : "p_read9", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "23"},
			{"Name" : "p_read10", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "24"},
			{"Name" : "p_read11", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "25"},
			{"Name" : "p_read12", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "26"},
			{"Name" : "p_read13", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "27"},
			{"Name" : "p_read14", "Type" : "None", "Direction" : "I", "DependentProc" : "2", "DependentChan" : "28"}]},
	{"ID" : "5", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.relu_ap_fixed_ap_ufixed_5_2_0_0_0_relu_config5_U0", "Parent" : "0",
		"CDFG" : "relu_ap_fixed_ap_ufixed_5_2_0_0_0_relu_config5_s",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "1",
		"VariableLatency" : "0", "ExactLatency" : "0", "EstimateLatencyMin" : "0", "EstimateLatencyMax" : "0",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "1",
		"HasNonBlockingOperation" : "0",
		"Port" : [
			{"Name" : "data_0_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "29"},
			{"Name" : "data_1_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "30"},
			{"Name" : "data_2_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "31"},
			{"Name" : "data_3_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "32"},
			{"Name" : "data_4_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "33"},
			{"Name" : "data_5_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "34"},
			{"Name" : "data_6_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "35"},
			{"Name" : "data_7_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "36"},
			{"Name" : "data_8_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "37"},
			{"Name" : "data_9_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "38"},
			{"Name" : "data_10_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "39"},
			{"Name" : "data_11_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "40"},
			{"Name" : "data_12_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "41"},
			{"Name" : "data_13_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "42"},
			{"Name" : "data_14_V_read", "Type" : "None", "Direction" : "I", "DependentProc" : "4", "DependentChan" : "43"}]},
	{"ID" : "6", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.Block_codeRepl320123320129_proc72_U0", "Parent" : "0", "Child" : ["7"],
		"CDFG" : "Block_codeRepl320123320129_proc72",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "1", "ap_idle" : "1",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "3", "EstimateLatencyMax" : "4",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "1",
		"HasNonBlockingOperation" : "0",
		"WaitState" : [
			{"State" : "ap_ST_fsm_state2", "FSM" : "ap_CS_fsm", "SubInstance" : "grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157"}],
		"Port" : [
			{"Name" : "p_read", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "44"},
			{"Name" : "p_read1", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "45"},
			{"Name" : "p_read2", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "46"},
			{"Name" : "p_read3", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "47"},
			{"Name" : "p_read4", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "48"},
			{"Name" : "p_read5", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "49"},
			{"Name" : "p_read6", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "50"},
			{"Name" : "p_read7", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "51"},
			{"Name" : "p_read8", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "52"},
			{"Name" : "p_read9", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "53"},
			{"Name" : "p_read10", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "54"},
			{"Name" : "p_read11", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "55"},
			{"Name" : "p_read12", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "56"},
			{"Name" : "p_read13", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "57"},
			{"Name" : "p_read14", "Type" : "None", "Direction" : "I", "DependentProc" : "5", "DependentChan" : "58"},
			{"Name" : "link_out_0_V", "Type" : "OVld", "Direction" : "IO"}]},
	{"ID" : "7", "Level" : "2", "Path" : "`AUTOTB_DUT_INST.Block_codeRepl320123320129_proc72_U0.grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157", "Parent" : "6", "Child" : ["8", "9", "10", "11", "12"],
		"CDFG" : "dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s",
		"Protocol" : "ap_ctrl_hs",
		"ControlExist" : "1", "ap_start" : "1", "ap_ready" : "1", "ap_done" : "1", "ap_continue" : "0", "ap_idle" : "1",
		"Pipeline" : "None", "UnalignedPipeline" : "0", "RewindPipeline" : "0", "ProcessNetwork" : "0",
		"II" : "0",
		"VariableLatency" : "1", "ExactLatency" : "-1", "EstimateLatencyMin" : "2", "EstimateLatencyMax" : "3",
		"Combinational" : "0",
		"Datapath" : "0",
		"ClockEnable" : "0",
		"HasSubDataflow" : "0",
		"InDataflowNetwork" : "0",
		"HasNonBlockingOperation" : "0",
		"Port" : [
			{"Name" : "data_0_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_1_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_2_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_3_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_4_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_5_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_6_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_7_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_8_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_9_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_10_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_11_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_12_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_13_V_read", "Type" : "None", "Direction" : "I"},
			{"Name" : "data_14_V_read", "Type" : "None", "Direction" : "I"}]},
	{"ID" : "8", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.Block_codeRepl320123320129_proc72_U0.grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157.myproject_mux_42_5_1_1_U69", "Parent" : "7"},
	{"ID" : "9", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.Block_codeRepl320123320129_proc72_U0.grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157.myproject_mux_42_5_1_1_U70", "Parent" : "7"},
	{"ID" : "10", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.Block_codeRepl320123320129_proc72_U0.grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157.myproject_mux_42_5_1_1_U71", "Parent" : "7"},
	{"ID" : "11", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.Block_codeRepl320123320129_proc72_U0.grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157.myproject_mux_42_5_1_1_U72", "Parent" : "7"},
	{"ID" : "12", "Level" : "3", "Path" : "`AUTOTB_DUT_INST.Block_codeRepl320123320129_proc72_U0.grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157.myproject_mux_42_5_1_1_U73", "Parent" : "7"},
	{"ID" : "13", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.Inputs_V_channel_U", "Parent" : "0"},
	{"ID" : "14", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_0_V_U", "Parent" : "0"},
	{"ID" : "15", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_1_V_U", "Parent" : "0"},
	{"ID" : "16", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_2_V_U", "Parent" : "0"},
	{"ID" : "17", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_3_V_U", "Parent" : "0"},
	{"ID" : "18", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_4_V_U", "Parent" : "0"},
	{"ID" : "19", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_5_V_U", "Parent" : "0"},
	{"ID" : "20", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_6_V_U", "Parent" : "0"},
	{"ID" : "21", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_7_V_U", "Parent" : "0"},
	{"ID" : "22", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_8_V_U", "Parent" : "0"},
	{"ID" : "23", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_9_V_U", "Parent" : "0"},
	{"ID" : "24", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_10_V_U", "Parent" : "0"},
	{"ID" : "25", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_11_V_U", "Parent" : "0"},
	{"ID" : "26", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_12_V_U", "Parent" : "0"},
	{"ID" : "27", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_13_V_U", "Parent" : "0"},
	{"ID" : "28", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer2_out_14_V_U", "Parent" : "0"},
	{"ID" : "29", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_0_V_U", "Parent" : "0"},
	{"ID" : "30", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_1_V_U", "Parent" : "0"},
	{"ID" : "31", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_2_V_U", "Parent" : "0"},
	{"ID" : "32", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_3_V_U", "Parent" : "0"},
	{"ID" : "33", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_4_V_U", "Parent" : "0"},
	{"ID" : "34", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_5_V_U", "Parent" : "0"},
	{"ID" : "35", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_6_V_U", "Parent" : "0"},
	{"ID" : "36", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_7_V_U", "Parent" : "0"},
	{"ID" : "37", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_8_V_U", "Parent" : "0"},
	{"ID" : "38", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_9_V_U", "Parent" : "0"},
	{"ID" : "39", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_10_V_U", "Parent" : "0"},
	{"ID" : "40", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_11_V_U", "Parent" : "0"},
	{"ID" : "41", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_12_V_U", "Parent" : "0"},
	{"ID" : "42", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_13_V_U", "Parent" : "0"},
	{"ID" : "43", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer4_out_14_V_U", "Parent" : "0"},
	{"ID" : "44", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_0_V_U", "Parent" : "0"},
	{"ID" : "45", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_1_V_U", "Parent" : "0"},
	{"ID" : "46", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_2_V_U", "Parent" : "0"},
	{"ID" : "47", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_3_V_U", "Parent" : "0"},
	{"ID" : "48", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_4_V_U", "Parent" : "0"},
	{"ID" : "49", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_5_V_U", "Parent" : "0"},
	{"ID" : "50", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_6_V_U", "Parent" : "0"},
	{"ID" : "51", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_7_V_U", "Parent" : "0"},
	{"ID" : "52", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_8_V_U", "Parent" : "0"},
	{"ID" : "53", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_9_V_U", "Parent" : "0"},
	{"ID" : "54", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_10_V_U", "Parent" : "0"},
	{"ID" : "55", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_11_V_U", "Parent" : "0"},
	{"ID" : "56", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_12_V_U", "Parent" : "0"},
	{"ID" : "57", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_13_V_U", "Parent" : "0"},
	{"ID" : "58", "Level" : "1", "Path" : "`AUTOTB_DUT_INST.layer5_out_14_V_U", "Parent" : "0"}]}


set ArgLastReadFirstWriteLatency {
	myproject {
		link_in_0_V {Type I LastRead 0 FirstWrite -1}
		link_in_1_V {Type I LastRead 0 FirstWrite -1}
		link_in_2_V {Type I LastRead 0 FirstWrite -1}
		link_in_3_V {Type I LastRead 0 FirstWrite -1}
		link_in_4_V {Type I LastRead 0 FirstWrite -1}
		link_in_5_V {Type I LastRead 0 FirstWrite -1}
		link_in_6_V {Type I LastRead 0 FirstWrite -1}
		link_in_7_V {Type I LastRead 0 FirstWrite -1}
		link_in_8_V {Type I LastRead 0 FirstWrite -1}
		link_in_9_V {Type I LastRead 0 FirstWrite -1}
		link_in_10_V {Type I LastRead 0 FirstWrite -1}
		link_in_11_V {Type I LastRead 0 FirstWrite -1}
		link_in_12_V {Type I LastRead 0 FirstWrite -1}
		link_in_13_V {Type I LastRead 0 FirstWrite -1}
		link_in_14_V {Type I LastRead 0 FirstWrite -1}
		link_in_15_V {Type I LastRead 0 FirstWrite -1}
		link_in_16_V {Type I LastRead 0 FirstWrite -1}
		link_in_17_V {Type I LastRead 0 FirstWrite -1}
		link_in_18_V {Type I LastRead 0 FirstWrite -1}
		link_in_19_V {Type I LastRead 0 FirstWrite -1}
		link_in_20_V {Type I LastRead 0 FirstWrite -1}
		link_in_21_V {Type I LastRead 0 FirstWrite -1}
		link_in_22_V {Type I LastRead 0 FirstWrite -1}
		link_in_23_V {Type I LastRead 0 FirstWrite -1}
		link_in_24_V {Type I LastRead 0 FirstWrite -1}
		link_in_25_V {Type I LastRead 0 FirstWrite -1}
		link_in_26_V {Type I LastRead 0 FirstWrite -1}
		link_in_27_V {Type I LastRead 0 FirstWrite -1}
		link_in_28_V {Type I LastRead 0 FirstWrite -1}
		link_in_29_V {Type I LastRead 0 FirstWrite -1}
		link_in_30_V {Type I LastRead 0 FirstWrite -1}
		link_in_31_V {Type I LastRead 0 FirstWrite -1}
		link_in_32_V {Type I LastRead 0 FirstWrite -1}
		link_in_33_V {Type I LastRead 0 FirstWrite -1}
		link_in_34_V {Type I LastRead 0 FirstWrite -1}
		link_in_35_V {Type I LastRead 0 FirstWrite -1}
		link_out_0_V {Type IO LastRead 1 FirstWrite 1}
		w2_V {Type I LastRead -1 FirstWrite -1}}
	Block_codeRepl320123_proc {
		link_in_0_V {Type I LastRead 0 FirstWrite -1}
		link_in_1_V {Type I LastRead 0 FirstWrite -1}
		link_in_2_V {Type I LastRead 0 FirstWrite -1}
		link_in_3_V {Type I LastRead 0 FirstWrite -1}
		link_in_4_V {Type I LastRead 0 FirstWrite -1}
		link_in_5_V {Type I LastRead 0 FirstWrite -1}
		link_in_6_V {Type I LastRead 0 FirstWrite -1}
		link_in_7_V {Type I LastRead 0 FirstWrite -1}
		link_in_8_V {Type I LastRead 0 FirstWrite -1}
		link_in_9_V {Type I LastRead 0 FirstWrite -1}
		link_in_10_V {Type I LastRead 0 FirstWrite -1}
		link_in_11_V {Type I LastRead 0 FirstWrite -1}
		link_in_12_V {Type I LastRead 0 FirstWrite -1}
		link_in_13_V {Type I LastRead 0 FirstWrite -1}
		link_in_14_V {Type I LastRead 0 FirstWrite -1}
		link_in_15_V {Type I LastRead 0 FirstWrite -1}
		link_in_16_V {Type I LastRead 0 FirstWrite -1}
		link_in_17_V {Type I LastRead 0 FirstWrite -1}
		link_in_18_V {Type I LastRead 0 FirstWrite -1}
		link_in_19_V {Type I LastRead 0 FirstWrite -1}
		link_in_20_V {Type I LastRead 0 FirstWrite -1}
		link_in_21_V {Type I LastRead 0 FirstWrite -1}
		link_in_22_V {Type I LastRead 0 FirstWrite -1}
		link_in_23_V {Type I LastRead 0 FirstWrite -1}
		link_in_24_V {Type I LastRead 0 FirstWrite -1}
		link_in_25_V {Type I LastRead 0 FirstWrite -1}
		link_in_26_V {Type I LastRead 0 FirstWrite -1}
		link_in_27_V {Type I LastRead 0 FirstWrite -1}
		link_in_28_V {Type I LastRead 0 FirstWrite -1}
		link_in_29_V {Type I LastRead 0 FirstWrite -1}
		link_in_30_V {Type I LastRead 0 FirstWrite -1}
		link_in_31_V {Type I LastRead 0 FirstWrite -1}
		link_in_32_V {Type I LastRead 0 FirstWrite -1}
		link_in_33_V {Type I LastRead 0 FirstWrite -1}
		link_in_34_V {Type I LastRead 0 FirstWrite -1}
		link_in_35_V {Type I LastRead 0 FirstWrite -1}}
	dense_resource_ap_ufixed_ap_fixed_config2_s {
		data_V_read {Type I LastRead 1 FirstWrite -1}
		w2_V {Type I LastRead -1 FirstWrite -1}}
	normalize_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_0_s {
		p_read {Type I LastRead 0 FirstWrite -1}
		p_read1 {Type I LastRead 0 FirstWrite -1}
		p_read2 {Type I LastRead 0 FirstWrite -1}
		p_read3 {Type I LastRead 0 FirstWrite -1}
		p_read4 {Type I LastRead 0 FirstWrite -1}
		p_read5 {Type I LastRead 0 FirstWrite -1}
		p_read6 {Type I LastRead 0 FirstWrite -1}
		p_read7 {Type I LastRead 0 FirstWrite -1}
		p_read8 {Type I LastRead 0 FirstWrite -1}
		p_read9 {Type I LastRead 0 FirstWrite -1}
		p_read10 {Type I LastRead 0 FirstWrite -1}
		p_read11 {Type I LastRead 0 FirstWrite -1}
		p_read12 {Type I LastRead 0 FirstWrite -1}
		p_read13 {Type I LastRead 0 FirstWrite -1}
		p_read14 {Type I LastRead 0 FirstWrite -1}}
	relu_ap_fixed_ap_ufixed_5_2_0_0_0_relu_config5_s {
		data_0_V_read {Type I LastRead 0 FirstWrite -1}
		data_1_V_read {Type I LastRead 0 FirstWrite -1}
		data_2_V_read {Type I LastRead 0 FirstWrite -1}
		data_3_V_read {Type I LastRead 0 FirstWrite -1}
		data_4_V_read {Type I LastRead 0 FirstWrite -1}
		data_5_V_read {Type I LastRead 0 FirstWrite -1}
		data_6_V_read {Type I LastRead 0 FirstWrite -1}
		data_7_V_read {Type I LastRead 0 FirstWrite -1}
		data_8_V_read {Type I LastRead 0 FirstWrite -1}
		data_9_V_read {Type I LastRead 0 FirstWrite -1}
		data_10_V_read {Type I LastRead 0 FirstWrite -1}
		data_11_V_read {Type I LastRead 0 FirstWrite -1}
		data_12_V_read {Type I LastRead 0 FirstWrite -1}
		data_13_V_read {Type I LastRead 0 FirstWrite -1}
		data_14_V_read {Type I LastRead 0 FirstWrite -1}}
	Block_codeRepl320123320129_proc72 {
		p_read {Type I LastRead 0 FirstWrite -1}
		p_read1 {Type I LastRead 0 FirstWrite -1}
		p_read2 {Type I LastRead 0 FirstWrite -1}
		p_read3 {Type I LastRead 0 FirstWrite -1}
		p_read4 {Type I LastRead 0 FirstWrite -1}
		p_read5 {Type I LastRead 0 FirstWrite -1}
		p_read6 {Type I LastRead 0 FirstWrite -1}
		p_read7 {Type I LastRead 0 FirstWrite -1}
		p_read8 {Type I LastRead 0 FirstWrite -1}
		p_read9 {Type I LastRead 0 FirstWrite -1}
		p_read10 {Type I LastRead 0 FirstWrite -1}
		p_read11 {Type I LastRead 0 FirstWrite -1}
		p_read12 {Type I LastRead 0 FirstWrite -1}
		p_read13 {Type I LastRead 0 FirstWrite -1}
		p_read14 {Type I LastRead 0 FirstWrite -1}
		link_out_0_V {Type IO LastRead 1 FirstWrite 1}}
	dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s {
		data_0_V_read {Type I LastRead 1 FirstWrite -1}
		data_1_V_read {Type I LastRead 1 FirstWrite -1}
		data_2_V_read {Type I LastRead 1 FirstWrite -1}
		data_3_V_read {Type I LastRead 1 FirstWrite -1}
		data_4_V_read {Type I LastRead 1 FirstWrite -1}
		data_5_V_read {Type I LastRead 1 FirstWrite -1}
		data_6_V_read {Type I LastRead 1 FirstWrite -1}
		data_7_V_read {Type I LastRead 1 FirstWrite -1}
		data_8_V_read {Type I LastRead 1 FirstWrite -1}
		data_9_V_read {Type I LastRead 1 FirstWrite -1}
		data_10_V_read {Type I LastRead 1 FirstWrite -1}
		data_11_V_read {Type I LastRead 1 FirstWrite -1}
		data_12_V_read {Type I LastRead 1 FirstWrite -1}
		data_13_V_read {Type I LastRead 1 FirstWrite -1}
		data_14_V_read {Type I LastRead 1 FirstWrite -1}}}

set hasDtUnsupportedChannel 0

set PerformanceInfo {[
	{"Name" : "Latency", "Min" : "14", "Max" : "16"}
	, {"Name" : "Interval", "Min" : "4", "Max" : "5"}
]}

set PipelineEnableSignalInfo {[
]}

set Spec2ImplPortList { 
	link_in_0_V { ap_none {  { link_in_0_V in_data 0 128 } } }
	link_in_1_V { ap_none {  { link_in_1_V in_data 0 128 } } }
	link_in_2_V { ap_none {  { link_in_2_V in_data 0 128 } } }
	link_in_3_V { ap_none {  { link_in_3_V in_data 0 128 } } }
	link_in_4_V { ap_none {  { link_in_4_V in_data 0 128 } } }
	link_in_5_V { ap_none {  { link_in_5_V in_data 0 128 } } }
	link_in_6_V { ap_none {  { link_in_6_V in_data 0 128 } } }
	link_in_7_V { ap_none {  { link_in_7_V in_data 0 128 } } }
	link_in_8_V { ap_none {  { link_in_8_V in_data 0 128 } } }
	link_in_9_V { ap_none {  { link_in_9_V in_data 0 128 } } }
	link_in_10_V { ap_none {  { link_in_10_V in_data 0 128 } } }
	link_in_11_V { ap_none {  { link_in_11_V in_data 0 128 } } }
	link_in_12_V { ap_none {  { link_in_12_V in_data 0 128 } } }
	link_in_13_V { ap_none {  { link_in_13_V in_data 0 128 } } }
	link_in_14_V { ap_none {  { link_in_14_V in_data 0 128 } } }
	link_in_15_V { ap_none {  { link_in_15_V in_data 0 128 } } }
	link_in_16_V { ap_none {  { link_in_16_V in_data 0 128 } } }
	link_in_17_V { ap_none {  { link_in_17_V in_data 0 128 } } }
	link_in_18_V { ap_none {  { link_in_18_V in_data 0 128 } } }
	link_in_19_V { ap_none {  { link_in_19_V in_data 0 128 } } }
	link_in_20_V { ap_none {  { link_in_20_V in_data 0 128 } } }
	link_in_21_V { ap_none {  { link_in_21_V in_data 0 128 } } }
	link_in_22_V { ap_none {  { link_in_22_V in_data 0 128 } } }
	link_in_23_V { ap_none {  { link_in_23_V in_data 0 128 } } }
	link_in_24_V { ap_none {  { link_in_24_V in_data 0 128 } } }
	link_in_25_V { ap_none {  { link_in_25_V in_data 0 128 } } }
	link_in_26_V { ap_none {  { link_in_26_V in_data 0 128 } } }
	link_in_27_V { ap_none {  { link_in_27_V in_data 0 128 } } }
	link_in_28_V { ap_none {  { link_in_28_V in_data 0 128 } } }
	link_in_29_V { ap_none {  { link_in_29_V in_data 0 128 } } }
	link_in_30_V { ap_none {  { link_in_30_V in_data 0 128 } } }
	link_in_31_V { ap_none {  { link_in_31_V in_data 0 128 } } }
	link_in_32_V { ap_none {  { link_in_32_V in_data 0 128 } } }
	link_in_33_V { ap_none {  { link_in_33_V in_data 0 128 } } }
	link_in_34_V { ap_none {  { link_in_34_V in_data 0 128 } } }
	link_in_35_V { ap_none {  { link_in_35_V in_data 0 128 } } }
	link_out_0_V { ap_ovld {  { link_out_0_V_i in_data 0 128 }  { link_out_0_V_o out_data 1 128 }  { link_out_0_V_o_ap_vld out_vld 1 1 } } }
}

set busDeadlockParameterList { 
}

# RTL port scheduling information:
set fifoSchedulingInfoList { 
}

# RTL bus port read request latency information:
set busReadReqLatencyList { 
}

# RTL bus port write response latency information:
set busWriteResLatencyList { 
}

# RTL array port load latency information:
set memoryLoadLatencyList { 
}
