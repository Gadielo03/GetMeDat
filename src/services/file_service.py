from appdirs import *
import json
import os   
appname = "GetMeDat"
appauthor = "Gadiel"

directorio = user_data_dir(appname, appauthor)

def initalize_storage() -> None:
    config = load_config()
    if not config:
        os.makedirs(directorio, exist_ok=True)
        default_config = {
          "current_url": "http://localhost:3000",
          "current_method": "GET",
          "current_params": {},
          "current_auth": "",
          "request_headers": {},
          "request_body": {},
          "response_data": {},
          "response_headers": {},
          "status_code": 0,
          "error_message": "",
          "is_loading": False,
          "timestamp": "",
          "show_timestamps": True,
          "auto_format_json": True
        }
        save_config(default_config)

def save_config(data: dict, filename: str = "default_config.json") -> None:
    archivo_path = os.path.join(directorio, filename)
    with open(archivo_path, 'w') as archivo:
        json.dump(data, archivo)

def load_config(filename: str = "default_config.json") -> dict:
    archivo_path = os.path.join(directorio, filename)
    try:
        with open(archivo_path, 'r') as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return {}  
    except json.JSONDecodeError:
        return {} 
    
def list_configs() -> list:
    files = os.listdir(directorio)
    return [f for f in files if f.endswith('.json')]