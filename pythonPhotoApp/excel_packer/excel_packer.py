import pandas as pd
import os



class ExcelPacker:

    def __init__(self):
        pass

    def pack_to_excel(self, desired_list: list):
        """
            Aktualnie prowizorka w excelu do czasu przygotowania porządnej bazy danych.
        """
        df1 = pd.DataFrame(desired_list,
                           index=[f'row {i+1}' for i in range(len(desired_list))],
                           columns=['data zakupu', 'produkty', 'cena - suma'])
        df1.to_excel("output.xlsx")

        os.startfile("output.xlsx")


