##################################################################
################# startup and configuration file #################
##################################################################

import os 
from pathlib import Path
from fastapi import FastAPI
from fastapi_chameleon import global_init
from fastapi.staticfiles import StaticFiles
import uvicorn


from views import (
    account,
    home,
    saleAds,
)


app = FastAPI()


def main():
    config()
    start_uvicorn()


def start_uvicorn():
    import uvicorn
    from docopt import docopt
    help_doc = """
                    FastAPI Web server for the course management Web App.
                    
                    Usage:
                        main.py [-p PORT] [-h HOST_IP] [-r]
                    
                    Options:
                        -p PORT, --port=PORT            Listen on this port [default: 8000]
                        -h HOST_IP, --host=HOST_IP      Listen on this IP address [default: 127.0.0.1]
                        -r, --reload                    Reload app
    """
    args = docopt(help_doc)


    uvicorn.run (
        'main:app',
        port = int(args['--port']),
        host = args['--host'],
        reload = args['--reload'],
        reload_includes = [
            '*.py',
        ]
    )


def config():
    config_templates()
    config_routes()
    
    
def config_templates():
    dev_mode = True
    BASE_DIR = Path(__file__).resolve().parent
    template_folder = str(BASE_DIR / 'templates')
    print(f'template_folder={template_folder}')
    global_init(template_folder, auto_reload=dev_mode)


def config_routes():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    for view in [home, saleAds, account]:
        app.include_router(view.router)


if __name__ == '__main__':
    main()
else:
    config()
