from datetime import datetime
from datetime import timedelta

Stock = ["QQQ","SPY","DIA","IWM",     \
         "AAPL","MSFT","GOOG","META", \
         "AMZN","TSLA","NVDA","TLT",  \
         "^Vix","SMH","XLF","ARKK",   \
         "AMD","JPM", "U","XLB",      \
         "BITO","XLE","XHB","XLP",    \
         "XLV","XLU","XLI","XBI",     \
         "XLK","UVXY","SOXL","^SPX"]

Type   = ["C","P"]
OptionType = ["CALL","PUT"]

disk_path = "/media/ponder/ADATA HM900/"

op_path   = 'OptionData'

stock_path = 'StockPriceData'

db_path   = 'DailyReport'

Debug     = True


def getToday(offset = 0): 
    current = datetime.now()
    current = current - timedelta(hours=offset)
    return current
