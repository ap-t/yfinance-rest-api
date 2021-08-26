import pandas as pd
import datetime
from bson import json_util

def _instance_to_str(index):
    if isinstance(index, datetime.datetime):
        return index.isoformat()
    
    return index

def series_to_list_with_index(series):
    out_list = []

    if not(isinstance(series, pd.Series)): return out_list

    s_dict = series.to_dict()

    for key in s_dict:
        new_dict = {}
        index_key = type(key).__name__.lower()
        new_dict[index_key] = _instance_to_str(key)
        new_dict['value'] = s_dict[key]
        out_list.append(new_dict)
    
    return out_list

def dataframe_to_list_with_index(df):
    out_list = []

    if not(isinstance(df, pd.DataFrame)): return out_list

    for index, row in df.iterrows():
        rdict = row.to_dict()
        index_key = type(index).__name__.lower()
        rdict[index_key] = _instance_to_str(index)
        out_list.append(rdict)
    
    return out_list

def to_camel_case(string):
    out = string

    if not(isinstance(out, str)): return out

    # Make lower case
    out = out.lower()

    # Capitlize first letter of each pieces except the first one
    pieces = out.split(' ')
    out = pieces[0] + ''.join(x.title() for x in pieces[1:])

    return out

def lookup_fn(df, key_row, key_col):
    try:
        return df.iloc[key_row][key_col]
    except IndexError:
        return 0

def parse_json(data):
    return json_util.dumps(data, default=json_util.default)


