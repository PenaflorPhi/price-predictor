import json
import os
from time import sleep

import requests
from dotenv import load_dotenv


def load_api_key() -> str | None:
    load_dotenv()
    return os.getenv("API_KEY")


def load_games() -> dict[str, int]:
    games = {
        "KINGDOM HEARTS HD 2.8 Final Chapter Prologue": 2552440,
        "KINGDOM HEARTS III + Re Mind (DLC)": 2552450,
        "Spyro™ Reignited Trilogy": 996580,
        "Factorio": 427520,
        "Balatro": 2379780,
        "Hyperbolica": 1256230,
        "Assassin's Creed™: Director's Cut Edition": 15100,
        "Assassin's Creed 2": 33230,
        "Assassin’s Creed® Brotherhood": 48190,
        "Assassin's Creed® Revelations": 201870,
        "FINAL FANTASY": 1173770,
        "FINAL FANTASY II": 1173780,
        "FINAL FANTASY III": 1173790,
        "Final Fantasy III (3D Remake)": 239120,
        "FINAL FANTASY IV": 1173800,
        "FINAL FANTASY IV: THE AFTER YEARS": 346830,
        "FINAL FANTASY V": 1173810,
        "FINAL FANTASY VI": 1173820,
        "FINAL FANTASY VII": 3837340,
        "CRISIS CORE –FINAL FANTASY VII– REUNION": 1608070,
        "FINAL FANTASY VII REBIRTH": 2909400,
        "FINAL FANTASY VII REMAKE INTERGRADE": 1462040,
        "FINAL FANTASY VIII - REMASTERED": 1026680,
        "FINAL FANTASY VIII": 39150,
        "FINAL FANTASY IX": 377840,
        "FINAL FANTASY X/X-2 HD Remaster": 359870,
        "FINAL FANTASY XII THE ZODIAC AGE": 595520,
        "FINAL FANTASY® XIII": 292120,
        "FINAL FANTASY® XIII-2": 292140,
        "LIGHTNING RETURNS™: FINAL FANTASY® XIII": 345350,
        "FINAL FANTASY XV WINDOWS EDITION": 637650,
        "Final Fantasy XVI": 2515020,
        "Red Dead Redemption": 2668510,
        "Red Dead Redemption 2": 1174180,
        "SpongeBob SquarePants: The Cosmic Shake": 1282150,
        "SpongeBob SquarePants: Battle for Bikini Bottom - Rehydrated": 969990,
        "Mega Man X Legacy Collection": 743890,
    }

    return games


def get_price_history(games: dict[str, int]) -> list[dict]:
    API_KEY = load_api_key()
    print(API_KEY)
    BASE = "https://api.isthereanydeal.com"
    HEADERS = {"Authorization": f"Bearer {API_KEY}"}

    price_history = []

    for game_name, game_id in games.items():
        r = requests.post(
            f"{BASE}/lookup/id/shop/61/v1",
            params={"key": API_KEY},
            json=[f"app/{game_id}"],
        )
        uuid = r.json().get(f"app/{game_id}")
        if uuid is None:
            print(f"No ITAD match for {game_name}")
            continue

        r = requests.get(
            f"{BASE}/games/history/v2",
            headers=HEADERS,
            params={
                "key": API_KEY,
                "id": uuid,
                "country": "US",
                "shops": 61,
            },
        )
        print(f"Got data for: {game_name}")

        print(r.json())

        price_history.append({game_name: r.json()})
        sleep(1)

    return price_history


if __name__ == "__main__":
    print(json.dumps(load_games(), indent=4, ensure_ascii=False))

    for game in get_price_history(load_games()):
        print(game)
