import numpy as np
import csv
import subprocess
import glob
from concurrent.futures import ProcessPoolExecutor



class RatioEquilibrium:

    def __init__(self, ratio_dir, default_script_dir):
        self.ratio_dir = ratio_dir
        self.default_script_dir = default_script_dir
        self.ratios = None

    def write_script(self):

        with open(f'{self.default_script_dir}', 'r') as file:
            lines = file.readlines()

        ratio_1_target = None
        ratio_2_target = None

        for i, line in enumerate(lines):

            if 'MATERIAL_PROPERTY SOIL1' in line:
                ratio_1_target = i+2
            if 'MATERIAL_PROPERTY SOIL2' in line:
                ratio_2_target = i+2

        for i in range(np.shape(self.ratios)[0]):

            if ratio_1_target is not None:
                lines[ratio_1_target] = f'POROSITY {self.ratios[i, 0]}\n'
            if ratio_2_target is not None:
                lines[ratio_2_target] = f'POROSITY {self.ratios[i, 1]}\n'

            with open(f'./output/ratio_calculation_{i}.in', 'w') as file:
                file.writelines(lines)

    def read_ratio(self):

        with open(f'{self.ratio_dir}', 'r') as csvfile:
            data = csv.reader(csvfile)
            data = np.array([row for row in data], dtype=float)

        self.ratios = np.zeros([data.shape[0], 2], float)

        self.ratios[:, 0] = data[:, -1]
        self.ratios[:, 1] = 1 - data[:, -1]

    def run_simulation(self, infile):
        subprocess.run(['mpirun', '-n', '1', '$PFLOTRAN_DIR/src/pflotran/pflotran', '-input_prefix', f"{infile[:-3]}"], check=True)
        subprocess.run(['mv', f"{infile[:-3]}.*", './pflotran_output/'], check=True)

    def run_pflotran(self, num_procs=4):
        input_files = glob.glob('./output/ratio_calculation_*.in')

        with ProcessPoolExecutor(max_workers=num_procs) as executor:
            results = list(executor.map(self.run_simulation, input_files))

        print("All simulations completed and results moved to ./pflotran_output/")


if __name__ == '__main__':

    ratio_dir = '../RandomSampling/output/lhs_sampled_data.csv'
    default_script_dir = './input/PFLOTRAN_mixing.in'

    ratio_calculation = RatioEquilibrium(ratio_dir, default_script_dir)

    ratio_calculation.read_ratio()
    ratio_calculation.write_script()
    ratio_calculation.run_pflotran()

