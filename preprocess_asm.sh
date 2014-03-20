#!/bin/bash

# This runs the pru code through the c preprocessor like the makefile
input=$1
output=$2

CPP=${CPP-cpp}

$CPP - < "$input" | sed -e 's/^#.*//' -e 's/;/\n/g' > "${output}"
