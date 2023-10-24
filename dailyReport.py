import os
import pandas as pd
import Constant as myarg
import datetime 
import shutil
import dataplot
import sys

def list_subdirectories(path):
    subdirectories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
    return subdirectories

def report(wexcel,reportName):

    sourcepath = os.path.join(myarg.disk_path,myarg.op_path)
    stocklist = myarg.Stock

#    today = myarg.getToday(12).strftime('%Y-%m-%d')
#    reportName = 'Report_' + today + '.xlsx' 
#    reportName = os.path.join(myarg.disk_path,myarg.db_path,reportName)

    for stockname in stocklist:
        exdaysPath = os.path.join(sourcepath,stockname)
        exdaysList = list_subdirectories(exdaysPath)
        alldf = pd.DataFrame()

        weekday = 4 if stockname != "^Vix" else 2

        for exday in exdaysList:
            y,m,d = exday.split('-')
            y = int(y)
            m = int(m)
            d = int(d)
    
            tdate = datetime.date(y,m,d)

            if tdate < myarg.getToday(myarg.offset_time).date():
                continue    

            if tdate.weekday() == weekday:
                filename  = stockname + '_'+ exday + '.csv'
                filepath = os.path.join(sourcepath,stockname,exday,filename)
                try:
                    df = pd.read_csv(filepath)
                    last_row = df.iloc[-1]
                    last_row['Date'] = exday
                    alldf = alldf._append(last_row,ignore_index = True)

                except Exception as e:
                    print(f"open file fail {e}")
                    continue
               
                print(f'filepath : {filepath}')
                dataplot.genpicture(stockname,exday,filepath)
            else:
                continue

        try:
            alldf['Date'] = pd.to_datetime(alldf['Date'])
            alldf = alldf.sort_values(by='Date',ascending = True)
            alldf['Date'] = alldf['Date'].dt.strftime('%Y-%m-%d')
            alldf.to_excel(wexcel,sheet_name=stockname,index=False)               
            alldf = pd.DataFrame()
        except Exception as e:
            print(f'write file fail{e}')
            continue

def updateReport(source,target):
    shutil.copy(source,target)

def updatepic():
    today = myarg.getToday(myarg.offset_time).strftime('%Y-%m-%d')
    stocklist = myarg.Stock
    
    for name in stocklist:
        exday = myarg.find_third_friday(today,name)
        targetpath = os.path.join(myarg.daliy_picture,exday)
        filepath = os.path.join(myarg.disk_path,myarg.op_path,name,exday,f"{name}_{exday}.csv.png")

        print(f'path {filepath}')

        if not os.path.exists(filepath):
            continue

        if not os.path.exists(targetpath):
            os.makedirs(targetpath)

        updateReport(filepath,target=targetpath)        

        #print('remove picture')
        #os.remove(filepath)

if __name__ == "__main__":

    try:
        today = myarg.getToday(myarg.offset_time).strftime('%Y-%m-%d')
        reportName = 'Report_' + today + '.xlsx' 
        reportName = os.path.join(myarg.disk_path,myarg.db_path,reportName)

        wexcel = pd.ExcelWriter(reportName,engine = 'xlsxwriter')
        report(wexcel,reportName)
        wexcel._save()
    
        target = myarg.DailyReprotPath 
        updateReport(reportName,target)
        updatepic()

    except Exception as e:
        sys.exit(1)

    sys.exit(0)
