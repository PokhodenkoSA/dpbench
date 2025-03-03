# Copyright (C) 2014-2015, 2018 Intel Corporation
#
# SPDX-License-Identifier: MIT
#
# ==============================================================================
# Makefile for GNU make

# ==============================================================================
#  Content:
#      Black-Scholes formula example makefile
# ==============================================================================
#
#    Parameters of this makefile:
#    ----------------------------
#
#      TARGET_ARCH= SSE, AVX <default>, AVX2, MIC
#
#      PREC= s (float) <default>, d (double)
#
#      ACC=ha, la, ep <default> : meaning math function accuracy level
# ==============================================================================

# ==============================================================================
# ############## Configure CFLAGS  #############################################
# ==============================================================================
CC          := icpx
QOPT        :=
FQOPT       :=f
EQCOLON     :="="
TARGET      := pairwise_distance

CFLAGS      += -g -O3
CFLAGS      += -fsycl -qopenmp
CFLAGS      += -I./

PREC ?= d
ifeq ($(PREC),d)
else
    CFLAGS += -D__DO_FLOAT__
endif

# ==============================================================================
# ############## Define make rules #############################################
# ==============================================================================

all: pairwise-distance

pairwise-distance: $(TARGET)

comp: $(TARGET)_comp

$(TARGET): data_gen.cpp main.cpp pairwise_distance.cpp
	$(CC) $(CPPFLAGS) $(CFLAGS) $^ -o $(TARGET)

$(TARGET)_comp: data_gen_comp.cpp main.cpp pairwise_distance_comp.cpp
	$(CC) $(CPPFLAGS) $(CFLAGS) $^ -o $(TARGET)_comp

clean:
	rm -rf *.o *.out *.optrpt *.yaml *~ pairwise_distance pairwise_distance_comp

.PHONY: all clean
