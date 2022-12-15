import time
import pandas as pd 
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
        df_users_merge.to_csv("data/test_dup.csv")

        l_tweets = [t.to_list() for t in tweets]

        df = pd.DataFrame(l_tweets, columns=["id", "user_id","text","username","description","action_type", "user_retweet", "follower_count","following_count"])
        
        df_final = df_users_merge.merge(df, left_on="username", right_on="user_retweet")
        df_final = df_final[["user_id_x", "user_id_y", "username_x", "username_y"]]
        
        df_final.to_csv("data/user_merge.csv")
        df.to_json("data/tweet.json", orient="records")


if __name__ == "__main__":
    CatchTrend(key_trend="niort",
               start_time="2022-12-06T00:00:00Z",
               end_time="2022-12-11T12:00:00Z")