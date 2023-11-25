import Constant as myarg
import sqlite3
import os 
import maxpain as mp
import pandas  as pd
from datetime import datetime
import shutil
import sys
import tarfile
from isHoliday import isholidays

def backup():

    today = myarg.getToday(myarg.offset_time).strftime("%Y-%m-%d")
    opsourcefolder = os.path.join(myarg.disk_path, myarg.op_path)
    stocksourcefolder = os.path.join(myarg.disk_path, myarg.stock_path)
    targetpath = os.path.join(myarg.disk_path,myarg.backup_path,today)

    if not os.path.exists(targetpath):
        os.makedirs(targetpath)

    op_archive_path = os.path.join(myarg.disk_path, myarg.backup_path, today, f"{myarg.op_path}.tar.gz")
    print(f"Backing up files from {opsourcefolder} to {op_archive_path}")
    with tarfile.open(op_archive_path, "w:gz") as tar:
        tar.add(opsourcefolder, arcname=os.path.basename(myarg.op_path))

    stock_archive_path = os.path.join(myarg.disk_path, myarg.backup_path, today, f"{myarg.stock_path}.tar.gz")
    print(f"Backing up files from {stocksourcefolder} to {stock_archive_path}")
    with tarfile.open(stock_archive_path, "w:gz") as tar:
        tar.add(stocksourcefolder, arcname=os.path.basename(myarg.stock_path))

    # today = myarg.getToday(myarg.offset_time).strftime("%Y-%m-%d")
    # opsourcefolder = os.path.join(myarg.disk_path,myarg.op_path)
    # stocksourcefolder = os.path.join(myarg.disk_path,myarg.stock_path)

    # targetfolder = os.path.join(myarg.disk_path,myarg.backup_path,today,myarg.op_path)
    # print(f"Back File {opsourcefolder} to {targetfolder}")
    # shutil.copytree(opsourcefolder,targetfolder)
    
    # targetfolder = os.path.join(myarg.disk_path,myarg.backup_path,today,myarg.stock_path)
    # print(f"Back File {stocksourcefolder} to {targetfolder}")
    # shutil.copytree(stocksourcefolder,targetfolder)


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
        exDays = list_subdirectories(path1)

        for exDay in exDays: 
            ## if exDay < Today , continue
            exDay_obj = datetime.strptime(exDay,"%Y-%m-%d")
            if exDay_obj < myarg.getToday(myarg.offset_time):
                print("exDay < Today , Skip")
                continue

            path2 = os.path.join(path1,exDay)  
            recDays = list_subdirectories(path2)
            sourcepath = path2
            
            #for recDay in recDays:
            ## just process today auto mode
            recDay = myarg.getToday(myarg.offset_time).strftime("%Y-%m-%d")

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
            savefile(alldf,filepath)
            alldf  = pd.DataFrame()

if __name__ == "__main__":
    
    ans = isholidays()

    if ans:
        sys.exit(1)
    
    try:
        backup()
        main()
    except Exception as e:
        print(f'{e}')
        sys.exit(1)
        
    sys.exit(0)
