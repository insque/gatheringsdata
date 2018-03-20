# -*- coding: utf-8 _*-
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sklearn

print("start...")

def read_db(code):
    code='A'+code
    conn = sqlite3.connect('kospi_minute.db')
    cmd='SELECT * FROM %s'%code
    #read_data=pd.read_sql_table(code,conn)
    read_data=pd.read_sql(cmd,conn)
    print(read_data)
    return read_data

def plot_data():


if __name__ == "__main__":
    os.system('cls')
    testcode='017650'
    print("testcode=%s"%testcode)
    #read_db(testcode)
    plot_data()

