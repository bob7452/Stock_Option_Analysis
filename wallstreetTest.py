import sys
import DownLoad 
from Constant import Stock,Type
from isHoliday import isholidays 


if __name__ == "__main__":

    ans = isholidays()

    if ans:
        sys.exit(1)

    try:
        if len(sys.argv) < 4:
            print("Run Auto Mode")
    
            for Name in Stock:
                for dT in Type:
                    DownLoad.DownLoad_Data(Name,0,dT)
           
            DownLoad.DownLoad_Index()
    
        else:
            name    = sys.argv[1]
            DLType  = sys.argv[2]
            dT      = sys.argv[3]
            Iterval = sys.argv[4]
    
            if DLType == 0:
                sDLType = "Option " + dT
            elif DLType == 1:
                sDLType = "Stock"
            else:
                sDLType = "Stock + Option " +dT
        
            print(name + " " + sDLType + " " + Iterval)
            DownLoad.DownLoad_Data(name,DLType,dT,Iterval)
    
    except Exception as e:
        print(f'Error Catch {e}')
        sys.exit(1)
    
    sys.exit(0)
