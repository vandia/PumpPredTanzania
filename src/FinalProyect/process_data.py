'''
Created on Mar 13, 2017

@author: vandia
'''

import numpy as np
import pandas as pd
import io_utilities as ut
import cleaning_utilities as cl
import analysis_utilities as ad
import os.path as osp
from numpy import str
from sympy.physics.units import length

def process_pump_dataset(dataset, tr_dataset=None, suffix=None):  

    dataset=cl.tolower(dataset);
    
    dataset = cl.drop_columns(dataset, ["amount_tsh","num_private", "recorded_by", "wpt_name", "scheme_name"])
    
    if tr_dataset is None:
        dataset = cl.clean_data(dataset)

    construction_year=[["funder","installer"],["basin"]];
    location=[['subvillage'],['ward','lga'],['district_code','region_code']];
    population=[['subvillage'],['ward'],['lga'],['district_code','region_code'],['region']];
    

    dataset = cl.fill_categorical_values(dataset, {'funder':['installer'],
                                                   'installer':['funder'],
                                                   'scheme_management':['management','management_group']})
    for i in construction_year:
        dataset = cl.fill_zero_values(dataset,{'construction_year':i})
    
    for i in population:
        dataset = cl.fill_zero_values(dataset,{'population':i})
    
    for i in location:
        dataset = cl.fill_zero_values(dataset,{'gps_height':i,'longitude':i})

    dataset = cl.fill_boolean_columns(dataset, ["public_meeting","permit"], False)
    dataset = cl.drop_columns(dataset, ["funder","installer", "ward","subvillage"])
    dataset.insert(0,"pump_id",dataset.index.values)

    type_list = {"pump_id":str,"public_meeting":np.bool_,"permit":np.bool_,'scheme_management':'category',
                "construction_year":'category',"region":'category',"region_code":'category',"district_code":'category',
                "extraction_type":'category',"extraction_type_group":'category', "extraction_type_class":'category',
                "management":'category',"management_group":'category', "payment":'category', "payment_type":'category',
                "water_quality":'category', "quality_group":'category', "quantity":'category',
                "quantity_group":'category', "source":'category', "source_type":'category',
                "source_class":'category', "waterpoint_type":'category', "waterpoint_type_group":'category',
                "basin":'category', "lga":'category',"status_group":'category'}

    dataset = cl.modify_column_types(dataset, type_list)
    ut.generate_arff("../../data_out/pumps"+suffix+".arff","pumps",dataset, tr_dataset)
    ad.colunmn_analysis(dataset,"../../data_out/",suffix=suffix+'_clean')
    ut.save_csv(dataset, '../../data_in/pumps'+suffix+'_clean.csv')
    return dataset


def main():
    #===========================================================================
    # Tranining data cleaning
    #===========================================================================
    fname="../../data_in/pumps_training.csv"
    if osp.isfile(fname):
        dataset = ut.load(fname, "id", date_cols=["date_recorded"]) 
    else:
        dataset = ut.load_and_join("../../data_in/training_data.csv", "../../data_in/training_labels.csv", "id", date_cols1=["date_recorded"])
        ut.save_csv(dataset, fname)
    dataset=process_pump_dataset(dataset,suffix="_training")

    
    #===========================================================================
    # Test data cleaning
    #===========================================================================
    fname="../../data_in/pumps_test.csv"
    labels= "../../data_in/pumps_test_labels.csv"
    
    if osp.isfile(labels):
        dataset_t = ut.load_and_join(fname, labels, "id", date_cols1=["date_recorded"])
    else:
        dataset_t = ut.load(fname, "id", date_cols=["date_recorded"])
        dataset_t = dataset.assign(status_group=pd.Series(np.random.choice(["functional","non functional","functional needs repair"]),
                                          index=dataset.index).values)
     
    process_pump_dataset(dataset_t, tr_dataset=dataset, suffix="_test")
    

if __name__ == '__main__':
    main()