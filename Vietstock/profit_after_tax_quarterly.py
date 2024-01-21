import requests
import csv
import os

class NetProfitParentCompany:
    def __init__(self, year_q1, year_q2, year_q3, year_q4, q1_value, q2_value, q3_value, q4_value):
        self.year_q1 = year_q1  
        self.year_q2 = year_q2  
        self.year_q3 = year_q3  
        self.year_q4 = year_q4  
        self.q1_value = q1_value  
        self.q2_value = q2_value  
        self.q3_value = q3_value  
        self.q4_value = q4_value  
        
    def __str__(self):
        return f"Q1 ({self.year_q1}): {self.q1_value}, Q2 ({self.year_q2}): {self.q2_value}, Q3 ({self.year_q3}): {self.q3_value}, Q4 ({self.year_q4}): {self.q4_value}"

url = 'https://finance.vietstock.vn/data/financeinfo'

startPage = 18 # Quarter 4 Year 2006
endPage = 1 # Quarter 3 year 2023

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'language=vi-VN; ASP.NET_SessionId=21sfmvh51dgvdttca5ah4mzh; __RequestVerificationToken=9dKBUB2UlfQaTtOeSusXXc_tcsuV2ja6a8_60wCsMtiD9goow9lymEv6ktbvi6cG3EUJk7DVU_Hm8lSiGzKyBbYFsxpZo0fIPukEC4GaQL81; Theme=Light; AnonymousNotification=; _pbjs_userid_consent_data=3524755945110770; _gid=GA1.2.2733822.1699716906; dable_uid=undefined; _cc_id=3c0816ed532b7602736fc191afc558d0; panoramaId_expiry=1699803275589; finance_viewedstock=FPT,API,; __gads=ID=7789dcb493136979:T=1699716874:RT=1699717310:S=ALNI_MaTFxocVsk5MVhjZFIEh0JEnVZPuA; __gpi=UID=00000c849d3f98a9:T=1699716874:RT=1699717310:S=ALNI_MaUsIC6-Y5YHA_mwnqsDhzLgDCgxw; _ga_EXMM0DKVEX=GS1.1.1699716905.1.1.1699717519.60.0.0; _ga=GA1.2.94767601.1699716906; cto_bundle=SbFNeF9RTTFBZ29CVk8wSlBmTWV3QzZlU2RSNUkyYjg0Q3A0WmE4NEp0VDMwSnpqUVJycGZTN3dzRHNiWExQVFlyYkZSdGtRVVdCS2pzVTRxJTJGdXpQY2VtNDRqTkl3WFM3Z0w5UVdkJTJGMXBvJTJCVU1zWVIyJTJGdTB2RmElMkI1bWw0THFTVW52eThSJTJCTm1OS3RYdnZQQ2duM3czMGpDTWU0bUE4eXIwMzV3ZHZqYjJOTm5pYmMlM0Q; cto_bidid=__ZMzV9xOFgyYTJ0NlBlZ0tlOGpIV05mUFZCNW5sMll3dEFMVEF4MWQ2SnY3SHVEeFU3UENETWpHdnBBczhwM25SWkNVdTMxSSUyRkpEWTR5VTBpcTJreXA5RXRVTkJwbyUyRmVvZmJQeGljNDZYcm5wWlElM0Q',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}
net_profit_objects = []
startYear = 2006

while startPage >= endPage:
    data = {
        'Code': 'FPT',
        'Page': startPage,
        'PageSize': 4,
        'ReportTermType': 2, # 1 for Yearly, 2 for Quarterly
        'ReportType': 'BCTQ',
        'Unit': 1000000,
        '__RequestVerificationToken': 'Z5tjjJrMhGgG5L3rKOgWUGuxPgS0a1erRTN4NQhWyxpKj-G-xfqubDx642zq0plzx74rJQ2IElp-AtzTuEySE4vbqmnxEXu_JcaDraj50341'
    }
    response = requests.post(url, data=data, headers=headers)

    
    if response.status_code == 200:
        data = response.json()
        income_statement = data[1]["Kết quả kinh doanh"]

        net_profit_data = next((item for item in income_statement if item["Name"] == "LNST của CĐ cty mẹ "), None)


        if net_profit_data:
            nextYear = startYear + 1
            net_profit = NetProfitParentCompany(
                nextYear,
                nextYear,
                nextYear,
                startYear,
                net_profit_data.get("Value3", 0),
                net_profit_data.get("Value2", 0),
                net_profit_data.get("Value1", 0),
                net_profit_data.get("Value4", 0)
            )
            net_profit_objects.append(net_profit)
            startYear += 1

        startPage -= 1

# for obj in net_profit_objects:
#     print(obj)

filename = 'NOPAT_Quarterly.csv'
current_directory = os.getcwd() + r'\\data\\'
csv_file_path = os.path.join(current_directory, filename)

csv_columns = ['Year', 'Q1', 'Q2', 'Q3', 'Q4']

csv_data = []
previous_q4_profit = 0  
count = 0
for company in net_profit_objects:
    year = company.year_q1  
    if count == 0:
        row = {
            'Year': year - 1,
            'Q1': 0,
            'Q2': 0,
            'Q3': 0,
            'Q4': company.q4_profit  
        }
    else:
        if count == len(net_profit_objects) - 1:
            nextQ4Profit = 0
        else:
            nextQ4Profit = net_profit_objects[count+1].q4_profit
        row = {
            'Year': year - 1,
            'Q1': company.q1_profit,
            'Q2': company.q2_profit,
            'Q3': company.q3_profit,
            'Q4': nextQ4Profit
        }
    csv_data.append(row)
    count += 1
# Write to CSV
try:
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(csv_data)
    print(f"Data successfully written to {csv_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")