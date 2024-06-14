#!/bin/bash
mkdir -p ./pflotran_output

for infile in ./output/ratio_calculation_*.in; do
  echo "Running pflotran on $infile..."
  mpirun -n 1 /home/wwy/pflotran/src/pflotran/pflotran -input_prefix "${infile%.*}"

done

find ./output -type f -name "ratio_calculation_*" ! -name "*.in" -exec mv {} ./pflotran_output/ \;

echo "All simulations completed and results moved to ./pflotran_output/"