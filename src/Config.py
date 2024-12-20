from fastapi.templating import Jinja2Templates


class Config:
    app_name = "main:app"
    app_host = "localhost"
    app_port = 5050

    templates = Jinja2Templates(directory="static/html")
