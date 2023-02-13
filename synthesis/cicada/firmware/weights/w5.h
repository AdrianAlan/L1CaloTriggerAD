//Numpy array shape [15, 1]
//Min -0.250000000000
//Max 0.500000000000
//Number of zeros 1

#ifndef W5_H_
#define W5_H_

#ifndef __SYNTHESIS__
weight5_t w5[15];
#else
weight5_t w5[15] = {0.125, -0.125, 0.375, -0.125, 0.375, 0.250, -0.125, 0.500, -0.250, 0.250, 0.125, 0.000, 0.375, 0.375, 0.250};
#endif

#endif
