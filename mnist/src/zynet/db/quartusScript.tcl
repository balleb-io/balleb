
project_new [lindex $argv 0] -overwrite

set_global_assignment -name FAMILY [lindex $argv 1]
set_global_assignment -name DEVICE [lindex $argv 2]
set_global_assignment -name VERILOG_FILE top_sim.v

project_close
