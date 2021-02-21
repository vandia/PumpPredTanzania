'''
Created on Mar 5, 2017

@author: vandia
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def colunmn_analysis (dataset,path,suffix=None):
    suf=suffix if suffix != None else ""
    rows=dataset.shape[0]
    with open(path+"variables_analysis"+suf+".csv", "w") as ofile:
        ofile.write("column_name, count, percentage_nulls, zeros, type, number_unique_values\n")
        for i in dataset.columns:
            ofile.write(i+', '+str(rows)+', '+'{:.1%}'.format(np.mean(dataset[i].isnull()))+', '
                        +'{:.1%}'.format((rows-np.count_nonzero(dataset[i],axis=0))/float(rows))+', '
                        +str(dataset[i].dtype.name)+", "+str(dataset[i].nunique())+' \n')
    dataset.describe().to_csv(path+"description"+suf+".csv")
        
        
def plot_dataset(dataset):
    plt.scatter(dataset['longitude'], dataset['latitude'], c=dataset['gps_height'])
    

