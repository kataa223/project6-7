import os
import requests
import pandas as pd
import pprint

from dotenv import load_dotenv
from common.logger import set_logger
import const.const as CONST
from models.item import Item
from models.item_rakuten import Item_rakuten

load_dotenv() #環境変数のロード
logger = set_logger(__name__)

RAKUTEN_PRODUCT_API_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706'

class RakutenAPI:
    
    @staticmethod
    def execute_item_search_api(keyword):
        # get
        url = RAKUTEN_PRODUCT_API_URL
        params = {
            'applicationId': os.environ["RAKUTEN_API_KEY"],
            'hits': 30,#一度のリクエストで返してもらう最大個数（MAX30)
            'keyword': keyword ,#検索するキーワード
            'page':1,#何ページ目か
            'postageFlag':1,#送料込みの商品に限定
        }
        
        req = requests.get(url, params=params)
        if not(300 > req.status_code >=200):
            return None
        # APIの戻り値を格納
        return req.json()
    
    @staticmethod
    def fetch_item(keyword):
        try:
            res = RakutenAPI.execute_item_search_api(keyword)
            if res == None or res.get("Items") == None or len(res["Items"]) == 0:
                return None
            
            result = []
            for i in res["Items"]:
                item = i['Item']
                item_rakuten = Item_rakuten(
                                  name=item['itemName'], 
                                  price=item['itemPrice'], 
                                  url=item['itemUrl'],
                                  keyword=keyword)
                result.append(item_rakuten)
            return result

        except Exception as e:
            logger.error(f"{keyword[0]}/{e}")
            return None