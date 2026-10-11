# Trình mô phỏng QuestaSim
SIM ?= questasim
TOPLEVEL_LANG ?= verilog

# Tệp nguồn Verilog
VERILOG_SOURCES += $(PWD)/project.v

# Tên Module đỉnh (trong project.v) và tên file testbench (test.py)
TOPLEVEL = tt_um_barrel_shifter
MODULE = test

# Tích hợp bộ công cụ Cocotb
include $(shell cocotb-config --makefiles)/Makefile.sim