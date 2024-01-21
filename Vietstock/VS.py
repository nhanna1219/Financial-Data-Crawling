import requests
import pandas as pd
from Vietstock.model import FinancialReport


def AssignValue(objects, index, key, item):
    setattr(objects[index], key, item['Value4'])
    setattr(objects[index + 1], key, item['Value3'])
    setattr(objects[index + 2], key, item['Value2'])
    setattr(objects[index + 3], key, item['Value1'])

def CalLongLiabilities(objects, index):
    for i in range(4):
        obj = objects[index + i]
        if obj.liabilities is None or obj.shortLiabilities is None:
            obj.longLiabilities = None
        else:
            obj.longLiabilities = obj.liabilities - obj.shortLiabilities

def GetReport(Ticker, dataDir, type, limit):
   type = 1 if type == 'Y' else 2
   url = 'https://finance.vietstock.vn/data/financeinfo'
   maxPage = limit  # Max page
   headers = {
       'Content-Type': 'application/x-www-form-urlencoded',
       'Cookie': 'language=vi-VN; ASP.NET_SessionId=21sfmvh51dgvdttca5ah4mzh; __RequestVerificationToken=9dKBUB2UlfQaTtOeSusXXc_tcsuV2ja6a8_60wCsMtiD9goow9lymEv6ktbvi6cG3EUJk7DVU_Hm8lSiGzKyBbYFsxpZo0fIPukEC4GaQL81; Theme=Light; AnonymousNotification=; _pbjs_userid_consent_data=3524755945110770; _gid=GA1.2.2733822.1699716906; dable_uid=undefined; _cc_id=3c0816ed532b7602736fc191afc558d0; panoramaId_expiry=1699803275589; finance_viewedstock=FPT,API,; __gads=ID=7789dcb493136979:T=1699716874:RT=1699717310:S=ALNI_MaTFxocVsk5MVhjZFIEh0JEnVZPuA; __gpi=UID=00000c849d3f98a9:T=1699716874:RT=1699717310:S=ALNI_MaUsIC6-Y5YHA_mwnqsDhzLgDCgxw; _ga_EXMM0DKVEX=GS1.1.1699716905.1.1.1699717519.60.0.0; _ga=GA1.2.94767601.1699716906; cto_bundle=SbFNeF9RTTFBZ29CVk8wSlBmTWV3QzZlU2RSNUkyYjg0Q3A0WmE4NEp0VDMwSnpqUVJycGZTN3dzRHNiWExQVFlyYkZSdGtRVVdCS2pzVTRxJTJGdXpQY2VtNDRqTkl3WFM3Z0w5UVdkJTJGMXBvJTJCVU1zWVIyJTJGdTB2RmElMkI1bWw0THFTVW52eThSJTJCTm1OS3RYdnZQQ2duM3czMGpDTWU0bUE4eXIwMzV3ZHZqYjJOTm5pYmMlM0Q; cto_bidid=__ZMzV9xOFgyYTJ0NlBlZ0tlOGpIV05mUFZCNW5sMll3dEFMVEF4MWQ2SnY3SHVEeFU3UENETWpHdnBBczhwM25SWkNVdTMxSSUyRkpEWTR5VTBpcTJreXA5RXRVTkJwbyUyRmVvZmJQeGljNDZYcm5wWlElM0Q',
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
   }
   objects = []
   index = 0
   while maxPage >= 1:
      data = {
          'Code': Ticker,
          'Page': maxPage,
          'PageSize': 4,
          'ReportTermType': type,  # 1 for Yearly, 2 for Quarterly
          'ReportType': 'BCTQ',
          'Unit': 1000000,
          '__RequestVerificationToken': 'Z5tjjJrMhGgG5L3rKOgWUGuxPgS0a1erRTN4NQhWyxpKj-G-xfqubDx642zq0plzx74rJQ2IElp-AtzTuEySE4vbqmnxEXu_JcaDraj50341'
      }
      response = requests.post(url, data=data, headers=headers)

      if response.status_code == 200:
         data = response.json()
         if not data[0]:
            maxPage -= 1
            continue
         for duration in data[0]:
            item = FinancialReport()
            item.year = duration['YearPeriod']
            item.quarter = duration['TermCode']
            objects.append(item)

         balance_sheet = data[1]['Cân đối kế toán']
         financial_statement = data[1]['Chỉ số tài chính']
         
         balance_items = {
             'totalAssests': balance_sheet[1],
             'liabilities': balance_sheet[2],
             'shortLiabilities': balance_sheet[3],
             'ownerEquity': balance_sheet[4]
         }

         financial_items = {
             'eps': financial_statement[0],
             'bvps': financial_statement[1],
             'pe': financial_statement[2]
         }
         
         for key, item in balance_items.items():
            AssignValue(objects, index, key, item)

         CalLongLiabilities(objects, index)

         for key, item in financial_items.items():
            AssignValue(objects, index, key, item)

         index = index + 4
         maxPage -= 1

   type = 'Y' if type == 1 else 'Q'

   data = []
   for item in objects:
      duration = item.year if type == 'Y' else f'{item.year} - {item.quarter}'
      data.append({
          'Duration': duration,
          'Total Assests': item.totalAssests,
          'Liabilities': item.liabilities,
          'Short-term Liabilities': item.shortLiabilities,
          'Long-term Liabilities': item.longLiabilities,
          'Owner\'s Equity': item.ownerEquity,
          'EPS': item.eps,
          'BVPS': item.bvps,
          'PE': item.pe
      })
   df = pd.DataFrame(data)
   df.drop_duplicates(inplace=True)
   df.to_csv(dataDir + f'\\FinancialReport_{type}.csv', index=False, header=True)
