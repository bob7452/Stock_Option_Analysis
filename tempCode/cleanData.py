import os
import pandas as pd
import Constant as myarg
   
def list_subdirectories(path):
    subdirectories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path,d))]
    return subdirectories

sourcepath = os.path.join(myarg.disk_path,myarg.op_path)

for stockname in myarg.Stock:
    exdaysPath = os.path.join(sourcepath,stockname)
    exdaysList = list_subdirectories(exdaysPath)

    for exday in exdaysList:
        filename = stockname+'_'+exday+'.csv'
        finalPath = os.path.join(sourcepath,stockname,exday,filename)
    
        print(finalPath)

        # 读取 CSV 文件
        df = pd.read_csv(finalPath)
        
        # 删除所有包含 "Unnamed" 的列
        df = df.loc[:, ~df.columns.str.contains('Unnamed')]
        
        # 保存 DataFrame 到新的 CSV 文件
        df.to_csv(finalPath, index=False)
        


