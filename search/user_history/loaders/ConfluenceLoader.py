import base64
import logging
import urllib.request
from typing import List
from urllib.error import HTTPError

from bs4 import BeautifulSoup

from helper.ConfigReader import get_string_property
from user_history.loaders.Loader import Loader


# BBC stands for British Broadcasting Corporation, the news site our dataset is from.
class ConfluenceLoader(Loader):
    LOG = logging.getLogger(__name__)

    def retrieve_history(self, username: str) -> List[str]:
        # Because I was unable to get an API endpoint working for confluence, we take a somewhat unorthodox approach
        # and scrape the page. This is very much intended as a temporary measure.
        base_url = get_string_property("confluence", "location")
        full_url = f"{base_url}/confluence/display/~{username}"

        soup = self._get_soup_of_page(full_url)
        # Find all update items
        update_items = soup.find_all("div", {"class": "update-item-details"})
        history_urls = []
        for update_item in update_items:
            item_url_end = update_item.find("a")["href"]
            history_urls.append(f"{base_url}{item_url_end}")

        # We need to visit the page of the item in history to get the id, I can't get it in the url, see
        # https://jira.atlassian.com/browse/CONFSERVER-11285
        found_ids: List[str] = []
        for url in history_urls:
            history_soup = self._get_soup_of_page(url)
            meta_object = history_soup.find("meta", {"name": "ajs-page-id"})
            if meta_object is not None:
                found_ids.append(meta_object["content"])
        return found_ids


    def _get_soup_of_page(self, url: str) -> BeautifulSoup:
        conf_username = get_string_property("confluence", "username")
        conf_password = get_string_property("confluence", "password")

        req = urllib.request.Request(url)

        credentials = ('%s:%s' % (conf_username, conf_password))
        encoded_credentials = base64.b64encode(credentials.encode('ascii'))
        req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

        try:
            page = urllib.request.urlopen(req)
        except HTTPError:
            # If the page for some reason can't load, it's better to continue and not use edit history, than
            # to return nothing.
            page = ""
        return BeautifulSoup(page, 'html.parser')
