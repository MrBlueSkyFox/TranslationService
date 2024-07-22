from fastapi import FastAPI

from events import startup
from routes import router as word_route

app = FastAPI()
app.add_event_handler("startup", startup(app))


app.include_router(word_route)
