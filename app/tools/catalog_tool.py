import json
from pathlib import Path


CATALOG_PATH = (
    Path(__file__)
    .parent.parent
    / "catalog"
    / "catalog.json"
)


def load_catalog():

    with open(
        CATALOG_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def search_catalog(
    query: str
):
    query = query.lower()

    catalog = load_catalog()

    matches = []

    for plan in catalog["plans"]:

        plan_text = (
            plan["name"]
            + " "
            + plan["price"]
            + " "
            + " ".join(plan["features"])
        ).lower()

        keywords = query.split()

        score = sum(
            keyword in plan_text
            for keyword in keywords
        )

        if score > 0:
            matches.append(
                {
                    "score": score,
                    "plan": plan
                }
            )

    matches.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return [
        item["plan"]
        for item in matches
    ]