from turtle import pd
from app_api.models import MOB_T_OPERATION
import pandas as pd


class processing_services:  
    def verfloat(data):
        if data is None:
            data=0
        return(data)

    def last_date(month, year):
        if month == 1:
            return 12, year - 1
        else:
            return month - 1, year

    def imprimiroperaciones():
            try:
                export = []
                salidaoperaciones = MOB_T_OPERATION.objects.all()
                for result in salidaoperaciones:
                    export.append(vars(result)) 
                df=pd.DataFrame.from_dict(export)
                df.to_excel("MOB_T_OPERATION.xlsx")        
            except:
                print("no se puedo guardar")     
    

