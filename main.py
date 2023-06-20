import pandas as pd
import glob
import os
import csv
import re

class Table():
    def __init__(self) -> None:
        file_list = glob.glob("./*1.UNOS/*")
        file_init = max(file_list, key = os.path.getctime)
        self.rows_desc = []
        self.rows_clean = []
        with open(file_init, encoding="utf8") as file_csv:
            reader = csv.reader(file_csv)
            for row in reader:
                self.rows_desc.append(row[7])
                self.rows_clean.append(row[0:6]+row[8:])
        
        self.file_df = pd.DataFrame(data = self.rows_clean[1:], columns = self.rows_clean[0])

    def CleanColumn(self):
        rows_sorted =[]
        for row in self.rows_desc[1:]:
            new_columns = (row.replace("\\n","")).split("\n")
            columns_sorted = {"Opis":"", "Rok dostave":"", "Brend":"", "Materijal":""}
            if len(new_columns)>0:
                columns_sorted["Opis"]=new_columns[0]
                for property in new_columns[1:]:
                    if ":" in property:
                        columns_sorted[property.split(":")[0]] = property.split(":")[1]
                    else:
                        columns_sorted["Opis"]+=property

            if "Dimenzije" in columns_sorted:
                dimensions = re.split("x|X|x|×",columns_sorted["Dimenzije"])
                if len(dimensions)==3:
                    columns_sorted["Visina"] = dimensions[0].split()[0]
                    columns_sorted["Širina"] = dimensions[1].split()[0]
                    columns_sorted["Dubina"] = dimensions[2].split()[0]
                    columns_sorted["Dimenzije"] = ""
                elif len(dimensions)==2:
                    columns_sorted["Visina"] = dimensions[0]
                    columns_sorted["Promjer"] = dimensions[1].split()[0][1:]
                    columns_sorted["Dimenzije"] = ""
            rows_sorted.append(columns_sorted)
        
        for row_sorted in rows_sorted:
            if "Rok isporuke" in row_sorted:
                row_sorted["Rok dostave"] = row_sorted["Rok isporuke"]
                del row_sorted["Rok isporuke"]
        
        df_new_columns = pd.DataFrame.from_dict(rows_sorted)
        df_final = pd.concat([self.file_df, df_new_columns], axis=1)
        df_final_clean = df_final.drop(['Težina (g)', 'Dužina (cm)','Širina (cm)','Visina (cm)'], axis=1)
        df_final_clean.to_excel("./2.ISPIS/ISPIS.xlsx")

            

table = Table()
table.CleanColumn()