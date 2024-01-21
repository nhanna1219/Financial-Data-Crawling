import pandas as pd 
import requests
import json

def getStockPrice(dataDir, symbol, interval, fromTime, toTime):
    while True:
        url = f"https://fwtapi3.fialda.com/api/services/app/StockInfo/GetTradingChartData?symbol={symbol}&interval={interval}&fromTime={fromTime}&toTime={toTime}"
        header = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.35.0",
            "Connection": "keep-alive"
        }    
        response = requests.get(url, headers=header)
        if (response.status_code == 200):
            result = response.text
            jsonObj = json.loads(result)
            data_list = [
                {"tradingTime": pd.to_datetime(entry["tradingTime"]).strftime('%Y-%m-%d'), "lastPrice": entry["lastPrice"] }
                for entry in jsonObj["result"]
            ]
            df = pd.DataFrame(data_list)

            df.to_csv(dataDir + f'\\StockPrice.csv', index=False, header=True)
            break
        else:
            print(f"Request failed with status code: {response.status_code}. Retrying...")
            fromTime = (pd.to_datetime(fromTime) + pd.DateOffset(years=1)).strftime('%Y-%m-%dT%H:%M:%S.000')