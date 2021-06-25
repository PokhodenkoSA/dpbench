#!/usr/bin/env python

# Copyright 2021 NVIDIA Corporation
# Copyright 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import argparse
from benchmark import run_benchmark

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--intercept",
        dest="B",
        action="store_true",
        help="include an intercept in the calculation",
    )
    parser.add_argument(
        "-f",
        "--features",
        type=int,
        default=32,
        dest="F",
        help="number of features for each input data point",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=1000,
        dest="I",
        help="number of iterations to run the algorithm for",
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=10,
        dest="N",
        help="number of elements in the data set in thousands",
    )
    parser.add_argument(
        "-p",
        "--precision",
        type=int,
        default=32,
        dest="P",
        help="precision of the computation in bits",
    )
    parser.add_argument(
        "-s",
        "--sample",
        type=int,
        default=100,
        dest="S",
        help="number of iterations between sampling the log likelihood",
    )
    parser.add_argument(
        "-b",
        "--benchmark",
        type=int,
        default=1,
        dest="benchmark",
        help="number of times to benchmark this application (default 1 - "
        "normal execution)",
    )
    parser.add_argument(
        "-u",
        "--use",
        default='numpy',
        choices=['numpy', 'dask', 'ramba', 'torch', 'heat', 'nums',],
        dest="use",
        help="use given numpy implementation",
    )
    args = parser.parse_args()

    if args.use == 'numpy':
        from linreg.linreg_numpy import run_linear_regression
    elif args.use == 'dask':
        from linreg.linreg_dask import run_linear_regression
    elif args.use == 'ramba':
        from linreg.linreg_ramba import run_linear_regression
    elif args.use == 'torch':
        from linreg.linreg_torch import run_linear_regression
    elif args.use == 'heat':
        from linreg.linreg_heat import run_linear_regression
    elif args.use == 'nums':
        from linreg.linreg_nums import run_linear_regression
    
    run_benchmark(
        run_linear_regression,
        args.benchmark,
        f"LINREG({args.P})",
        (args.N, args.F, args.P, args.I, args.S, args.B),
    )
