#ifndef NNET_INSTR_GEN_H_
#define NNET_INSTR_GEN_H_

#include <iostream>
#include "nnet_helpers.h"

namespace nnet {

template<class data_T, typename CONFIG_T>
class FillConv1DBuffer{
    public:
    static void fill_buffer(
        data_T data[CONFIG_T::in_width * CONFIG_T::n_chan],
        data_T buffer[CONFIG_T::n_pixels][CONFIG_T::filt_width * CONFIG_T::n_chan],
        const unsigned partition
    ) {
        // To be implemented in subclasses
    }
};

template<class data_T, typename CONFIG_T>
class FillConv2DBuffer{
    public:
    static void fill_buffer(
        data_T data[CONFIG_T::in_height * CONFIG_T::in_width * CONFIG_T::n_chan],
        data_T buffer[CONFIG_T::n_pixels][CONFIG_T::filt_height * CONFIG_T::filt_width * CONFIG_T::n_chan],
        const unsigned partition
    ) {
        // To be implemented in subclasses
    }
};

//hls4ml insert code
template<class data_T, typename CONFIG_T>
class fill_buffer_3 : public FillConv2DBuffer<data_T, CONFIG_T> {
    public:
    static void fill_buffer(
        data_T data[CONFIG_T::in_height * CONFIG_T::in_width * CONFIG_T::n_chan],
        data_T buffer[CONFIG_T::n_pixels][CONFIG_T::filt_height * CONFIG_T::filt_width * CONFIG_T::n_chan],
        const unsigned partition
    ) {
        if (partition ==   0) {
            buffer[0][0] =    data[0]; buffer[0][1] =    data[1]; buffer[0][2] =    data[2]; buffer[0][3] =   data[14]; buffer[0][4] =   data[15]; buffer[0][5] =   data[16]; buffer[0][6] =   data[28]; buffer[0][7] =   data[29]; buffer[0][8] =   data[30];
            buffer[1][0] =    data[2]; buffer[1][1] =    data[3]; buffer[1][2] =    data[4]; buffer[1][3] =   data[16]; buffer[1][4] =   data[17]; buffer[1][5] =   data[18]; buffer[1][6] =   data[30]; buffer[1][7] =   data[31]; buffer[1][8] =   data[32];
            buffer[2][0] =    data[4]; buffer[2][1] =    data[5]; buffer[2][2] =    data[6]; buffer[2][3] =   data[18]; buffer[2][4] =   data[19]; buffer[2][5] =   data[20]; buffer[2][6] =   data[32]; buffer[2][7] =   data[33]; buffer[2][8] =   data[34];
            buffer[3][0] =    data[6]; buffer[3][1] =    data[7]; buffer[3][2] =    data[8]; buffer[3][3] =   data[20]; buffer[3][4] =   data[21]; buffer[3][5] =   data[22]; buffer[3][6] =   data[34]; buffer[3][7] =   data[35]; buffer[3][8] =   data[36];
            buffer[4][0] =    data[8]; buffer[4][1] =    data[9]; buffer[4][2] =   data[10]; buffer[4][3] =   data[22]; buffer[4][4] =   data[23]; buffer[4][5] =   data[24]; buffer[4][6] =   data[36]; buffer[4][7] =   data[37]; buffer[4][8] =   data[38];
            buffer[5][0] =   data[10]; buffer[5][1] =   data[11]; buffer[5][2] =   data[12]; buffer[5][3] =   data[24]; buffer[5][4] =   data[25]; buffer[5][5] =   data[26]; buffer[5][6] =   data[38]; buffer[5][7] =   data[39]; buffer[5][8] =   data[40];
            buffer[6][0] =   data[28]; buffer[6][1] =   data[29]; buffer[6][2] =   data[30]; buffer[6][3] =   data[42]; buffer[6][4] =   data[43]; buffer[6][5] =   data[44]; buffer[6][6] =   data[56]; buffer[6][7] =   data[57]; buffer[6][8] =   data[58];
            buffer[7][0] =   data[30]; buffer[7][1] =   data[31]; buffer[7][2] =   data[32]; buffer[7][3] =   data[44]; buffer[7][4] =   data[45]; buffer[7][5] =   data[46]; buffer[7][6] =   data[58]; buffer[7][7] =   data[59]; buffer[7][8] =   data[60];
            buffer[8][0] =   data[32]; buffer[8][1] =   data[33]; buffer[8][2] =   data[34]; buffer[8][3] =   data[46]; buffer[8][4] =   data[47]; buffer[8][5] =   data[48]; buffer[8][6] =   data[60]; buffer[8][7] =   data[61]; buffer[8][8] =   data[62];
            buffer[9][0] =   data[34]; buffer[9][1] =   data[35]; buffer[9][2] =   data[36]; buffer[9][3] =   data[48]; buffer[9][4] =   data[49]; buffer[9][5] =   data[50]; buffer[9][6] =   data[62]; buffer[9][7] =   data[63]; buffer[9][8] =   data[64];
            buffer[10][0] =   data[36]; buffer[10][1] =   data[37]; buffer[10][2] =   data[38]; buffer[10][3] =   data[50]; buffer[10][4] =   data[51]; buffer[10][5] =   data[52]; buffer[10][6] =   data[64]; buffer[10][7] =   data[65]; buffer[10][8] =   data[66];
            buffer[11][0] =   data[38]; buffer[11][1] =   data[39]; buffer[11][2] =   data[40]; buffer[11][3] =   data[52]; buffer[11][4] =   data[53]; buffer[11][5] =   data[54]; buffer[11][6] =   data[66]; buffer[11][7] =   data[67]; buffer[11][8] =   data[68];

        }
        if (partition ==   1) {
            buffer[0][0] =   data[56]; buffer[0][1] =   data[57]; buffer[0][2] =   data[58]; buffer[0][3] =   data[70]; buffer[0][4] =   data[71]; buffer[0][5] =   data[72]; buffer[0][6] =   data[84]; buffer[0][7] =   data[85]; buffer[0][8] =   data[86];
            buffer[1][0] =   data[58]; buffer[1][1] =   data[59]; buffer[1][2] =   data[60]; buffer[1][3] =   data[72]; buffer[1][4] =   data[73]; buffer[1][5] =   data[74]; buffer[1][6] =   data[86]; buffer[1][7] =   data[87]; buffer[1][8] =   data[88];
            buffer[2][0] =   data[60]; buffer[2][1] =   data[61]; buffer[2][2] =   data[62]; buffer[2][3] =   data[74]; buffer[2][4] =   data[75]; buffer[2][5] =   data[76]; buffer[2][6] =   data[88]; buffer[2][7] =   data[89]; buffer[2][8] =   data[90];
            buffer[3][0] =   data[62]; buffer[3][1] =   data[63]; buffer[3][2] =   data[64]; buffer[3][3] =   data[76]; buffer[3][4] =   data[77]; buffer[3][5] =   data[78]; buffer[3][6] =   data[90]; buffer[3][7] =   data[91]; buffer[3][8] =   data[92];
            buffer[4][0] =   data[64]; buffer[4][1] =   data[65]; buffer[4][2] =   data[66]; buffer[4][3] =   data[78]; buffer[4][4] =   data[79]; buffer[4][5] =   data[80]; buffer[4][6] =   data[92]; buffer[4][7] =   data[93]; buffer[4][8] =   data[94];
            buffer[5][0] =   data[66]; buffer[5][1] =   data[67]; buffer[5][2] =   data[68]; buffer[5][3] =   data[80]; buffer[5][4] =   data[81]; buffer[5][5] =   data[82]; buffer[5][6] =   data[94]; buffer[5][7] =   data[95]; buffer[5][8] =   data[96];
            buffer[6][0] =   data[84]; buffer[6][1] =   data[85]; buffer[6][2] =   data[86]; buffer[6][3] =   data[98]; buffer[6][4] =   data[99]; buffer[6][5] =  data[100]; buffer[6][6] =  data[112]; buffer[6][7] =  data[113]; buffer[6][8] =  data[114];
            buffer[7][0] =   data[86]; buffer[7][1] =   data[87]; buffer[7][2] =   data[88]; buffer[7][3] =  data[100]; buffer[7][4] =  data[101]; buffer[7][5] =  data[102]; buffer[7][6] =  data[114]; buffer[7][7] =  data[115]; buffer[7][8] =  data[116];
            buffer[8][0] =   data[88]; buffer[8][1] =   data[89]; buffer[8][2] =   data[90]; buffer[8][3] =  data[102]; buffer[8][4] =  data[103]; buffer[8][5] =  data[104]; buffer[8][6] =  data[116]; buffer[8][7] =  data[117]; buffer[8][8] =  data[118];
            buffer[9][0] =   data[90]; buffer[9][1] =   data[91]; buffer[9][2] =   data[92]; buffer[9][3] =  data[104]; buffer[9][4] =  data[105]; buffer[9][5] =  data[106]; buffer[9][6] =  data[118]; buffer[9][7] =  data[119]; buffer[9][8] =  data[120];
            buffer[10][0] =   data[92]; buffer[10][1] =   data[93]; buffer[10][2] =   data[94]; buffer[10][3] =  data[106]; buffer[10][4] =  data[107]; buffer[10][5] =  data[108]; buffer[10][6] =  data[120]; buffer[10][7] =  data[121]; buffer[10][8] =  data[122];
            buffer[11][0] =   data[94]; buffer[11][1] =   data[95]; buffer[11][2] =   data[96]; buffer[11][3] =  data[108]; buffer[11][4] =  data[109]; buffer[11][5] =  data[110]; buffer[11][6] =  data[122]; buffer[11][7] =  data[123]; buffer[11][8] =  data[124];

        }
        if (partition ==   2) {
            buffer[0][0] =  data[112]; buffer[0][1] =  data[113]; buffer[0][2] =  data[114]; buffer[0][3] =  data[126]; buffer[0][4] =  data[127]; buffer[0][5] =  data[128]; buffer[0][6] =  data[140]; buffer[0][7] =  data[141]; buffer[0][8] =  data[142];
            buffer[1][0] =  data[114]; buffer[1][1] =  data[115]; buffer[1][2] =  data[116]; buffer[1][3] =  data[128]; buffer[1][4] =  data[129]; buffer[1][5] =  data[130]; buffer[1][6] =  data[142]; buffer[1][7] =  data[143]; buffer[1][8] =  data[144];
            buffer[2][0] =  data[116]; buffer[2][1] =  data[117]; buffer[2][2] =  data[118]; buffer[2][3] =  data[130]; buffer[2][4] =  data[131]; buffer[2][5] =  data[132]; buffer[2][6] =  data[144]; buffer[2][7] =  data[145]; buffer[2][8] =  data[146];
            buffer[3][0] =  data[118]; buffer[3][1] =  data[119]; buffer[3][2] =  data[120]; buffer[3][3] =  data[132]; buffer[3][4] =  data[133]; buffer[3][5] =  data[134]; buffer[3][6] =  data[146]; buffer[3][7] =  data[147]; buffer[3][8] =  data[148];
            buffer[4][0] =  data[120]; buffer[4][1] =  data[121]; buffer[4][2] =  data[122]; buffer[4][3] =  data[134]; buffer[4][4] =  data[135]; buffer[4][5] =  data[136]; buffer[4][6] =  data[148]; buffer[4][7] =  data[149]; buffer[4][8] =  data[150];
            buffer[5][0] =  data[122]; buffer[5][1] =  data[123]; buffer[5][2] =  data[124]; buffer[5][3] =  data[136]; buffer[5][4] =  data[137]; buffer[5][5] =  data[138]; buffer[5][6] =  data[150]; buffer[5][7] =  data[151]; buffer[5][8] =  data[152];
            buffer[6][0] =  data[140]; buffer[6][1] =  data[141]; buffer[6][2] =  data[142]; buffer[6][3] =  data[154]; buffer[6][4] =  data[155]; buffer[6][5] =  data[156]; buffer[6][6] =  data[168]; buffer[6][7] =  data[169]; buffer[6][8] =  data[170];
            buffer[7][0] =  data[142]; buffer[7][1] =  data[143]; buffer[7][2] =  data[144]; buffer[7][3] =  data[156]; buffer[7][4] =  data[157]; buffer[7][5] =  data[158]; buffer[7][6] =  data[170]; buffer[7][7] =  data[171]; buffer[7][8] =  data[172];
            buffer[8][0] =  data[144]; buffer[8][1] =  data[145]; buffer[8][2] =  data[146]; buffer[8][3] =  data[158]; buffer[8][4] =  data[159]; buffer[8][5] =  data[160]; buffer[8][6] =  data[172]; buffer[8][7] =  data[173]; buffer[8][8] =  data[174];
            buffer[9][0] =  data[146]; buffer[9][1] =  data[147]; buffer[9][2] =  data[148]; buffer[9][3] =  data[160]; buffer[9][4] =  data[161]; buffer[9][5] =  data[162]; buffer[9][6] =  data[174]; buffer[9][7] =  data[175]; buffer[9][8] =  data[176];
            buffer[10][0] =  data[148]; buffer[10][1] =  data[149]; buffer[10][2] =  data[150]; buffer[10][3] =  data[162]; buffer[10][4] =  data[163]; buffer[10][5] =  data[164]; buffer[10][6] =  data[176]; buffer[10][7] =  data[177]; buffer[10][8] =  data[178];
            buffer[11][0] =  data[150]; buffer[11][1] =  data[151]; buffer[11][2] =  data[152]; buffer[11][3] =  data[164]; buffer[11][4] =  data[165]; buffer[11][5] =  data[166]; buffer[11][6] =  data[178]; buffer[11][7] =  data[179]; buffer[11][8] =  data[180];

        }
        if (partition ==   3) {
            buffer[0][0] =  data[168]; buffer[0][1] =  data[169]; buffer[0][2] =  data[170]; buffer[0][3] =  data[182]; buffer[0][4] =  data[183]; buffer[0][5] =  data[184]; buffer[0][6] =  data[196]; buffer[0][7] =  data[197]; buffer[0][8] =  data[198];
            buffer[1][0] =  data[170]; buffer[1][1] =  data[171]; buffer[1][2] =  data[172]; buffer[1][3] =  data[184]; buffer[1][4] =  data[185]; buffer[1][5] =  data[186]; buffer[1][6] =  data[198]; buffer[1][7] =  data[199]; buffer[1][8] =  data[200];
            buffer[2][0] =  data[172]; buffer[2][1] =  data[173]; buffer[2][2] =  data[174]; buffer[2][3] =  data[186]; buffer[2][4] =  data[187]; buffer[2][5] =  data[188]; buffer[2][6] =  data[200]; buffer[2][7] =  data[201]; buffer[2][8] =  data[202];
            buffer[3][0] =  data[174]; buffer[3][1] =  data[175]; buffer[3][2] =  data[176]; buffer[3][3] =  data[188]; buffer[3][4] =  data[189]; buffer[3][5] =  data[190]; buffer[3][6] =  data[202]; buffer[3][7] =  data[203]; buffer[3][8] =  data[204];
            buffer[4][0] =  data[176]; buffer[4][1] =  data[177]; buffer[4][2] =  data[178]; buffer[4][3] =  data[190]; buffer[4][4] =  data[191]; buffer[4][5] =  data[192]; buffer[4][6] =  data[204]; buffer[4][7] =  data[205]; buffer[4][8] =  data[206];
            buffer[5][0] =  data[178]; buffer[5][1] =  data[179]; buffer[5][2] =  data[180]; buffer[5][3] =  data[192]; buffer[5][4] =  data[193]; buffer[5][5] =  data[194]; buffer[5][6] =  data[206]; buffer[5][7] =  data[207]; buffer[5][8] =  data[208];
            buffer[6][0] =  data[196]; buffer[6][1] =  data[197]; buffer[6][2] =  data[198]; buffer[6][3] =  data[210]; buffer[6][4] =  data[211]; buffer[6][5] =  data[212]; buffer[6][6] =  data[224]; buffer[6][7] =  data[225]; buffer[6][8] =  data[226];
            buffer[7][0] =  data[198]; buffer[7][1] =  data[199]; buffer[7][2] =  data[200]; buffer[7][3] =  data[212]; buffer[7][4] =  data[213]; buffer[7][5] =  data[214]; buffer[7][6] =  data[226]; buffer[7][7] =  data[227]; buffer[7][8] =  data[228];
            buffer[8][0] =  data[200]; buffer[8][1] =  data[201]; buffer[8][2] =  data[202]; buffer[8][3] =  data[214]; buffer[8][4] =  data[215]; buffer[8][5] =  data[216]; buffer[8][6] =  data[228]; buffer[8][7] =  data[229]; buffer[8][8] =  data[230];
            buffer[9][0] =  data[202]; buffer[9][1] =  data[203]; buffer[9][2] =  data[204]; buffer[9][3] =  data[216]; buffer[9][4] =  data[217]; buffer[9][5] =  data[218]; buffer[9][6] =  data[230]; buffer[9][7] =  data[231]; buffer[9][8] =  data[232];
            buffer[10][0] =  data[204]; buffer[10][1] =  data[205]; buffer[10][2] =  data[206]; buffer[10][3] =  data[218]; buffer[10][4] =  data[219]; buffer[10][5] =  data[220]; buffer[10][6] =  data[232]; buffer[10][7] =  data[233]; buffer[10][8] =  data[234];
            buffer[11][0] =  data[206]; buffer[11][1] =  data[207]; buffer[11][2] =  data[208]; buffer[11][3] =  data[220]; buffer[11][4] =  data[221]; buffer[11][5] =  data[222]; buffer[11][6] =  data[234]; buffer[11][7] =  data[235]; buffer[11][8] =  data[236];

        }
    }
};

}

#endif