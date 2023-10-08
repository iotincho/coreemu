# Built-in packages
from datetime import datetime

# Third-party packages
from fastapi import FastAPI

# Local packages


app = FastAPI()

@app.get("/keep_alive")
async def root():
    return {
        "data": {
            "utc_time": datetime.utcnow()
        }
    }


