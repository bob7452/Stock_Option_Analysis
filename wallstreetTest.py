import sys
import pandas as pd
import os 
from wallstreet import Stock,Call,Put
from datetime import datetime


def savefile(df,date):

    today_date = datetime.today().strftime('%Y-%m-%d')
    Path = "/media/ponder/ADATA HM900/OptionData/"
    Path = Path+today_date+"/"
    directory = os.path.dirname(Path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    Path = Path + date + "_" + "OptionData.csv"
    df.to_csv(Path, index=False)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Key in Stock Name")
    else:
        name = sys.argv[1]
        print("Stock Name : " + name)
        
        stock = Call(name)
        
        for date in stock.expirations:

            allDF = pd.DataFrame()
            day,mom,year = date.split("-")
            day = int(day)
            mom = int(mom)
            year = int(year)
            
            print("========= "+ name +" - "+ date +" =========")
            total = len(stock.strikes)

            for index, price in enumerate(stock.strikes):
                price = int(price)
                temp = Call(name,d = day, m = mom, y= year,strike = price)

                data = { 'Date'  : [date],
                        'Strike' : [price],
                        'OI' : [temp.open_interest],
                        'IV' : [temp.implied_volatility()],
                        'Delta' : [temp.delta()],
                        'Gamma' : [temp.gamma()],
                        'Theta' : [temp.theta()],
                        }
                df = pd.DataFrame(data)
                allDF = pd.concat([allDF,df])


                print(f"==== Process {index+1}/{total} ====")

            print(allDF.to_string(index=False))
            savefile(allDF,date)
            print("")
            print("========================================")