import time
import pandas as pd 
import logging
import numpy as np

from pytwitter import Api
from helper.connect_twitter import connect_twitter

class CatchFollow():

    def __init__(self) -> None:
        self.api = connect_twitter()
        self.__run__()

    def __run__(self):
        df_user = pd.read_csv("data/user_merge.csv")
        df_user = df_user[df_user["count_follows"] > 0]
        users_merge = df_user["user_id"].to_list()
        users_merge = tuple(users_merge)
        logging.info("Script start : %s users" % len(users_merge)) 
        df_user_merge = pd.DataFrame({"id_1": users_merge})

        match_user_final = pd.DataFrame(columns=["user_id", "id_1", "id_2"])

        for user_id in users_merge:
            logging.info("[id: %s]" % user_id)

            follows = []

            try:
                result_follows = self.api.get_following(user_id=user_id, return_json=True)
            except Exception as e:
                logging.error(e)
                raise e

            if "data" not in result_follows:
                continue

            for follow in result_follows["data"]:
                follows.append([user_id, int(follow["id"])])

            df_follows = pd.DataFrame(follows, columns=['user_id', 'id_2'], dtype=np.int64)

            match_user = df_user_merge.merge(df_follows, left_on="id_1", right_on="id_2")
            match_user_final = pd.concat([match_user_final, match_user])

            logging.info("\t%s user linked" % match_user.shape[0])

            time.sleep(60)


        match_user_final.to_csv("data/user_link.csv")
        

if __name__ == "__main__":
    CatchFollow()