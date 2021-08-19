/*
 * Copyright (C) 2014-2015, 2018 Intel Corporation
 *
 * SPDX-License-Identifier: MIT
 */

#define _XOPEN_SOURCE
#define _DEFAULT_SOURCE 
#include <stdlib.h>
#include <stdio.h>
#include <ia32intrin.h>
#include <omp.h>

#include "euro_opt.h"

using namespace std;
using namespace cl::sycl;

tfloat RandRange( tfloat a, tfloat b, struct drand48_data *seed ) {
    double r;
    drand48_r(seed, &r);
    return r*(b-a) + a;
}

/*
// This function allocates arrays to hold input and output parameters
// for the Black-Scholes formula.
//     nopt - length of arrays
// Random input parameters
//     s0   - initial price
//     x    - strike price
//     t    - maturity
// Output arrays for call and put prices
//     vcall_compiler
//     vput_compiler
*/
void InitData( queue *q, size_t nopt, tfloat* *s0, tfloat* *x, tfloat* *t,
                   tfloat* *vcall_compiler, tfloat* *vput_compiler)
{
    tfloat *ts0, *tx, *tt, *tvcall_compiler, *tvput_compiler;
    int i;

    /* Allocate aligned memory */
    ts0             = (tfloat*)malloc_shared( nopt * sizeof(tfloat), *q);
    tx              = (tfloat*)malloc_shared( nopt * sizeof(tfloat), *q);
    tt              = (tfloat*)malloc_shared( nopt * sizeof(tfloat), *q);
    tvcall_compiler = (tfloat*)malloc_shared( nopt * sizeof(tfloat), *q);
    tvput_compiler  = (tfloat*)malloc_shared( nopt * sizeof(tfloat), *q);

    if ( (ts0 == NULL) || (tx == NULL) || (tt == NULL) ||
         (tvcall_compiler == NULL) || (tvput_compiler == NULL) )
    {
        printf("Memory allocation failure\n");
        exit(-1);
    }

    ifstream file;
    file.open("price.bin", ios::in|ios::binary);
    if (file) {
      file.read(reinterpret_cast<char *>(ts0), nopt*sizeof(tfloat));
      file.close();
    } else {
      std::cout << "Input file not found.\n";
      exit(0);
    }

    file.open("strike.bin", ios::in|ios::binary);
    if (file) {
      file.read(reinterpret_cast<char *>(tx), nopt*sizeof(tfloat));
      file.close();
    } else {
      std::cout << "Input file not found.\n";
      exit(0);
    }

    file.open("t.bin", ios::in|ios::binary);
    if (file) {
      file.read(reinterpret_cast<char *>(tt), nopt*sizeof(tfloat));
      file.close();
    } else {
      std::cout << "Input file not found.\n";
      exit(0);
    }

    for ( i = 0; i < nopt; i++ ){	
      tvcall_compiler[i] = 0.0;
      tvput_compiler[i]  = 0.0;
    }    

    *s0 = ts0;
    *x  = tx;
    *t  = tt;
    *vcall_compiler = tvcall_compiler;
    *vput_compiler  = tvput_compiler;
}

/* Deallocate arrays */
void FreeData( queue* q, tfloat *s0, tfloat *x, tfloat *t,
                   tfloat *vcall_compiler, tfloat *vput_compiler)
{
    /* Free memory */
  free(s0, q->get_context());
  free(x, q->get_context());
  free(t, q->get_context());
  free(vcall_compiler, q->get_context());
  free(vput_compiler, q->get_context());
}
