from pytwitter import Api

import json
import os
import logging

def connect_twitter():
    """
        Connect twitter api using bearer token

        :rtype: pytwitter.Api
    """

    if "TWITTER_BEARER_TOKEN" not in os.environ.keys():
        raise Exception('Impossible de récuperer le jeton d\'accès a Twitter "TWITTER_BEARER_TOKEN" dans les variables d\'environnement')

    api = Api(
        bearer_token=os.environ.get("TWITTER_BEARER_TOKEN")
    )

    return api


if __name__ == "__main__":
    connect_twitter()