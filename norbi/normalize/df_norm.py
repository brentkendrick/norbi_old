import pandas as pd
import numpy as np
import peakutils
from scipy import integrate


def df_trunc(df, left_cut, right_cut):

    df_trnc = df.copy()
    filt = ((df_trnc.iloc[:,0]> left_cut) & 
            (df_trnc.iloc[:,0]< right_cut))#assign to variable
    return df_trnc.loc[filt] 

def df_center(df, ctr_indexes):

    # Find maximum peak center X, and Y values for every data column

    x_val = np.asarray(df.iloc[:,0])
    xctrs = []
    yctrs = []

    for i in range(len(df.columns)-1):
        y_val = np.asarray(df.iloc[:,(i+1)])

        ctr_indexes = peakutils.indexes(y_val, thres=.35, min_dist=1)
        xctrs.append(x_val[ctr_indexes][0].tolist())
        yctrs.append(y_val[ctr_indexes][0].tolist())

    RTdelta = (df.iloc[1, 0] - df.iloc[0, 0]) # retention time data interval

    # Shift the x-axis of the data to align to max peak

    for i in range(len(df.columns)-2):
        shft = (int(round((xctrs[i+1]-xctrs[0])/RTdelta)))  #calculate the integer rows to shift data relative to 1st sample
        df.iloc[:,(i+2)]=df.iloc[:,(i+2)].shift(-shft)

    # Fill in ends of data after dataframe shift
    df.ffill(axis = 0, inplace=True) 
    df.bfill(axis = 0, inplace=True) 
    return df

def df_area_norm(df):
    """Normalize to area of 100 to give intuitive feel for peak area%"""
    df.reset_index(drop=True,inplace=True)

    proteins = list(df.columns)[1:]

    for i in proteins:
        dy = integrate.trapz(df[i], df[df.columns[0]]) 
        df[i] = df[i]/abs(dy)*100 #absolute value because decreasing x-values give negative area
    return df    