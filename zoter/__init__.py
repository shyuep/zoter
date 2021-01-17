"""
Main package to interface with Zotero API.
"""

import datetime
import logging
import os

import requests

NEW_VER = datetime.datetime.today().strftime("%Y%m%d")

logger = logging.getLogger(__name__)


class Zoter:
    """
    Class for interacting with Zotero API.
    """

    def __init__(self, user_id: str = os.environ.get("ZOTERO_USER_ID"),
                 api_key: str = os.environ.get("ZOTERO_API_KEY")):
        """
        In order for you to use this class, you need to generate a Zotero API key.
        Login to Zotero web interface -> Settings -> Feeds/API -> Create new private key
        Then add your zotero userid (a string of numbers!) and api key as environment
        variables ZOTERO_USER_ID or ZOTERO_API_KEY, respectively. Or you can just pass in
        your user id and api_key to this class.

        :param user_id: Zotero user id. Defaults to ZOTERO_USER_ID environment variable.
        :param api_key: Zotero API key. Defaults to ZOTERO_API_KEY environment variable.
        """
        self.session = requests.Session()
        self.session.headers = {"Zotero-API-Key": api_key}
        self.user_id = user_id

    def __enter__(self):
        """
        Support for "with" context.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Support for "with" context.
        """
        self.session.close()

    def get_my_publications(self) -> list:
        """
        Returns a list of publications.

        :return: List of publications for user_id.
        """
        url = "https://api.zotero.org/users/%s/publications/items" % self.user_id
        total = float("inf")
        start = 0
        items = []
        while start < total:
            response = self.session.get(url, params={"start": start, "limit": 100})
            d = response.json()
            items.extend(d)
            total = int(response.headers["Total-Results"])
            start += len(d)
            logger.debug("start = %d, total = %d" % (start, total))
        return items
