import pandas as pd 
import requests

def GetRequest(url):
    token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxOTk2NTc4ODk4LCJuYmYiOjE2OTY1Nzg4OTgsImNsaWVudF9pZCI6ImZpcmVhbnQud2ViIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsInJvbGVzIiwiZW1haWwiLCJhY2NvdW50cy1yZWFkIiwiYWNjb3VudHMtd3JpdGUiLCJvcmRlcnMtcmVhZCIsIm9yZGVycy13cml0ZSIsImNvbXBhbmllcy1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImZpbmFuY2UtcmVhZCIsInBvc3RzLXdyaXRlIiwicG9zdHMtcmVhZCIsInN5bWJvbHMtcmVhZCIsInVzZXItZGF0YS1yZWFkIiwidXNlci1kYXRhLXdyaXRlIiwidXNlcnMtcmVhZCIsInNlYXJjaCIsImFjYWRlbXktcmVhZCIsImFjYWRlbXktd3JpdGUiLCJibG9nLXJlYWQiLCJpbnZlc3RvcGVkaWEtcmVhZCJdLCJzdWIiOiI0MzkxNjc5My0xNTRiLTQ5ZTMtOTc2Mi1mNGFmNDA1OGYzNWQiLCJhdXRoX3RpbWUiOjE2OTY1Nzg4OTYsImlkcCI6Ikdvb2dsZSIsIm5hbWUiOiIxOTUyMTk0MEBnbS51aXQuZWR1LnZuIiwic2VjdXJpdHlfc3RhbXAiOiJiMzFmNzVlZC00YjkzLTQzOTQtYmQyOS01ZDE0MWQyNGE0YjYiLCJqdGkiOiI5ZjA4ODUyMTg5NjQwN2FjNzA2NGYwYWUyZGZjOWViYyIsImFtciI6WyJleHRlcm5hbCJdfQ.CFwF1vUcIuKc2Jx9H47UW3EZKb8mafiW3ZKauew5ulsRAdPOv6FDeV2mBECWtHwpp3I0Amzsnzp05CAtAbsrzAhC3HZliNUADSm8p2toUEDsz_eGGYqs7bxMEeWaK8uabUZodYZlvrA5Rd6MtMqq1ucFGLlJA1MeDhqPDHQcOXLiumyizYDgIngGYXug2inqYBaegbtZMGkJ_jQL4ic7QBFDsWEMzYgmTjtsDdMdHin9uyX94WbXKYUXW2Y4Q8ptUkXm_lQM84IMKZFcGhvccIKAYAT-FPgmjtDcDyxXWvwcjptwfMISb5EPCUKl35HcFPoirlydnfDeYbXIu1TjSQ'
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    return response

def GetSales(symbol, dataDir, type, limit):
    url = f"https://restv2.fireant.vn/symbols/{symbol}/financial-reports?type=IS&period={type}&compact=true&offset=0&limit={limit}"
    
    response = GetRequest(url)
    json = response.json()
    length = len(json['rows'][0])
    data = {
        "Date": json['columns'][2:length],
        "Sales": json['rows'][0][2:length]
    }
    df = pd.DataFrame(data)
    df.to_csv(dataDir + f'\\Sales_{type}.csv', index=False, header=True)
    
def GetNPAT(symbol, dataDir, type, limit):
    url = f"https://restv2.fireant.vn/symbols/{symbol}/financial-reports?type=IS&period={type}&compact=true&offset=0&limit={limit}"
    
    response = GetRequest(url)
    json = response.json()
    length = len(json['rows'][3])
    nopat_values = [value for value in json['rows'][3][2:length]]
    data = {
        "Date": json['columns'][2:length],
        "NOPAT": nopat_values
    }
    df = pd.DataFrame(data)
    df.to_csv(dataDir + f'\\NPAT_{type}.csv', index=False, header=True)
    
def getMoneyExchangePerYear(dataDir,ticker):
    opc = []
    for i in range(3,5):
        url = f"https://restv2.fireant.vn/symbols/{ticker}/full-financial-reports?type={i}&year=2023&quarter=0&limit=100"
        response = GetRequest(url)
        json = response.json()
        if json:
            obj = next((obj for obj in json if obj["name"] == "Lưu chuyển tiền thuần từ hoạt động kinh doanh"), None)
            if obj and obj.get("values"):
                for value in obj["values"]:
                    item = {
                        "Duration": value.get("period", ""),
                        "opc": value.get("value", "")
                    }
                    opc.append(item)
    df = pd.DataFrame(opc)
    grouped_data = df.groupby("Duration")["opc"].sum().reset_index()
    grouped_data.to_csv(dataDir + f'\\opc.csv', index=False, header=True)
    
def formatReport(json, dataDir):
    periods = set()
    for item in json:
        for value in item['values']:
            periods.add(value['period'])

    sorted_periods = sort_periods(periods)

    def process_hierarchy(data):
        frames = []
        for item in data:
            hierarchy_name = item['name']
            if hierarchy_name.startswith('-'):
                hierarchy_name = hierarchy_name[1:].lstrip()
            
            row_data = {period: None for period in sorted_periods}
            row_data['Item'] = hierarchy_name

            for value_item in item['values']:
                if value_item['period'] in sorted_periods:
                    row_data[value_item['period']] = value_item['value']

            frames.append(pd.DataFrame([row_data]))

        return frames

    all_frames = process_hierarchy(json)
    formatted_df = pd.concat(all_frames, ignore_index=True)

    cols = ['Item'] + sorted_periods
    formatted_df = formatted_df[cols]
    return formatted_df



def sort_periods(periods):
    # Extract year and quarter, then sort by year and quarter
    sorted_periods = sorted(
        periods, 
        key=lambda x: (int(x.split(' ')[1]), {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}[x.split(' ')[0]])
    )
    return sorted_periods

def getFinancialReportByQuarter(dataDir,ticker):
    """ Glosary
    i:
    1 = Blance Sheet
    2 = Business Operation Result
    3 = Direct Money Exchange 
    4 = Indirect Money Exchange
    """
    opc = []
    for i in range (1,5):
        url = f"https://restv2.fireant.vn/symbols/{ticker}/full-financial-reports?type={i}&year=2024&quarter=1&limit=100"
        response = GetRequest(url)
        json = response.json()
        output_file = ''
        if json:
            if i == 1 or i == 2:
                balance_sheet = formatReport(json, dataDir)
                if i == 1: 
                    output_file = f'{dataDir}/balanceSheet.csv'
                else:
                    output_file = f'{dataDir}/businessOperationResult.csv'
                balance_sheet.to_csv(output_file, index=False, encoding='utf-8-sig')
            elif i == 3 or i == 4:
                obj = next((obj for obj in json if obj["name"] == "Lưu chuyển tiền thuần trong kỳ"), None)
                if obj and obj.get("values"):
                    for value in obj["values"]:
                        item = {
                            "Period": value.get("period", ""),
                            "Lưu chuyển tiền thuần trong kỳ": value.get("value", "")
                        }
                        opc.append(item)
                        
    df = pd.DataFrame(opc)
    unique_periods_sorted = sort_periods(df['Period'].unique())

    # Create a categorical type based on the sorted unique periods
    df['Period'] = pd.Categorical(df['Period'], categories=unique_periods_sorted, ordered=True)

    # Sort the DataFrame by the 'Period' column
    df = df.sort_values(by='Period')

    # Group by the sorted 'Period' and sum
    grouped_data = df.groupby("Period")["Lưu chuyển tiền thuần trong kỳ"].sum().reset_index()

    grouped_data.to_csv(dataDir + '/moneyExchange.csv', index=False, header=True, encoding='utf-8-sig')
    print(f'Finished Crawling: {ticker}')
                    
                    