from icecream import ic
import requests
from input_format import CustomInputFormat
from random_datas import generate_data





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
        print(self.infos)


class TestFastAPIRoutes(__TestFastAPIRoutesInit):
    #please ensure on your FastAPI app(openapi_url='/openapi.json')
    def __send_requests(self,method:str,path:str,data:dict,isfor_json:bool=True,isfor_params:bool=False):
        headers=self.headers
        if path==self.custom_inputs.get('path','') and method==self.custom_inputs.get('method',''):
            data=self.custom_inputs['data']
            isfor_json=self.custom_inputs['isfor_json']
            isfor_params=self.custom_inputs['isfor_params']
            if self.custom_inputs.get('headers',False):
                if self.custom_inputs['headers']!={}:
                    headers=self.custom_inputs['headers']

        print(headers)

        if data=={}:
            data=None

        json,form_data,param=data,None,None
        response=None


        if not isfor_json:
            json,param,form_data=None,None,data

        if isfor_params:
            param=data
            json=None
            form_data=None

        if self.base_url[-1]=='/':
            self.base_url=self.base_url[0:-1]
            print(self.base_url)

        url=f"{self.base_url}{path}"
        # print(f"method : {method} url : {url} data : {data} json : {json} formdata : {form_data} param : {param}")
        if method=='POST':
            response=requests.post(url,json=json,data=form_data,params=param,headers=self.headers)
        elif method=='PUT':
            response=requests.put(url,json=json,data=form_data,params=param,headers=headers)
        elif method=='DELETE':
            response=requests.delete(url,params=param,headers=headers)
        elif method=='GET':
            response=requests.get(url,params=param,headers=headers)
        ic(method,url,data,response.status_code,':',response.json())
        return response



    def __get_field_data(self,schema_name:str):
        data={}
        field_names=list(self.infos['components']['schemas'][schema_name]['properties'].keys())

        for field_name in field_names:
            print(schema_name,field_name)
            field=self.infos['components']['schemas'][schema_name]['properties'][field_name]
            value=None
            if datatype:=field.get('type',None):
                item=field.get('items',{})
                item_type=None

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
        return data

    def start_test(self):
        
        paths=self.routes_tocheck
        if paths==[]:
            paths=list(self.infos['paths'].keys())
        print(paths)

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
                                print('from param name :', datatype.get('items',{'type':None})['type'])
                                data[param_name['name']]=generate_data(datatype=datatype.get('type',None),items_type=datatype.get('items',{'type':None})['type'])
                                print(datatype)
                        print(data)

                        self.__send_requests(method.upper(),path,data,isfor_params=isfor_query,isfor_json=isfor_json)
                        
                else:
                    print('no route/path found')
            else:
                print('unchecked routes :',path)

if __name__=='__main__':
    test=TestFastAPIRoutes()
    print(test.start_test())

 