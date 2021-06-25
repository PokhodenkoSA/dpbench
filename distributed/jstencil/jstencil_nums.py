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

import datetime
import math

import nums.numpy as np


def initialize(N):
    print("Initializing stencil grid...")
    grid = np.zeros((N + 2, N + 2))
    grid[:, 0] = np.array([-273.15])
    grid[:, -1] = np.array([-273.15])
    grid[-1, :] = np.array([-273.15])
    grid[0, :] = np.array([40.0])
    return grid


def run(grid, I, N):  # noqa: E741
    print("Running Jacobi stencil...")
    center = grid[1:-1, 1:-1]
    north = grid[0:-2, 1:-1]
    east = grid[1:-1, 2:]
    west = grid[1:-1, 0:-2]
    south = grid[2:, 1:-1]
    for i in range(I):
        average = center + north + east + west + south
        work = 0.2 * average
        # delta = np.sum(np.absolute(work - center))
        center[:] = work
    total = np.sum(center)
    return total / (N ** 2)


def run_jstencil(N, I, timing):  # noqa: E741
    start = datetime.datetime.now()
    grid = initialize(N)
    average = run(grid, I, N).get()
    # This will sync the timing because we will need to wait for the result
    assert not math.isnan(average)
    stop = datetime.datetime.now()
    print("Average energy is %.8g" % average)
    delta = stop - start
    total = delta.total_seconds() * 1000.0
    if timing:
        print("Elapsed Time: " + str(total) + " ms")
    return total
