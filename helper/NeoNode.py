from neomodel import config, StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo

class Tweet(StructuredNode):
    _id = UniqueIdProperty()
    text = StringProperty(unique_index=False)
    id_text = StringProperty(unique_index=True)

class User(StructuredNode):
    _id = UniqueIdProperty()
    user_id = IntegerProperty(unique_index=True)
    username = StringProperty()
    description = StringProperty()
    follower_count = IntegerProperty()
    following_count = IntegerProperty()

    tweet = RelationshipTo(Tweet, "AS_INTERACTION")
