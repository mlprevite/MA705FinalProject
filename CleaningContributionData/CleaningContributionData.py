# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 17:31:49 2021

@author: Mia
"""
import pandas as pd
import numpy as np
import re
import pyperclip
import geopandas
import matplotlib.pyplot as plt

#CLEANING CONTRIBUTIONS DATA

Contributions = pd.read_csv("/Users/Mia/Documents/Graduate School/MA705/Final Project/CleaningContributionData/Contributions2020.csv")


Contributions['first_name'] = Contributions['Filer Full Name Reverse'].str.split(', ').str[-1]

Contributions['last_name'] = Contributions['Filer Full Name Reverse'].str.split(' ').str[0]

Contributions['last_name'] = Contributions['last_name'].str.replace(',','')

Contributions['Cand_Name'] = Contributions['first_name'] +  " " + Contributions['last_name']

Contributions = Contributions.drop(['Filer Full Name Reverse','first_name','last_name'],axis=1)



#move Columns

def movecol(Contributions, cols_to_move=[], ref_col='', place='After'):
    
    cols = Contributions.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]
    
    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]
    
    return(Contributions[seg1 + seg2 + seg3])


Contributions = movecol(Contributions, 
             cols_to_move=['Filer CPF ID'], 
             ref_col='Record Type ID',
             place='Before')



Contributions = movecol(Contributions, 
             cols_to_move=['Cand_Name'], 
             ref_col='Filer CPF ID',
             place='After')



Contributions.to_csv("/Users/Mia/Documents/Graduate School/MA705/Final Project/FinalDataFrame/Contributions2020Master.csv",index=False)

