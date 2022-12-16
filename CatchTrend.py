import time
import pandas as pd 
import uuid
import numpy as np

from pytwitter import Api
from helper.Tweet import Tweet
from helper.connect_twitter import connect_twitter

def tweet_to_object(json_tweet, json_user):
    tweet = Tweet(text=json_tweet["text"],
                  id=json_tweet["id"],
                  user_id=json_user["id"],
                  username=json_user["username"],
                  description=json_user["description"],
                  following_count=json_user["public_metrics"]["following_count"],
                  follower_count=json_user["public_metrics"]["followers_count"]
            )

    return tweet


class CatchTrend():
    """
        Catch twitter trend based on the key_trend specified

        Collect all tweet wherer the key_trend is found and all 
        the retweet of this tweet

        A time range must be specified with : a start_time and a end_time
        Format : YYYY-MM-DDTHH:MM:ssZ

    """

    def __init__(self, key_trend, start_time, end_time) -> None:
        self.api = connect_twitter()
        self.key_trend = key_trend
        self.start_time = start_time
        self.end_time = end_time
        self.__run__()
        
    
    def __run__(self):
        tweets = []
        users_merge = []

        next_token = None

        while next_token != "end":
            results = self.api.search_tweets(query=self.key_trend,
                                             expansions="author_id",
                                             user_fields="location,description,public_metrics",
                                             start_time=self.start_time,
                                             end_time=self.end_time,
                                             return_json=True,
                                             next_token=next_token,
                                             max_results=100)

            if "next_token" in results["meta"]:
                next_token = results["meta"]["next_token"]
            else:
                next_token = "end"

            users = {user["id"]: user for user in results["includes"]["users"]}

            for tweet in results["data"]:
                tweet_object = tweet_to_object(json_tweet=tweet, json_user=users[tweet["author_id"]]) 
                tweet_object.resume()
                tweets.append(tweet_object)
                
                users_merge.append([tweet_object.user_id, tweet_object.username ,tweet_object.following_count])

            time.sleep(5)

        df_users_merge = pd.DataFrame(users_merge, columns=["user_id", "username", "count_follows"])
        df_users_merge = df_users_merge.drop_duplicates()

        l_tweets = [t.to_list() for t in tweets]

        df = pd.DataFrame(l_tweets, columns=["id", "user_id","text","username","description","action_type", "user_retweet", "follower_count","following_count"])
        
        df_final = df_users_merge.merge(df, left_on="username", right_on="user_retweet")
        df_final = df_final[["user_id_x", "user_id_y", "username_x", "username_y"]]
        
        df_final.to_csv("data/user_merge_1.csv")

        df_tweet_tweet = df[["text"]]
        df_tweet_unique = df_tweet_tweet.drop_duplicates(subset=["text"])
        df_tweet_unique["id_text"] = df_tweet_unique["text"].apply(lambda x : uuid.uuid1())
        df_tweet_unique["id_text"] = df_tweet_unique["id_text"].astype(str)

        df_tweet = df.merge(df_tweet_unique, on=["text"])
        print(df_tweet)
        df_tweet["text_final"] = df_tweet.apply(lambda x: self.prep_tweet(x), axis=1)

        df_tweet.to_json("data/tweet_1.json", orient="records")

    @staticmethod
    def prep_tweet(x):
        print(x.user_retweet)
        if x.user_retweet is not None:
            len_username_pattern = len(x.username) + 7
            text = x.text
            text_prep = text[len_username_pattern:]
            return text_prep
        else:
            return x.text


if __name__ == "__main__":
    CatchTrend(key_trend="niort",
               start_time="2022-12-14T00:00:00Z",
               end_time="2022-12-14T12:00:00Z")