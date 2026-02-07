import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter()

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "hobbies.json"

def load_hobbies():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)["combinations"]


@router.get("/hobbies/{combination_key}")
async def get_hobbies(combination_key: str):
    hobbies = load_hobbies()
    if combination_key not in hobbies:
        raise HTTPException(status_code=404, detail="조합을 찾을 수 없습니다")
    return hobbies[combination_key]


@router.get("/hobbies/{combination_key}/extra")
async def get_extra_hobbies(combination_key: str):
    hobbies = load_hobbies()
    if combination_key not in hobbies:
        raise HTTPException(status_code=404, detail="조합을 찾을 수 없습니다")
    return {"extra_hobbies": hobbies[combination_key].get("extra_hobbies", [])}
