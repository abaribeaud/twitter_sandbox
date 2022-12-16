import pandas as pd
from neomodel import config, UniqueIdProperty
from helper.NeoNode import User, Tweet
import uuid

class PopulateDB():
    config.DATABASE_URL = 'cred'

    def __init__(self) -> None:
        self.__run__()

    def __run__(self):
        df_tweet = pd.read_json("data/tweet_1.json", orient="record")

        df_tweet_tweet = df_tweet[["text", "id_text"]]
        df_tweet_unique = df_tweet_tweet.drop_duplicates(subset=["text"])
        
        df_tweet_unique.apply(lambda x : self.tweet_to_node(x), axis=1)

        df_tweet_user = df_tweet[['user_id', 'username', 'description', 'follower_count', 'following_count']]

        df_tweet_user = df_tweet_user.drop_duplicates(subset=["user_id"])

        df_tweet_user.apply(lambda x : self.user_to_node(x), axis=1)
        
        df_map = df_tweet[["user_id", "id_text"]]

        self.connect_node(df_map)

        

    @staticmethod
    def connect_node(node_map):
        for _, row in node_map.iterrows():
            user = User.nodes.get(user_id=row["user_id"])
            tweet = Tweet.nodes.get(id_text=row["id_text"]) 

            user.tweet.connect(tweet)

    @staticmethod
    def user_to_node(x):
        User(username=x.username,
                    user_id=x.user_id,
                    description=x.description,
                    follower_count=x.follower_count,
                    following_count=x.following_count).save()

    @staticmethod
    def tweet_to_node(x):
        Tweet(text=x.text,
                    id_text=x.id_text).save()

if __name__ == "__main__":
    PopulateDB()