import Constant as myarg
import sqlite3
import os 
import maxpain as mp
import pandas  as pd

def list_subdirectories(path):
    subdirectories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return subdirectories


def main():

    #search subfolder under path
    sourcepath = os.path.join(myarg.disk_path,myarg.op_path)
    path = sourcepath

    recordday  = list_subdirectories(path)

    watchlist  = myarg.Stock
    optype     = myarg.OptionType 

    day = "2023-10-20"

    stocks = ['QQQ','TSLA','SPY','^Vix']
    for name in stocks:
       alldf = pd.DataFrame()
       if name == "^Vix":
           day = "2023-10-18"
       for date in recordday:
           path = sourcepath  

           callpath = os.path.join(path,date,name,day,"CALL","OptionData.csv")
           putpath = os.path.join(path,date,name,day,"PUT","OptionData.csv")
           data = mp.main(callpath,putpath,1)
           
           new_row = pd.Series({'date': date})
           data = data.assign(**new_row)

           alldf = pd.concat([alldf,data])

       print(alldf) 
       fileName = name +"_20231020.csv"
       alldf.to_csv(fileName)

if __name__ == "__main__":
    main()
