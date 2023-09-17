import Constant as myarg
import sqlite3
import os 
import maxpain as mp
import pandas  as pd
from datetime import datetime


def list_subdirectories(path):
    subdirectories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return subdirectories

def savefile(df,FilePath):

    directory = os.path.dirname(FilePath)

    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(FilePath):
        df.to_csv(FilePath)
    else:
        temp = pd.read_csv(FilePath)
        temp = pd.concat([temp,df])
        temp.to_csv(FilePath)

def main():

    watchlist  = myarg.Stock
    optype     = myarg.OptionType 
    alldf      = pd.DataFrame()
    for name in watchlist:
        path1  = os.path.join(myarg.disk_path,myarg.op_path,name)
        exDays = list_subdirectories(path1)

        for exDay in exDays: 
            ## if exDay < Today , continue
            exDay_obj = datetime.strptime(exDay,"%Y-%m-%d")
            if exDay_obj < myarg.getToday(12):
                print("exDay < Today , Skip")

            path2 = os.path.join(path1,exDay)  
            recDays = list_subdirectories(path2)
            sourcepath = path2
            
            #for recDay in recDays:
            ## just process today auto mode
            recDay = myarg.getToday(12).strftime("%Y-%m-%d")

            putpath = os.path.join(sourcepath,recDay,"putdata.csv")
            print("callpath",callpath)
            print("putpath",putpath)
            if not os.path.exists(callpath) or not os.path.exists(putpath):
                continue

            data = mp.main(callpath,putpath,1)
            new_row = pd.Series({'date': recDay})
            data = data.assign(**new_row)
            alldf = pd.concat([alldf,data])

            print(alldf) 
            filename = name + '_' + exDay +'.csv'
            filepath = os.path.join(sourcepath,filename)
            savefile(alldf,filepath)
            alldf  = pd.DataFrame()

if __name__ == "__main__":
    main()
