# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 17:45:33 2021

@author: Mia
"""

import pandas as pd
import numpy as np
import datetime
import pyperclip
import geopandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#load data
Contributions = pd.read_csv("/Users/Mia/Documents/Graduate School/MA705/Final Project/FinalDataFrame/Contributions2020Master.csv",index_col=0)

Candidates = pd.read_csv("/Users/Mia/Documents/Graduate School/MA705/Final Project/FinalDataFrame/CandidatesMaster.csv",index_col=0)


#create dataframe with only ID Name and office sought

CandidatesOffice = Candidates[['Cand_Name','Office Type Sought','District Name Sought','Party Affiliation']]

Contributions_Cand = Contributions[['Cand_Name','Date','Amount']]

#merge
ContributionsCand = pd.merge(CandidatesOffice, Contributions_Cand,left_index=True, right_index=True)

ContributionsCand['Cand_Name'] = ContributionsCand['Cand_Name_x']

#drop name
ContributionsCand = ContributionsCand.drop(['Cand_Name_y','Cand_Name_x'],axis=1)

#move Columns

def movecol(ContributionsCand, cols_to_move=[], ref_col='', place='After'):
    
    cols = ContributionsCand.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]
    
    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]
    
    return(ContributionsCand[seg1 + seg2 + seg3])


ContributionsCand = movecol(ContributionsCand, 
             cols_to_move=['Cand_Name'], 
             ref_col='Office Type Sought',
             place='Before')


#insert index
ContributionsCand.reset_index(level=0, inplace=True)

#drop id
ContributionsCand = ContributionsCand.drop(['index'],axis=1)

#save dataframe
ContributionsCand.to_pickle("/Users/Mia/Documents/Graduate School/MA705/Final Project/Dashboard/ContributionsCand.pkl")


