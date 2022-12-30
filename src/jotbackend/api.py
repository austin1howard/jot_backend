"""
FastAPI API.
"""
import secrets
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.cors import CORSMiddleware

from jotbackend import dao
from jotbackend.domain import CreateJot, Jot
from jotbackend.util import narvhal

app = FastAPI(
    title="Jot Backend",
    description="Backend for Jot.",
    version="0.1.0",
)

security = HTTPBearer()


def get_current_username(credentials: HTTPAuthorizationCredentials = Depends(security)):
    current_credentials_bytes = credentials.credentials.encode("utf8")
    correct_credentials_bytes = b"imsecure"
    is_correct_credentials = secrets.compare_digest(current_credentials_bytes, correct_credentials_bytes)
    if not is_correct_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.credentials


@app.get("/")
async def ping():
    return {"ping": "pong"}


@app.post("/jot", status_code=201)
async def create_jot(jot: CreateJot, username: str = Depends(get_current_username)):
    jot = Jot(
        plain_text=jot.plain_text,
        created_at=datetime.utcnow(),
        latitude=jot.latitude,
        longitude=jot.longitude,
    )
    await dao.create_jot(jot)


# FastAPI's `add_middleware` will add this before the 500 handling, so 500 errors won't have proper CORS headers. So, we do the wrapping
# manually.
app = CORSMiddleware(app=app, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Execution from Python
def main():
    narvhal(app, 2500)


if __name__ == "__main__":
    main()
