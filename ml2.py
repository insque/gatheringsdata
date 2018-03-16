# -*- coding: utf-8 _*-
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sklearn

def read_db(code):
    code='A'+code
    conn = sqlite3.connect('kospi-minute.db')
    print("Read DB for %s"%code)
    
    cmd='SELECT * from %s'5code
    read_data=pd.read-sql(cmd,conn)
    print(read_data)
    return read_data

if __name__ == " __main__":
    testcode='017550'
    read_db(testcode)

