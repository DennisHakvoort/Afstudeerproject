import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import search
from helper.ConfigReader import get_string_property, get_int_property

# setup fastapi
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(search.router)


def _setup_fast_api():
    ip = get_string_property("api", "ip")
    port = get_int_property("api", "port")
    uvicorn.run(app, host=ip, port=port)



def _setup_logger():
    logformat = get_string_property("logging", "format")
    loglevel = logging.getLevelName(get_string_property("logging", "level"))
    logging.basicConfig(format=logformat, level=loglevel)
    logging.info("Logger initiated")


if __name__ == '__main__':
    # Launch all things that should be initialized on start of application
    _setup_logger()
    _setup_fast_api()
