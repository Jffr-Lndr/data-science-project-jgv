import pandas as pd
import numpy as np
from datetime import datetime
from re import match
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://project_dat_5623:STdvleCgo7H9jXH7osWL@project-dat-5623.postgresql.a.osc-fr1.scalingo-dbs.com:32019/project_dat_5623?sslmode=prefer"
engine = create_engine(DATABASE_URL, connect_args={'sslmode': "allow"})


def availability_parse(string):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if string == 'Ready To Move' or string == 'Immediate Possession':
        return datetime(2023, 1, 1)
    else:
        return datetime(2023, months.index(string[3:])+1, int(string[0:2]))


def size_parse(string):
    temp = str(string).split(' ')
    if len(temp) > 1:
        if temp[1] == 'Bedroom':
            return int(temp[0])+1
        elif temp[1] == 'RK':
            return int(temp[0])
        elif temp[1] == 'BHK':
            return int(temp[0])+1
    else:
        return np.nan


def total_sqft_parse(string):
    if ' - ' in string:
        temp = string.split(' ')
        return (float(temp[0]) + float(temp[2]))/2
    elif match('^[\.0-9]*$', string):
        return float(string)
    else:
        return np.nan


data_frame = pd.read_csv("../data/dataset.csv")
cols = ['area_type', 'availability', 'location',
        'size', 'total_sqft', 'bath', 'balcony', 'price']
data_frame = data_frame[cols]

data_frame['availability'] = [availability_parse(
    x) for x in data_frame['availability']]

data_frame['size'] = [size_parse(x) for x in data_frame['size']]

data_frame['total_sqft'] = [total_sqft_parse(
    x) for x in data_frame['total_sqft']]

data_frame.to_sql('data_cleaned', engine, if_exists='replace')

print(pd.read_sql('data_cleaned', engine))
