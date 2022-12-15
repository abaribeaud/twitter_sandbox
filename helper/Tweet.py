class Tweet():

    def __init__(self, id, text, user_id, username, description, follower_count, following_count) -> None:
        self.id = id
        self.text = text
        self.user_id = user_id
        self.username = username
        self.description = description
        self.action_type = "retweet" if text[:4] == "RT @" else "tweet"
        self.user_retweet = text.split()[1][1:-1] if text[:4] == "RT @" else None
        self.follower_count = follower_count
        self.following_count = following_count
        self.user_retweet_id = None

    def tweet_to_neo4j(self):
        return None

    def to_list(self):
        l_tweet = [self.id,
                   self.user_id,
                   self.text,
                   self.username,
                   self.description,
                   self.action_type,
                   self.user_retweet,
                   self.follower_count,
                   self.following_count]

        return l_tweet

    def to_json(self):
        jtweet = {"id": self.id,
                  "user_id": self.user_id,
                  "text": self.text,
                  "username": self.username,
                  "description": self.description,
                  "action_type": self.action_type,
                  "user_retweet": self.user_retweet,
                  "follower_count": self.follower_count,
                  "following_count": self.following_count
                 }
        
        return jtweet


    def resume(self):
        print("Text : %s  ...\nNom d'utilisateur : %s\nDescription : %s ...\nType : %s" % (self.text[:100], self.username, self.description[:100], self.action_type))