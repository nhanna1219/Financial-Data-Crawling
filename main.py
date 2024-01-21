
import os
from Fireant import FA
from Vietstock import VS
from Fialda import FD
import pandas as pd


def CreateDir(ticker):
    baseDir = os.getcwd()
    dataDir = os.path.join(baseDir, f'data\\{ticker}')
    if not os.path.exists(dataDir):
        os.makedirs(dataDir, mode=0o7)
    return dataDir
# Get Sale
def Sale(ticker,outputType):
    dataDir = CreateDir(ticker)
    if outputType == 'Y':
        limit = 15
    else:
        limit = 1000
    FA.GetSales(ticker,dataDir,outputType,limit)

# Get Net Profit After Tax
def NPAT(ticker, outputType):
    dataDir = CreateDir(ticker)
    
    if outputType == 'Y':
        limit = 15
    else:
        limit = 1000
    FA.GetNPAT(ticker,dataDir,outputType,limit)

# Get EPS
def VSReport(ticker,outputType):
    dataDir = CreateDir(ticker)
    
    if outputType == 'Q':
        limit = 20
    else:
        limit = 10
    VS.GetReport(ticker,dataDir,outputType,limit)

def FDReport(ticker):
    dataDir = CreateDir(ticker)
    FD.getStockPrice(dataDir, ticker, "1d", "2006-10-1T00:00:00.000", "2024-1-13T15:00:00.000")

def MoneyExchangeBO(ticker):
    dataDir = CreateDir(ticker)
    FA.getMoneyExchangePerYear(dataDir,ticker)

def FAFinancialReport(ticker):
    dataDir = CreateDir(ticker)
    FA.getFinancialReportByQuarter(dataDir, ticker)
    
def main():
    baseDir = os.getcwd()
    df = pd.read_csv(f'{baseDir}\\tickers.csv', header=None)
    tickers = df.values.tolist()
    type = ['Y','Q'] # Q for Quarter, Y for Year

    for ticker in tickers:
        Sale(ticker[0], type[0])
        Sale(ticker[0], type[1])
        
        NPAT(ticker[0], type[0])
        NPAT(ticker[0], type[1])
        
        VSReport(ticker[0],type[0])
        VSReport(ticker[0],type[1])
        
        FDReport(ticker[0])
        MoneyExchangeBO(ticker[0])
        
        FAFinancialReport(ticker[0])
        
        




if __name__ == "__main__":
    main()