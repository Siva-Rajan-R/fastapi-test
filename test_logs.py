from rich.console import Console
from rich.text import Text
import os

def get_log_file_path():
    log_file_directory='DeB-FastAPI-Test-Logs'
    os.makedirs(log_file_directory,exist_ok=True)

    cur_log_file_no=0
    
    while True:
        log_file_name=f'DeB-FastAPI-Test-Logs-{cur_log_file_no+1}.txt'
        path=os.path.join(log_file_directory,log_file_name)

        if not os.path.exists(path):
            return path
        cur_log_file_no+=1



console=Console()
log_file_path=get_log_file_path()
file_log=Console(record=True,file=open(log_file_path,'a'))

def status_code_colors(status_code):
    if 100 <= status_code < 200:
        return "cyan"
    elif 200 <= status_code < 300:
        return "bold green"
    elif 300 <= status_code < 400:
        return "blue"
    elif 400 <= status_code < 500:
        return "bold yellow"
    elif 500 <= status_code < 600:
        return "bold red"
    else:
        return "white"

def log_request(method: str, path: str,data:dict, status: int,response:str,method_of_input:str,is_last_route:bool=False):
    color_map = {
        "GET": "#00F6FF",
        "POST": "#00FF03",
        "DELETE": "red",
        "PUT": "yellow",
        "PATCH": "magenta"
    }

    if not response.isprintable():
        response={'DeB-FastApi-Test-Response':'Binary response (Image,Video,Audio,File,HTML...)'}

    method_text = Text(method, style=color_map.get(method, "white"))

    console.print(f"\n\n\n[bold]-> {method_text} [white]{path}[/white] Inputs ({method_of_input}) ->  [#52EEFF]{data}[/#52EEFF] -> [{status_code_colors(status)}]{status}[/{status_code_colors(status)}][/bold]",style=color_map.get(method.upper(),'green'))
    console.print(f'[bold]Result : {response}',style='white')
    if is_last_route:
        console.print(f'\n\n[bold]You can see your logs on the directory of : [#52EEFF]{log_file_path}[/#52EEFF]',style='white')
    file_log.print(f"\n\n\n-> {method} {path} Inputs ({method_of_input}) -> {data} -> {status}")
    file_log.print(f'Result : {response}')