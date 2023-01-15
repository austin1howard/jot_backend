"""
FastAPI API.
"""
from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from odmantic import ObjectId
from starlette.middleware.cors import CORSMiddleware

from jotbackend import dao
from jotbackend.domain import CreateJot, Jot
from jotbackend.util import get_subject_from_token, narvhal

app = FastAPI(
    title="Jot Backend",
    description="Backend for Jot.",
    version="0.1.0",
)

security = HTTPBearer()


def get_user_email(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # This is a JWT, check it
    email = get_subject_from_token(credentials.credentials)

    return email


@app.get("/")
async def ping():
    return {"ping": "pong"}


@app.post("/jot", status_code=201)
async def create_jot(jot: CreateJot, email: str = Depends(get_user_email)):
    jot = Jot(
        plain_text=jot.plain_text,
        created_at=datetime.utcnow(),
        latitude=jot.latitude,
        longitude=jot.longitude,
    )
    await dao.create_jot(jot)


@app.get("/jots", response_model=List[Jot])
async def get_jots(include_handled: bool = Query(False), email: str = Depends(get_user_email)) -> List[Jot]:
    return [j async for j in dao.get_jots(include_handled)]


@app.get("/jot/{id}", response_model=Jot)
async def get_jot(id: str, email: str = Depends(get_user_email)) -> Jot:
    jot = await dao.get_jot(ObjectId(id))
    if not jot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jot not found")
    return jot


@app.delete("/jot/{id}")
async def mark_jot_handled(id: str, email: str = Depends(get_user_email)):
    jot = await dao.get_jot(ObjectId(id))
    if not jot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jot not found")
    await dao.mark_jot_handled(ObjectId(id), None)


# FastAPI's `add_middleware` will add this before the 500 handling, so 500 errors won't have proper CORS headers. So, we do the wrapping
# manually.
app = CORSMiddleware(app=app, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# Execution from Python
def main():
    narvhal(app, 2500)


if __name__ == "__main__":
    main()
