import json

from pathlib import Path

from fastapi import APIRouter

router = APIRouter(
    prefix="/catalog",
    tags=["Catalog"]
)

CATALOG_PATH = (
    Path(__file__)
    .parent.parent
    / "catalog"
    / "catalog.json"
)


@router.get("")
def get_catalog():

    with open(
        CATALOG_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)