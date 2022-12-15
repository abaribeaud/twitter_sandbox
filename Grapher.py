import time
import pandas as pd 
import logging
import numpy as np

from pytwitter import Api



class Grapher():
    """
        Tweet to graph format
    """

    def __init__(self) -> None:
        self.__run__()

    def __run__(self):
        df_user = pd.read_csv("data/user_merge.csv")
        
        df_user = df_user[["user_id_x","user_id_y"]]
        df_user.to_csv("data/prep_gephy.csv", index=False)
        

if __name__ == "__main__":
    Grapher()