import pandas as pd

class TargetValueAnalysis:

    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)
        self.data = self.data[['Porosity', 'Volume [m^3]', 'Total UO2++ [m]', 'Total Sorbed UO2++ [mol/m^3]', 'Uraninite VF [m^3 mnrl/m^3 bulk]', 'Material ID']]
        
    def calculate_aqueous(self):
        material_1 = self.data[self.data['Material ID'] == 1]
        self.aqueous_granite = (material_1['Total UO2++ [m]'] * material_1['Volume [m^3]'] * material_1['Porosity']).sum()
        
        material_2 = self.data[self.data['Material ID'] == 2]
        self.aqueous_bentonite = (material_2['Total UO2++ [m]'] * material_2['Volume [m^3]'] * material_2['Porosity']).sum()
    
    def calculate_adsorbed(self):
        material_2 = self.data[self.data['Material ID'] == 2]
        self.adsorbed = (material_2['Total Sorbed UO2++ [mol/m^3]'] * material_2['Volume [m^3]']).sum()
    
    def calculate_uraninite(self):
        material_3 = self.data[self.data['Material ID'] == 3]
        self.dissolved = ((0.05 - material_3['Uraninite VF [m^3 mnrl/m^3 bulk]']) * material_3['Volume [m^3]'] / (24.62 * 10**6)).sum()

    def save_target_values(self, file_path):
        target_values = pd.DataFrame({'Aqueous UO2++ in Granite': [self.aqueous_granite], 'Aqueous UO2++ in Bentonite': [self.aqueous_bentonite], 'Adsorbed UO2++ in Bentonite': [self.adsorbed], 'Dissolved Uraninite in Bentonite': [self.dissolved]})
        target_values.to_excel(file_path, index=False)


if __name__ == '__main__':
    tva = TargetValueAnalysis('/home/wwy/pflotran_sensitivity_analysis/SensitivityAnalysis/src/TargetValueAnalysis/output/mesh_centered_data.csv')
    tva.calculate_aqueous()
    tva.calculate_adsorbed()
    tva.calculate_uraninite()
    print(tva.aqueous_granite)
    print(tva.aqueous_bentonite)
    print(tva.adsorbed)
    print(tva.dissolved)
    tva.save_target_values('/home/wwy/pflotran_sensitivity_analysis/SensitivityAnalysis/src/TargetValueAnalysis/output/target_values.xlsx')

