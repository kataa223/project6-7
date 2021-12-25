import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dotenv import load_dotenv
load_dotenv() #環境変数のロード

from common.spread_sheet_manager import SpreadsheetManager
from engine.ans_yahoo import YahooAPI
from engine.ans_rakuten import RakutenAPI

SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]

def search(search_key:str, search_api:str, output_sheet_name:str):
    # 検索key一覧の取得
    ss = SpreadsheetManager()
    ss.connect_by_sheetname(SPREADSHEET_ID, search_key)
    key_df = ss.fetch_all_data_to_df()
    key_list = key_df[search_key.split("_")[0]].values.tolist()
    
    # APIによる商品の検索
    items = []
    for key in key_list:
        print(key)
        
        if search_api == "0":
            # YahooAPIでの検索
            item_list = YahooAPI.fetch_item(key[0])
        elif search_api == "1":
            # RakutenAPIでの検索
            item_list = RakutenAPI.fetch_item(key[0])
        
        if item_list:
            for item in item_list:
                items.append(item.__dict__)
    
    # 書き込み
    ss.connect_by_sheetname(SPREADSHEET_ID, output_sheet_name)
    ss.bulk_insert(items)
    

def main():
    # YahooAPIでの検索
    print("YahooAPIでの検索スタート！")
    search("jan_list", "0", "item_list")
    print("YahooAPIでの検索完了！")
    
    # 楽天APIでの検索
    print("楽天APIでの検索スタート！")
    search("keyword_list", "1", "item_list2")
    print("楽天APIでの検索完了！")

main()