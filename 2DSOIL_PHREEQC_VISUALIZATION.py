## AS FILE FOR VISUALIZING 2DSOIL-PHREEQCRM RESULTS

import matplotlib.pyplot as PLT
import numpy as NP
import pandas as PD
import os

# FILE = open("TEST_FILE.txt", "r" )
# FIELDS = FILE.read()
# print(FIELDS)
NUM_NODES = 600  # NUMBER OF NODES IN 2DSOIL
FIELDS_PD = PD.read_csv('TEST_FILE.txt',sep = ' *, *')
print("READ FROM PANDAS")
print(FIELDS_PD)
print("COLUMNS FROM PANDAS")
print(FIELDS_PD.columns)
COLUMNS_FIELDS_PD = FIELDS_PD.columns
COLUMNS_FIELDS_PD = COLUMNS_FIELDS_PD
#ARRAY_FIELDS = FIELDS.to_numpy
print("ARRAY FROM PANDAS")
ARRAY_FIELDS = FIELDS_PD.to_numpy()
print(ARRAY_FIELDS)
print("'DATE' COLUMN IN ARRAY")
DATE_ARRAY = FIELDS_PD[["Date"]].to_numpy()
UNIQUE_DATES = NP.unique(DATE_ARRAY)
NUM_DAYS = UNIQUE_DATES.size
print("NUM_DAYS =", NUM_DAYS)

X_ARRAY = (FIELDS_PD[["X"]].to_numpy())[0:NUM_NODES]
Y_ARRAY = (FIELDS_PD[["Y"]].to_numpy())[0:NUM_NODES]

Q_ARRAY = FIELDS_PD[["Q"]].to_numpy()
Q_ARRAY_DATE = NP.zeros(NUM_NODES,dtype=float)

#for J in range(0,NUM_DAYS):

J = 0
for J in range(0,NUM_DAYS):
    for I in range(0,NUM_NODES):
        Q_ARRAY_DATE[I] = Q_ARRAY[I+J*NUM_NODES]
        os.system("pause")
        

for I in range(0,NUM_NODES):
    print(X_ARRAY[I],Y_ARRAY[I],Q_ARRAY[1])



#print(UNIQUE_DATES)
print(X_ARRAY)
#print(Y_ARRAY)
#X,Y = NP.meshgrid(X_ARRAY,Y_ARRAY)
#PLT.tripcolor(X_ARRAY,Y_ARRAY,Q_ARRAY)
