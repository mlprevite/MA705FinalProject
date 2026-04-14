# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 17:52:24 2021

@author: Mia
"""

"""
Candidate data was pre cleaned in excel. Empty rows were deleted in excel.
Candidates who had "Statewide" in the column "Office Type Sought" had their 
office title from the column "District Name Sought" as this was the only office
that had the office title within the "District Name Column". Because these offices
were statewide offices corisponding to no districts, the state name, Massachusetts,
was put in place of the district name in the "District Name Sought" column. So for every
statewide office, the name of the office is included within the "Office Type Sought" column.


"""

import pandas as pd
import numpy as np
import re
import pyperclip
import geopandas
import matplotlib.pyplot as plt






#CLEANING CANDIDATE DATA

#load data
Candidates = pd.read_csv("/Users/Mia/Documents/Graduate School/MA705/Final Project/CleaningCandidateData/candidates.csv")

Candidates['Cand_Name'] = Candidates['Candidate First Name'] +  " " + Candidates['Candidate Last Name']

Candidates = Candidates.drop(['Candidate First Name','Candidate Last Name'],axis=1)


#move Columns

def movecol(Candidates, cols_to_move=[], ref_col='', place='After'):
    
    cols = Candidates.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]
    
    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]
    
    return(Candidates[seg1 + seg2 + seg3])


Candidates = movecol(Candidates, 
             cols_to_move=['Cand_Name'], 
             ref_col='Is_Candidate_Only',
             place='After')


Candidates.to_csv("/Users/Mia/Documents/Graduate School/MA705/Final Project/FinalDataFrame/CandidatesMaster.csv",index=False)

