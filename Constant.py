from datetime import datetime
from datetime import timedelta
import os
import pandas as pd

Stock = ["QQQ","SPY","DIA","IWM",     \
         "AAPL","MSFT","GOOG","META", \
         "AMZN","TSLA","NVDA","TLT",  \
         "^Vix","SMH","^SPX","ARKK",  \
         "AMD","JPM", "U","XLB",      \
         "BITO","XLE","XHB","XLP",    \
         "XLV","XLU","XLI","XBI",     \
         "XLK","UVXY","SOXL","XLF",   \
         "KWEB"]

Type   = ["C","P"]
OptionType = ["CALL","PUT"]

disk_path = "/media/ponder/ADATA HM900/"

op_path   = 'OptionData'

stock_path = 'StockPriceData'

db_path   = 'DailyReport'

backup_path = 'BackUp'

DailyReprotPath = '/home/ponder/migoogledrive/Stock/Daily/'

Debug     = True

offset_time = 27

def getToday(offset = 0): 
    current = datetime.now()
    current = current - timedelta(hours=offset)
    return current

class IOTool:
    def __init__(self) -> None:
        pass

    def list_subdirectories(self,path):
        subdirectories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return subdirectories    

    def savefile(instance : pd.DataFrame,FilePath):

        directory = os.path.dirname(FilePath)

        if not os.path.exists(directory):
            os.makedirs(directory)

        instance.to_csv(FilePath)
