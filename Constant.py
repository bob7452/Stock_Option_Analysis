from datetime import datetime
from datetime import timedelta

Stock = ["QQQ","SPY","DIA","IWM",     \
         "AAPL","MSFT","GOOG","META", \
         "AMZN","TSLA","NVDA","TLT",  \
         "^Vix","SMH","XLF","ARKK"]

Type   = ["C","P"]
OptionType = ["Call","Put"]

disk_path = "/media/ponder/ADATA HM900/"

op_path   = 'OptionData'

stock_path = 'StockPriceData'

db_path   = 'DailyReport'

def getToday(offset = 0): 
    current = datetime.now()
    current = current - timedelta(hours=offset)
    return current
