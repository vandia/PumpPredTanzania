'''
Created on Mar 13, 2017

@author: vandia
'''

import numpy as np
import pandas as pd
import io_utilities as ut
import analysis_utilities as ad
import os.path as osp

def main():
    fname="../../data_in/pumps_training.csv"
    if osp.isfile(fname):
        dataset = ut.load(fname, "id", date_cols=["date_recorded"]) 
    else:
        dataset = ut.load_and_join("../../data_in/training_data.csv", "../../data_in/training_labels.csv", "id",
                                    date_cols1=["date_recorded"])
        ut.save_csv(dataset, fname)
    
    ad.colunmn_analysis(dataset,"../../data_out/","_training")
    
    
    #===========================================================================
    # Test data analysis
    #===========================================================================
    fname="../../data_in/pumps_test.csv"
    dataset_t = ut.load(fname, "id", date_cols=["date_recorded"]) 
    ad.colunmn_analysis(dataset_t,"../../data_out/","_test")
    

if __name__ == '__main__':
    main()