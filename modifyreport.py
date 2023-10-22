import Constant as myarg
import sqlite3
import os 
import maxpain as mp
import pandas  as pd
from datetime import datetime
import shutil
import dataplot

def backup():

    today = myarg.getToday(myarg.offset_time).strftime("%Y-%m-%d")
    opsourcefolder = os.path.join(myarg.disk_path,myarg.op_path)
    stocksourcefolder = os.path.join(myarg.disk_path,myarg.stock_path)

    targetfolder = os.path.join(myarg.disk_path,myarg.backup_path,today,myarg.op_path)
    print(f"Back File {opsourcefolder} to {targetfolder}")
    shutil.copytree(opsourcefolder,targetfolder)
    targetfolder = os.path.join(myarg.disk_path,myarg.backup_path,today,myarg.stock_path)
    print(f"Back File {stocksourcefolder} to {targetfolder}")
    shutil.copytree(stocksourcefolder,targetfolder)
    

def list_subdirectories(path):
    subdirectories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return subdirectories

def savefile(df,FilePath):

    directory = os.path.dirname(FilePath)

    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(FilePath):
        df.to_csv(FilePath,index=False)
    else:
        try:
            temp = pd.read_csv(FilePath)
            temp = pd.concat([temp,df])
            temp.to_csv(FilePath,index=False)
        except pd.errors.EmptyDataError:
            df.to_csv(FilePath,index = False)

def main():

    watchlist  = myarg.Stock
    print(watchlist)
    optype     = myarg.OptionType 
    alldf      = pd.DataFrame()
    for name in watchlist:
        path1  = os.path.join(myarg.disk_path,myarg.op_path,name)
        if not os.path.exists(path1):
            continue

        exDays = list_subdirectories(path1)

        for exDay in exDays: 
            ## if exDay < Today , continue
            #exDay_obj = datetime.strptime(exDay,"%Y-%m-%d")
            #if exDay_obj < myarg.getToday(myarg.offset_time):
            #   print("exDay < Today , Skip")
            #   continue
        
            path2 = os.path.join(path1,exDay)  
            recDays = list_subdirectories(path2)
            sourcepath = path2
            
            

            for recDay in recDays:
            ## just process today auto mode
            #recDay = myarg.getToday(myarg.offset_time).strftime("%Y-%m-%d")

                callpath = os.path.join(sourcepath,recDay,"calldata.csv")
                putpath = os.path.join(sourcepath,recDay,"putdata.csv")
                print("callpath",callpath)
                print("putpath",putpath)
                if not os.path.exists(callpath) or not os.path.exists(putpath):
                    print("callpath / putpath is not exist")
                    continue

                data = mp.main(callpath,putpath,0)
                alldf = pd.concat([alldf,data])

            print(alldf) 
            filename = name + '_' + exDay +'.csv'
            filepath = os.path.join(sourcepath,filename)
           
            if os.path.exists(filepath):
                os.remove(filepath)

            savefile(alldf,filepath)
            alldf  = pd.DataFrame()

def _modifyPic():

    watchlist  = myarg.Stock
    alldf      = pd.DataFrame()
    for name in watchlist:
        path1  = os.path.join(myarg.disk_path,myarg.op_path,name)

        if not os.path.exists(path1) :
            print("report not exist")
            continue

        exDays = list_subdirectories(path1)

        for exDay in exDays: 
            path2 = os.path.join(path1,exDay)  
            sourcepath = path2
        
            reportName = os.path.join(sourcepath,f'{name}_{exDay}.csv')
            print(f'Report {reportName}')
            if not os.path.exists(reportName) :
                print("report not exist")
                continue

            dataplot.genpicture(name,exDay,reportName)
            


def _modifystock():

    watchlist  = myarg.Stock
    watchlist.append("Index")
    print(watchlist)

    alldf      = pd.DataFrame()
    for name in watchlist:
        sourcepath  = os.path.join(myarg.disk_path,myarg.stock_path,name)
        recDays = list_subdirectories(sourcepath)

        for recDay in recDays:
            if name == "Index":
                GreenPath = os.path.join(sourcepath,recDay,"CNNGreenIndex.csv")
                MarketPath = os.path.join(sourcepath,recDay,"MarketBreath.csv")
                greendata = pd.read_csv(GreenPath)
                marketdata = pd.read_csv(MarketPath)
                
                print(f'market path : {MarketPath}\n')
                print(f'Green Path : {GreenPath}\n')

                newdata = pd.DataFrame({
                    'Date': [greendata['Date'].iloc[0]],
                    'Fear Green Value': [greendata['Value'].iloc[0]],
                    'MMTW': [marketdata['Value'].iloc[0]],
                    'MMFI': [marketdata['Value'].iloc[1]],
                    'MMTH': [marketdata['Value'].iloc[2]]
                })
                
                alldf = pd.concat([alldf,newdata])

            else:
                stockpath = os.path.join(sourcepath,recDay,"Data.csv")
                print("stockpath",stockpath)
                stockprice = pd.read_csv(stockpath)
                newdata = pd.DataFrame({
                    'Date': [recDay],
                    'Open': [stockprice['Open'].iloc[0]],
                    'Close':[stockprice['Close'].iloc[-1]],
                    'High': [stockprice['High'].max()],
                    'Low': [stockprice['Low'].min()]
                }) 
                alldf = pd.concat([alldf,newdata])

        print(alldf) 
        filename = name + '.csv'
        filepath = os.path.join(sourcepath,filename)
        
        savefile(alldf,filepath)
        alldf  = pd.DataFrame()


if __name__ == "__main__":
#    backup()
#    _modifystock()
#    main()
    _modifyPic()   
   
