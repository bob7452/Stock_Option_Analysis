import os
import pandas as pd
import Constant as myarg
import datetime 
import shutil


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
            print(tdate)

            if tdate < myarg.getToday(12).date():
                continue    

            if tdate.weekday() == weekday:
                filename  = stockname + '_'+ exday + '.csv'
                filepath = os.path.join(sourcepath,stockname,exday,filename)
                print(filepath) 
                try:
                    df = pd.read_csv(filepath)
                    last_row = df.iloc[-1]
                    last_row['Date'] = exday
                    print(last_row)
                    alldf = alldf._append(last_row,ignore_index = True)

                except Exception as e:
                    print(f"open file fail {e}")
                    continue
            else:
                continue

        try:
            alldf.to_excel(wexcel,sheet_name=stockname,index=False)               
            alldf = pd.DataFrame()
        except Exception as e:
            print(f'write file fail{e}')
            continue

    return reportName

def updateReport(source,target):
    shutil.copy(source,target)

if __name__ == "__main__":

    today = myarg.getToday(12).strftime('%Y-%m-%d')
    reportName = 'Report_' + today + '.xlsx' 
    reportName = os.path.join(myarg.disk_path,myarg.db_path,reportName)

    wexcel = pd.ExcelWriter(reportName,engine = 'xlsxwriter')
    source = report(wexcel,reportName)
    wexcel._save()
    
    target = myarg.DailyReprotPath 
    updateReport(source,target)



