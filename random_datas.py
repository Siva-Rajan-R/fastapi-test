import random,string
from typing import Any

def generate_data(datatype,items_type:Any=None):
    if datatype=='string':
        return 'De-Buggers'
    elif datatype=='integer':
        return random.randrange(1,100)
    elif datatype=='number':
        return round(random.uniform(1,1000),2)
    elif datatype=='array':
        data=[]
        if items_type!=None:
            for _ in range(5):
                if isinstance(items_type,str):
                    data.append(generate_data(datatype=items_type))
                elif isinstance(items_type,dict):
                    data.append(items_type)
        else:
            data=['string',12,7.0,False]
        return data
    
    elif datatype == 'object':
        return {"name":"siva rajan","age":18,"mark_percentage":18.9,'is_pg':False}
    elif datatype == 'boolean':
        return random.choice([False,True])
    
    else:
        return datatype