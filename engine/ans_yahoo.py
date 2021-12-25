import os
import requests
import pandas as pd
import pprint

from dotenv import load_dotenv
from common.logger import set_logger
import const.const as CONST
from models.item import Item

load_dotenv() #環境変数のロード
logger = set_logger(__name__)

YAHOO_PRODUCT_API_URL = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"

class YahooAPI:
    
    @staticmethod
    def execute_item_search_api(jan):
        # get
        url = YAHOO_PRODUCT_API_URL
        params={
            "appid":os.environ["YAHOO_API_KEY"],
            "jan_code":jan,
            "sort":"+price",
            # "results":"5",
            #"shipping":"free"
        }
        req = requests.get(url, headers=CONST.API_HEADRS,params=params)
        if not(300 > req.status_code >=200):
            return None
        # APIの戻り値を格納
        return req.json()
    
    @staticmethod
    def fetch_item(jan):
        try:
            res = YahooAPI.execute_item_search_api(jan)
            if res == None or res.get("hits") == None or len(res["hits"]) == 0:
                return None
            
            result = []
            for i in res["hits"]:
                item_yahoo = Item(
                                name=i["name"], 
                                price=i["price"], 
                                review_count=i["review"]["count"],
                                review_average=i["review"]["rate"], 
                                url=i["url"],
                                jan=jan
                            )
                result.append(item_yahoo)
            return result

        except Exception as e:
            logger.error(f"{jan[0]}/{e}")
            return None