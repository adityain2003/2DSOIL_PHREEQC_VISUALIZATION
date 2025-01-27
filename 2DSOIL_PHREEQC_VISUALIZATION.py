## AS FILE FOR VISUALIZING 2DSOIL-PHREEQCRM RESULTS

import matplotlib.pyplot as PLT
import numpy as NP
import pandas as PD
import scipy.interpolate
import matplotlib.animation as animation
import ffmpeg
from IPython.display import clear_output, display
from matplotlib import cm
from matplotlib.animation import PillowWriter
import matplotlib.cbook as cbook
import matplotlib.colors as COLORS
import time
import os

# FILE = open("TEST_FILE.txt", "r" )
# FIELDS = FILE.read()
# print(FIELDS)
NUM_NODES = 670  # NUMBER OF NODES IN 2DSOIL
X_Y_STEP_SIZE = 0.1   # RESOLUTION OF RESAMPLING GRID
FIELDS_PD = PD.read_csv('INPUT.csv',sep = ' *, *')
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
DATE_ARRAY = FIELDS_PD.iloc[:, 1].to_numpy()
UNIQUE_DATES = NP.unique(DATE_ARRAY)
NUM_DAYS = UNIQUE_DATES.size
print("NUM_DAYS =", NUM_DAYS)

X_ARRAY = (FIELDS_PD[["X"]].to_numpy())[0:NUM_NODES]
Y_ARRAY = (FIELDS_PD[["Y"]].to_numpy())[0:NUM_NODES]   

#X,Y = NP.meshgrid(X_ARRAY,Y_ARRAY)
X_ARRAY_MIN = NP.min(X_ARRAY)
X_ARRAY_MAX = NP.max(X_ARRAY)
Y_ARRAY_MIN = NP.min(Y_ARRAY)
Y_ARRAY_MAX = NP.max(Y_ARRAY)

#print("X_ARRAY_MIN","X_ARRAY_MAX","Y_ARRAY_MIN","Y_ARRAY_MAX")
#print(X_ARRAY_MIN,X_ARRAY_MAX,Y_ARRAY_MIN,Y_ARRAY_MAX)

X_GRID = NP.linspace(X_ARRAY_MIN,X_ARRAY_MAX,int((X_ARRAY_MAX-X_ARRAY_MIN)/X_Y_STEP_SIZE))
Y_GRID = NP.linspace(Y_ARRAY_MIN,Y_ARRAY_MAX,int((Y_ARRAY_MAX-Y_ARRAY_MIN)/X_Y_STEP_SIZE))

X_GRID,Y_GRID = NP.meshgrid(X_GRID,Y_GRID, indexing='xy')

X_ARRAY_FLATTENED = X_ARRAY.ravel()
Y_ARRAY_FLATTENED = Y_ARRAY.ravel()


#####################################
####    ANIMATION AND PLOTTING  #####
#####################################
FIGURE, AXIS_ARRAY = PLT.subplots(1,3, figsize = (9,6)) #(1,1,sharex=True,sharey=True)
#PLT.tight_layout()
PLT.subplots_adjust(hspace=0.2)
#AXIS_ARRAY[0].set_aspect('equal')

THETA_ARRAY = FIELDS_PD[["A_CONC"]].to_numpy()
HNEW_ARRAY = FIELDS_PD[["B_CONC"]].to_numpy()
C_CONC_ARRAY = FIELDS_PD[["C_CONC"]].to_numpy()

THETA_ARRAY_MIN = NP.min(THETA_ARRAY)
THETA_ARRAY_MAX = NP.max(THETA_ARRAY)

HNEW_ARRAY_MIN = NP.min(HNEW_ARRAY)
HNEW_ARRAY_MAX = NP.max(HNEW_ARRAY)

C_CONC_ARRAY_MIN = NP.min(C_CONC_ARRAY)
C_CONC_ARRAY_MAX = NP.max(C_CONC_ARRAY)

IMAGE_COLLECTION = []

for I in range(0,NUM_NODES):
    print(X_ARRAY[I],Y_ARRAY[I],THETA_ARRAY[I],HNEW_ARRAY[I],C_CONC_ARRAY[I])

THETA_ARRAY_TIMESTEP = NP.zeros(NUM_NODES,dtype=float)  
HNEW_ARRAY_TIMESTEP = NP.zeros(NUM_NODES,dtype=float)
C_CONC_ARRAY_TIMESTEP = NP.zeros(NUM_NODES,dtype=float)

FIGURE, AXIS_ARRAY = PLT.subplots(1,3, figsize = (9,6)) #(1,1,sharex=True,sharey=True)
PLT.subplots_adjust(hspace=0.2)

J = 0
for I in range(0,NUM_NODES):
    THETA_ARRAY_TIMESTEP[I] = THETA_ARRAY[I+J*NUM_NODES]
    HNEW_ARRAY_TIMESTEP[I] = HNEW_ARRAY[I+J*NUM_NODES]
    C_CONC_ARRAY_TIMESTEP[I] = C_CONC_ARRAY[I+J*NUM_NODES]

THETA_RESAMPLED = scipy.interpolate.griddata((X_ARRAY.ravel(),Y_ARRAY.ravel()),THETA_ARRAY_TIMESTEP.ravel(),(X_GRID,Y_GRID))
HNEW_RESAMPLED = scipy.interpolate.griddata((X_ARRAY.ravel(),Y_ARRAY.ravel()),HNEW_ARRAY_TIMESTEP.ravel(),(X_GRID,Y_GRID))
C_CONC_ARRAY_RESAMPLED = scipy.interpolate.griddata((X_ARRAY.ravel(),Y_ARRAY.ravel()),C_CONC_ARRAY_TIMESTEP.ravel(),(X_GRID,Y_GRID))

THETA_FIGURE_TIMESTEP = AXIS_ARRAY[0].imshow(THETA_RESAMPLED, #animated = True,
                            cmap='jet', 
                            interpolation='bilinear',    #bilinear   # nearest
                            origin='lower',
                            norm = COLORS.Normalize(vmin=THETA_ARRAY_MIN, vmax=THETA_ARRAY_MAX),
#                            vmin = vmin,
#                            vmax = vmax,
                            extent = [X_ARRAY_MIN,X_ARRAY_MAX,Y_ARRAY_MIN,Y_ARRAY_MAX])
AXIS_ARRAY[0].set_title('A')

HNEW_FIGURE_TIMESTEP = AXIS_ARRAY[1].imshow(HNEW_RESAMPLED, #animated = True,
                            cmap='jet', 
                            interpolation='bilinear',    #bilinear   # nearest
                            origin='lower',
                            norm = COLORS.Normalize(vmin = HNEW_ARRAY_MIN ,vmax = HNEW_ARRAY_MAX),
                            #vmin=HNEW_ARRAY_TIMESTEP.max(), 
                            #vmax=HNEW_ARRAY_TIMESTEP.min(),
                            extent = [X_ARRAY_MIN,X_ARRAY_MAX,Y_ARRAY_MIN,Y_ARRAY_MAX])
AXIS_ARRAY[1].set_title('B')


C_CONC_FIGURE_TIMESTEP = AXIS_ARRAY[2].imshow(C_CONC_ARRAY_RESAMPLED, #animated = True,
                            cmap='jet', 
                            interpolation='bilinear',    #bilinear   # nearest
                            origin='lower',
                            norm = COLORS.Normalize(vmin = C_CONC_ARRAY_MIN ,vmax = C_CONC_ARRAY_MAX),
                            #vmin=HNEW_ARRAY_TIMESTEP.max(), 
                            #vmax=HNEW_ARRAY_TIMESTEP.min(),
                            extent = [X_ARRAY_MIN,X_ARRAY_MAX,Y_ARRAY_MIN,Y_ARRAY_MAX])
AXIS_ARRAY[2].set_title('C')


PLT.colorbar(THETA_FIGURE_TIMESTEP,ax=AXIS_ARRAY[0], boundaries = NP.linspace(THETA_ARRAY_MIN,THETA_ARRAY_MAX,6))    # EDITED THE LOWER LIMIT
PLT.colorbar(HNEW_FIGURE_TIMESTEP,ax=AXIS_ARRAY[1], boundaries = NP.linspace(HNEW_ARRAY_MIN,HNEW_ARRAY_MAX,6))
PLT.colorbar(C_CONC_FIGURE_TIMESTEP,ax=AXIS_ARRAY[2], boundaries = NP.linspace(C_CONC_ARRAY_MIN,C_CONC_ARRAY_MAX,6))


def DATE_SEQUENCE(J):

    FIGURE.suptitle('Concentration of Species on day '+str(J))
    #FIGURE.suptitle('Concentration of Species on day    '+str(UNIQUE_DATES[J]))

    for I in range(0,NUM_NODES):
        THETA_ARRAY_TIMESTEP[I] = THETA_ARRAY[I+J*NUM_NODES]
        HNEW_ARRAY_TIMESTEP[I] = HNEW_ARRAY[I+J*NUM_NODES]
        C_CONC_ARRAY_TIMESTEP[I] = C_CONC_ARRAY[I+J*NUM_NODES]
    #    os.system("pause")


    THETA_RESAMPLED = scipy.interpolate.griddata((X_ARRAY.ravel(),Y_ARRAY.ravel()),THETA_ARRAY_TIMESTEP.ravel(),(X_GRID,Y_GRID))
    HNEW_RESAMPLED = scipy.interpolate.griddata((X_ARRAY.ravel(),Y_ARRAY.ravel()),HNEW_ARRAY_TIMESTEP.ravel(),(X_GRID,Y_GRID))
    C_CONC_ARRAY_RESAMPLED = scipy.interpolate.griddata((X_ARRAY.ravel(),Y_ARRAY.ravel()),C_CONC_ARRAY_TIMESTEP.ravel(),(X_GRID,Y_GRID))

    THETA_FIGURE_TIMESTEP.set_array(THETA_RESAMPLED)
    HNEW_FIGURE_TIMESTEP.set_array(HNEW_RESAMPLED)
    C_CONC_FIGURE_TIMESTEP.set_array(C_CONC_ARRAY_RESAMPLED)

ANIMATION = animation.FuncAnimation(FIGURE, DATE_SEQUENCE, frames=range(0,NUM_DAYS),repeat=False)

PLT.show(block = False)
#ANIMATION.save(filename="Animation_1.mpeg", writer=animation.FFMpegWriter())
ANIMATION.save("ANIMATION_AK.GIF", dpi=600, writer=PillowWriter(fps=2))
PLT.close()
#PLT.ioff()
#PLT.show()
#

#print(UNIQUE_DATES)
print(X_ARRAY)
#print(Y_ARRAY)
#X,Y = NP.meshgrid(X_ARRAY,Y_ARRAY)
#PLT.tripcolor(X_ARRAY,Y_ARRAY,THETA_ARRAY)