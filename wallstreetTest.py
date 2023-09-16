import sys
import DownLoad 
from Constant import Stock,Type


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Run Auto Mode")

        for Name in Stock:
            for dT in Type:
                DownLoad.DownLoad_Data(Name,2,dT)
       
        DownLoad.DownLoad_GreenIndex()
        DownLoad.DownLoad_MarketBreath()

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
