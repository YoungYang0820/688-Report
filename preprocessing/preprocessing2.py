#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 16:53:30 2018
"""

import pandas as pd 

def standardize(data):
    return (data - data.mean()) / (data.max() - data.min())

if __name__ == '__main__':
    '''
    categorial features need ont hot encoding 
    numerical features need normalization 
    '''
    for indicator in [True, False]:
        if indicator:
            filename = 'features_train.csv'
        else:
            filename = 'features_test.csv'
        df = pd.read_csv(filename)
        
        '''
        categorial features
        '''
        # last_sold_date
    #    one_hot = pd.get_dummies(df['last_sold_date'])
    #    df = df.drop('last_sold_date', axis=1)
    #    df = df.join(one_hot)
        
        # heating
        one_hot = pd.get_dummies(df['heating'])
        df = df.drop('heating', axis=1)
        df = df.join(one_hot)
        
        # cooling
        one_hot = pd.get_dummies(df['cooling'])
        df = df.drop('cooling', axis=1)
        df = df.join(one_hot, rsuffix='_cooling')
        
        # parking
        one_hot = pd.get_dummies(df['parking'])
        df = df.drop('parking', axis=1)
        df = df.join(one_hot, rsuffix='_parking')
        
        # type
        one_hot = pd.get_dummies(df['type'])
        df = df.drop('type', axis=1)
        df = df.join(one_hot, rsuffix='_type')
        
        '''
        numerical features
        '''    
        # label (price)
        labels = standardize(df['label'])
        df = df.drop('label', axis=1)
        df = df.join(labels)
        
        # last sold price
        sold_price = standardize(df['last_sold_price'])
        df = df.drop('last_sold_price', axis=1)
        df = df.join(sold_price)
        
        # price per square
        df.pricePerSquare = df.label / df.lot
        sold_price = standardize(df['pricePerSquare'])
        df = df.drop('pricePerSquare', axis=1)
        df = df.join(sold_price)
        
        '''
        fill nan 
        '''
    #    df['beds'].fillna(df['beds'].mean(),inplace = True)
    #    df['baths'].fillna(df['baths'].mean(),inplace = True)
    #    df['square'].fillna(df['square'].mean(),inplace = True)
    #    df['longitude'].fillna(df['longitude'].mean(),inplace = True)
    #    df['latitude'].fillna(df['latitude'].mean(),inplace = True)
    #    df['last_sold_price'].fillna(df['last_sold_price'].mean(),inplace = True)
    #    df['lot'].fillna(df['lot'].mean(),inplace = True)
    #    df['pricePerSquare'].fillna(df['pricePerSquare'].mean(),inplace = True)
    
        df = df.dropna(axis=0,how='any')
        print(len(df))
        
        if indicator:
            df.to_csv('features_train_model.csv', index=False)
        else:
            df.to_csv('features_test_model.csv', index=False)
    
    