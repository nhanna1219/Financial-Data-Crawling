class FinancialReport:
    def __init__(self, year=None, quarter=None, totalAssests=None,liabilities=None, shortLiabilities=None, longLiabilities=None, ownerEquity=None,eps=None, bvps=None, pe=None):
        self.year = year
        self.quarter = quarter
        self.totalAssests = totalAssests
        self.liabilities = liabilities
        self.shortLiabilities = shortLiabilities
        self.longLiabilities = longLiabilities
        self.ownerEquity = ownerEquity
        self.eps = eps
        self.bvps = bvps
        self.pe = pe
        
    def __str__(self):
        return f"""Financial Data for Year {self.year}, Quarter {self.quarter}:
                Total Assets: {self.totalAssests}
                Liabilities: {self.liabilities}
                Short-Term Liabilities: {self.shortLiabilities}
                Owner's Equity: {self.ownerEquity}
                EPS: {self.eps}
                BVPS: {self.bvps}
                PE: {self.pe}"""


