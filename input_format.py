from typing import TypedDict

class CustomInputFormat(TypedDict):
    method:str
    path:str
    isfor_params:bool
    isfor_json:bool
    data:dict
    headers:dict