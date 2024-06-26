import pandas as pd

class TargetValueAnalysis:

    def __init__(self):
        pass

    # load a dataframe from ./src/RunPFLOTRAN/TargetValueAnalysis/output/mesh_centered_data.csv
    
    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)
        return self.data
    
    # load_data 함수에서 읽어온 데이터프레임의 컬럼명 중 X [m], Y [m], Z [m], Total UO2++ [M], Total Sorbed UO2++ [mol/m^3], Material ID를 따로 저장

    def set_columns(self):
        self.data = self.data[self.data['Material ID'] != 3]
        self.X = self.data['X [m]']
        self.Y = self.data['Y [m]']
        self.Z = self.data['Z [m]']
        self.Total_UO2 = self.data['Total UO2++ [M]']
        self.Total_Sorbed_UO2 = self.data['Total Sorbed UO2++ [mol/m^3]']
        self.Material_ID = self.data['Material ID']
        return self.X, self.Y, self.Z, self.Total_UO2, self.Total_Sorbed_UO2, self.Material_ID
    
    



 


        
        

        


    
