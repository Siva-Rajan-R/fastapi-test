import requests
from .input_format import CustomInputFormat
from .random_datas import generate_data
import random
from .test_logs import console,log_request,file_log
import os
from datetime import datetime


class __TestFastAPIRoutesInit:
    #please ensure on your FastAPI app(openapi_url='/openapi.json')
    def __init__(self,custom_inputs:CustomInputFormat={},base_url:str='http://127.0.0.1:8000/',headers:dict=None,routes_tocheck:list=[],routes_touncheck:list=[]):
        #please ensure on your FastAPI app(openapi_url='/openapi.json')
        self.infos=requests.get(f'{base_url}openapi.json').json()
        self.custom_inputs=custom_inputs
        self.base_url=base_url
        self.headers=headers
        self.routes_tocheck=routes_tocheck
        self.routes_touncheck=routes_touncheck


class TestFastAPIRoutes(__TestFastAPIRoutesInit):
    #please ensure on your FastAPI app(openapi_url='/openapi.json')
    def __send_requests(self,method:str,path:str,data:dict,isfor_json:bool=True,isfor_params:bool=False):
        method_of_input='JSON DATA'
        headers=self.headers
        if path==self.custom_inputs.get('path','') and method==self.custom_inputs.get('method',''):
            data=self.custom_inputs['data']
            isfor_json=self.custom_inputs['isfor_json']
            isfor_params=self.custom_inputs['isfor_params']
            if self.custom_inputs.get('headers',False):
                if self.custom_inputs['headers']!={}:
                    headers=self.custom_inputs['headers']


        if data=={}:
            data=None

        json,form_data,param=data,None,None
        response=None


        if not isfor_json:
            json,param,form_data=None,None,data
            method_of_input='FORM DATA'

        if isfor_params:
            param=data
            json=None
            form_data=None
            method_of_input='QUERY DATA'

        if self.base_url[-1]=='/':
            self.base_url=self.base_url[0:-1]

        url=f"{self.base_url}{path}"
        # (f"method : {method} url : {url} data : {data} json : {json} formdata : {form_data} param : {param}")
        if method=='POST':
            response=requests.post(url,json=json,data=form_data,params=param,headers=self.headers)
        elif method=='PUT':
            response=requests.put(url,json=json,data=form_data,params=param,headers=headers)
        elif method=='DELETE':
            response=requests.delete(url,json=json,data=form_data,params=param,headers=headers)
        elif method=='GET':
            response=requests.get(url,json=json,data=form_data,params=param,headers=headers)
        # ic(method,url,data,response.status_code,':',response.json())
        log_request(method=method,path=url,data=data,status=response.status_code,response=response.text,method_of_input=method_of_input)
        return response



    def __get_field_data(self,schema_name:str):
        data={}
        field_base_query=self.infos['components']['schemas'][schema_name]
        if field_names:=field_base_query.get('properties',None):
            field_names=list(field_names.keys())

            for field_name in field_names:
                field=field_base_query['properties'][field_name]
                value=None
                
                if is_anyof:=field.get('anyOf',None):
                    field=is_anyof[0]


                if datatype:=field.get('type',None):
                    item=field.get('items',{})
                    item_type=None

                    if format_type:=field.get('format',None):
                        datatype=format_type

                    if item.get('type',None):
                        item_type=item['type']
                        
                    elif ref_schema_name:=item.get('$ref',None):
                        ref_schema_name=ref_schema_name.split('/')[-1]
                        item_type=self.__get_field_data(schema_name=ref_schema_name)

                    value=generate_data(datatype=datatype,items_type=item_type)

                else:
                    if ref2_schema_name:=field.get('$ref',None):
                        ref2_schema_name=ref2_schema_name.split('/')[-1]
                        value=self.__get_field_data(ref2_schema_name)
                data[field_name]=value
        else:
            value=random.choice(field_base_query['enum'])
            return value
        
        return data

    def start_test(self):

        text = " FASTAPI TESTING BY DE-BUGGERS "
        pad_width = (os.get_terminal_size().columns - len(text)) // 2
        line = "-" * pad_width + text + "-" * pad_width
        console.print(f"\n[bold]{line}[/bold]", style="#00ff00")

        paths=self.routes_tocheck
        if paths==[]:
            paths=list(self.infos['paths'].keys())

        console.print(f"\n[bold]Paths/Routes to test -> : {paths} {len(paths)} Paths/Routes",style='magenta')

        file_log.print(line)
        file_log.print(f"Date : {datetime.now().date()} Time : {datetime.now().time()}")
        file_log.print(f"\nPaths/Routes to test -> : {paths} {len(paths)} Paths/Routes")

        for path in paths:
            if path not in self.routes_touncheck:
                if methods:=self.infos['paths'].get(path,False):
                    for method in list(methods.keys()):
                        data={}
                        datatype=None
                        isfor_query=False
                        isfor_json=True

                        if schema:=self.infos['paths'][path][method].get('requestBody',0):
                            json_schema=schema['content'].get('application/json',0)
                            if not json_schema:
                                form_schema=schema['content'].get('application/x-www-form-urlencoded',0)
                                if not form_schema:
                                    form_schema=schema['content'].get('multipart/form-data',0)
                                schema=form_schema
                                isfor_json=False
                            else:
                                schema=json_schema
                            schema_name=schema['schema']['$ref'].split('/')[-1]
                            datas=self.__get_field_data(schema_name=schema_name)
                            data=datas

                        elif param_names:=self.infos['paths'][path][method].get('parameters',0):
                            isfor_query=True
                            for param_name in param_names:
                                datatype=param_name['schema']
                                if datatype.get('anyOf',None):
                                    datatype=datatype['anyOf'][0]
                                data[param_name['name']]=generate_data(datatype=datatype.get('format',None) if datatype.get('format',None) else datatype.get('type',None),items_type=datatype.get('items',{'type':None})['type'])

                        self.__send_requests(method.upper(),path,data,isfor_params=isfor_query,isfor_json=isfor_json)
                        
                else:
                    print('No route/path found')
            else:
                print('Unchecked routes :',path)

if __name__=='__main__':
    test=TestFastAPIRoutes()
    test.start_test()

 