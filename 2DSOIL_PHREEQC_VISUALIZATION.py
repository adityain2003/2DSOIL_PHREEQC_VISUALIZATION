## AS FILE FOR VISUALIZING 2DSOIL-PHREEQCRM RESULTS

import matplotlib.pyplot as PLT
import numpy as NP
import pandas as PD
import scipy.interpolate
import matplotlib.animation as animation
import os

# FILE = open("TEST_FILE.txt", "r" )
# FIELDS = FILE.read()
# print(FIELDS)
NUM_NODES = 600  # NUMBER OF NODES IN 2DSOIL
X_Y_STEP_SIZE = 0.1   # RESOLUTION OF RESAMPLING GRID
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

Q_ARRAY = FIELDS_PD[["thNew"]].to_numpy()
Q_ARRAY_DATE = NP.zeros(NUM_NODES,dtype=float)

#for J in range(0,NUM_DAYS):

J = 153
#for J in range(0,NUM_DAYS):
for I in range(0,NUM_NODES):
    Q_ARRAY_DATE[I] = Q_ARRAY[I+J*NUM_NODES]
#    os.system("pause")
        

for I in range(0,NUM_NODES):
    print(X_ARRAY[I],Y_ARRAY[I],Q_ARRAY[I])

#X,Y = NP.meshgrid(X_ARRAY,Y_ARRAY)
X_ARRAY_MIN = NP.min(X_ARRAY)
X_ARRAY_MAX = NP.max(X_ARRAY)
Y_ARRAY_MIN = NP.min(Y_ARRAY)
Y_ARRAY_MAX = NP.max(Y_ARRAY)
print("X_ARRAY_MIN","X_ARRAY_MAX","Y_ARRAY_MIN","Y_ARRAY_MAX")
print(X_ARRAY_MIN,X_ARRAY_MAX,Y_ARRAY_MIN,Y_ARRAY_MAX)


FIGURE, AX = PLT.subplots(1,1,sharex=True,sharey=True) #(1,1,sharex=True,sharey=True)
AX.set_aspect('equal')

#Q_FIGURE_TIMESTEP = AX.tripcolor(X_ARRAY.flatten(),Y_ARRAY.flatten(),Q_ARRAY_DATE)

X_GRID = NP.linspace(X_ARRAY_MIN,X_ARRAY_MAX,int((X_ARRAY_MAX-X_ARRAY_MIN)/X_Y_STEP_SIZE))
Y_GRID = NP.linspace(Y_ARRAY_MIN,Y_ARRAY_MAX,int((Y_ARRAY_MAX-Y_ARRAY_MIN)/X_Y_STEP_SIZE))

X_GRID,Y_GRID = NP.meshgrid(X_GRID,Y_GRID, indexing='xy')

X_ARRAY_FLATTENED = X_ARRAY.ravel()
Y_ARRAY_FLATTENED = Y_ARRAY.ravel()

Q_RESAMPLED = scipy.interpolate.griddata((X_ARRAY.ravel(),Y_ARRAY.ravel()),Q_ARRAY_DATE.ravel(),(X_GRID,Y_GRID))
#X_RESAMPLED = NP.mgrid()

Q_FIGURE_TIMESTEP = PLT.imshow(Q_RESAMPLED,
                               cmap='jet', 
                               interpolation='bilinear',    #bilinear   # nearest
                               origin='lower',
                               extent=[X_ARRAY_MIN,X_ARRAY_MAX,Y_ARRAY_MIN,Y_ARRAY_MAX],)

PLT.colorbar()
PLT.show()

#print(UNIQUE_DATES)
print(X_ARRAY)
#print(Y_ARRAY)
#X,Y = NP.meshgrid(X_ARRAY,Y_ARRAY)
#PLT.tripcolor(X_ARRAY,Y_ARRAY,Q_ARRAY)
