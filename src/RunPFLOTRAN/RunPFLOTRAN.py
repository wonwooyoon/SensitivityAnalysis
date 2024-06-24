
import subprocess

def run_pflotran_main():
    bash_code = """
#!/bin/bash
mkdir -p ./src/RunPFLOTRAN/output

for infile in ./src/RunPFLOTRAN/input/sample_*.in; do
  echo "Running pflotran on $infile..."
  mpirun -n 12 /home/wwy/pflotran/src/pflotran/pflotran -input_prefix "${infile%.*}"
  
  find "${infile%.*}".* ! -name "*.in" -exec mv {} ./src/RunPFLOTRAN/output/ \;

done

echo "All simulations completed and results moved to ./src/RunPFLOTRAN/output/"
"""
    subprocess.run(['bash', '-c', bash_code], check=True)


if __name__ == '__main__':

    run_pflotran_main()
