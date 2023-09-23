import os
import pandas as pd
import Constant as myarg
import maxpain 
   
def list_subdirectories(path):
    subdirectories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
    return subdirectories

sourcepath = os.path.join(myarg.disk_path,myarg.op_path)
alldf = pd.DataFrame()

for stockname in myarg.Stock:
    exdaysPath = os.path.join(sourcepath,stockname)
    exdaysList = list_subdirectories(exdaysPath)

    for exday in exdaysList:
        exdayPath = os.path.join(sourcepath,stockname,exday)
        recDays = list_subdirectories(exdayPath)

        for recday in recDays:
            callfileName = os.path.join(sourcepath,stockname,exday,recday,"calldata.csv") 
            putfileName = os.path.join(sourcepath,stockname,exday,recday,"putdata.csv") 
            
            print(callfileName)
            print(putfileName)

            try:
                # 读取 CSV 文件
                df = maxpain.main(callfileName,putfileName)
                alldf = pd.concat([alldf,df])
                
            except Exception as e:
                print(f"读取或处理文件时发生错误：{e}")
                continue

        print(alldf)
        fname = stockname  + "_" + exday + ".csv" 
        fname = os.path.join(exdayPath,fname)
        alldf.to_csv(fname,index = False)
        alldf = pd.DataFrame()


