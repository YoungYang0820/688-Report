import pandas as pd
import numpy as np
import math

def extract_zip(x):
    '''
    input: string
    output: string
    '''
    if len(x.split(' ')) < 2:
        return None
    return x.split(' ')[1]

def extract_beds(x):
    '''
    input: string
    output: float
    '''
    if len(x.split(' ')) < 2:
        return None
    return float(x.split(' ')[0])

def extract_baths(x):
    '''
    input: string
    output: float
    '''
    if len(x.split(' ')) < 2:
        return None
    return float(x.split(' ')[0])

def extract_square(x):
    '''
    input: string
    output: float
    '''
    if len(x.split(' ')) < 2:
        return None
    return float(x.split(' ')[0])

def extract_zestimate(x):
    '''
    input: string
    output: float
    '''
    if isinstance(x,float):
        return None
    elif x.startswith('('):
        return None
    elif x.endswith('/mo'):
        return None
    try:
        return float(x)
    except:
        return None

def extract_sale(x):
    '''
    input: string
    output: float
    '''
    if isinstance(x,float):
        return None
    else:
        if x.startswith('Price'):
            return None
        if x.startswith('Off'):
            return None
        elif len(x.split(' ')) > 2:
            return float(x.split(' ')[0])
        return float(x)

def extract_longitude(x):
    '''
    input: float64
    output: float
    '''
    return float(x)

def extract_latitude(x):
    '''
    input: float64
    output: float
    '''
    return float(x)

def extract_days(x):
    '''
    input: string
    output: float
    '''
    if isinstance(x,float):
        return None
    elif x.startswith('Less'):
        return float('0')
    return float(x)

def extract_views(x):
    '''
    input: float64
    output: float
    '''
    if math.isnan(x):
        return None
    return float(x)

def extract_saves(x):
    '''
    input: float64
    output: float
    '''
    if math.isnan(x):
        return None
    return float(x)

def extract_last_sold_date(x):
    '''
    input: string
    output: string
    '''
    if isinstance(x,float):
        return None
    month, year = x.split('-')
    if int(year) > 50:
        year = '19' + year
    else:
        year = '20' + year
    if month == 'Jan':
        month = '01'
    elif month == 'Feb':
        month = '02'
    elif month == 'Mar':
        month = '03'
    elif month == 'Apr':
        month = '04'
    elif month == 'May':
        month = '05'
    elif month == 'Jun':
        month = '06'
    elif month == 'Jul':
        month = '07'
    elif month == 'Aug':
        month = '08'
    elif month == 'Sep':
        month = '09'
    elif month == 'Oct':
        month = '10'
    elif month == 'Nov':
        month = '11'
    elif month == 'Dec':
        month = '12'
    return year + month

def extract_last_sold_price(x):
    '''
    input: float64
    output: float
    '''
    if math.isnan(x):
        return None
    return float(x)


""" The following are the features of Features.
    How to convert the type of a dictionary's value?
"""
def extract_type(x):  
    '''
    input: dict
    output: string
    '''
    dictionary = {}
    pairs = x.split(';')

    for pair in pairs:
        key, value = pair.split(':')
        dictionary[key] = value
    if 'Type' not in dictionary.keys():
        return None
    return str(dictionary['Type'])

def extract_year_built(x):
    '''
    input: dict
    output: string
    '''
    dictionary = {}
    pairs = x.split(';')
    for pair in pairs:
        key, value = pair.split(':')
        dictionary[key] = value
    if 'Year Built' not in dictionary.keys():
        return None
    if dictionary['Year Built'] is None or dictionary['Year Built'] == '':
        return None
    if dictionary['Year Built'] == 'No Data':
        return None
    return str(dictionary['Year Built'])

def extract_heating(x):
    '''
    input: dict
    output: string
    '''
    dictionary = {}
    pairs = x.split(';')
    for pair in pairs:
        key, value = pair.split(':')
        dictionary[key] = value
    if 'Heating' not in dictionary.keys():
        return 'No'
    if dictionary['Heating'] is None or dictionary['Heating'] == '':
        return 'No'
    if dictionary['Heating'] == 'No Data':
        return 'No'
    return str(dictionary['Heating'])

def extract_cooling(x):
    '''
    input: dict
    output: string
    '''
    dictionary = {}
    pairs = x.split(';')
    for pair in pairs:
        key, value = pair.split(':')
        dictionary[key] = value
    if 'Cooling' not in dictionary.keys():
        return 'No'
    if dictionary['Cooling'] is None or dictionary['Cooling'] == '':
        return 'No'
    if dictionary['Cooling'] == 'No Data':
        return 'No'
    return dictionary['Cooling']

def extract_parking(x):
    '''
    input: dict
    output: string
    '''
    dictionary = {}
    pairs = x.split(';')
    for pair in pairs:
        key, value = pair.split(':')
        dictionary[key] = value
    if 'Parking' not in dictionary.keys():
        return 'No'
    if dictionary['Parking'] is None or dictionary['Parking'] == '':
        return 'No'
    if dictionary['Parking'] == 'No Data':
        return 'No'
    return dictionary['Parking']

def extract_lot(x):
    '''
    input: dict
    output: string
    '''
    dictionary = {}
    pairs = x.split(';')
    for pair in pairs:
        key, value = pair.split(':')
        dictionary[key] = value
    if 'Lot' not in dictionary.keys():
        return None
    lot = dictionary['Lot']
    if lot is None or lot == '' or lot == 'No data':
        return None
    tmp = lot.split(' ')
    if len(tmp) != 2:
        return None
    if tmp[1] not in ['acres', 'sqft']:
        return None
    if tmp[1] == 'acres':
        tmp[0] = float(tmp[0]) * 43560
    return float(tmp[0])

def extract_pricePerSquare(x):
    '''
    input: dict
    output: float
    '''
    dictionary = {}
    pairs = x.split(';')
    for pair in pairs:
        key, value = pair.split(':')
        dictionary[key] = value
    if 'Price/sqft' not in dictionary.keys():
        return None
    pricePerSquare = dictionary['Price/sqft']
    if pricePerSquare is None or pricePerSquare == '' or pricePerSquare == 'No Data':
        return None
    try:
        pricePerSquare = pricePerSquare.split('$')[1]
        return float(pricePerSquare)
    except:
        return None

def extract_price(x):
    if isinstance(x, float):
        return x
    x = x.strip().split(' ')[0]
    try:
        x = float(x)
    except:
        x = None
    return x

def main():
    for indicator in [True, False]:
        if indicator:
            filename = '../crawler/result/checked_zillow.sold.csv'
        else:
            filename = '../crawler/result/checked_zillow_2018-04-27.csv'
        
        df = pd.read_csv(filename)
        print(df.dtypes)
        new_df = pd.DataFrame()
        
        new_df['zip'] = df['Zip'].apply(lambda x : extract_zip(x))
        new_df['beds'] = df['Beds'].apply(lambda x : extract_beds(x))
        new_df['baths'] = df['Baths'].apply(lambda x : extract_baths(x))
        new_df['square'] = df['Square'].apply(lambda x : extract_square(x))
        new_df['longitude'] = df['Longitude'].apply(lambda x : extract_longitude(x))
        new_df['latitude'] = df['Latitude'].apply(lambda x : extract_latitude(x))
        
        '''
        useless features
        '''
    #    new_df['zestimate'] = df['Zestimate'].apply(lambda x : extract_zestimate(x))
    #    new_df['days'] = df['Days'].apply(lambda x : extract_days(x))
    #    new_df['views'] = df['Views'].apply(lambda x : extract_views(x))
    #    new_df['saves'] = df['Saves'].apply(lambda x : extract_saves(x))
      
        new_df['last_sold_date'] = df['LastSoldDate'].apply(lambda x : extract_last_sold_date(x))
        new_df['last_sold_price'] = df['LastSoldPrice'].apply(lambda x : extract_last_sold_price(x))
        
        # Type,Year Built,Heating,Cooling,Parking,Lot,Price/sqft
        new_df['type'] = df['Feature'].apply(lambda x : extract_type(x))
        new_df['year_built'] = df['Feature'].apply(lambda x : extract_year_built(x))
        new_df['heating'] = df['Feature'].apply(lambda x : extract_heating(x))
        new_df['cooling'] = df['Feature'].apply(lambda x : extract_cooling(x))    
        new_df['parking'] = df['Feature'].apply(lambda x : extract_parking(x))
        new_df['lot'] = df['Feature'].apply(lambda x : extract_lot(x))
        new_df['pricePerSquare'] = df['Feature'].apply(lambda x : extract_pricePerSquare(x))
        
        new_df['label'] = df['Sale'].apply(lambda x: extract_price(x))
        
        print(new_df.dtypes)
        
        if indicator:
            new_df.to_csv('features_train.csv', index=False)
        else:
            new_df.to_csv('features_test.csv', index=False)
    
if __name__ == '__main__':
#    main()
    pass