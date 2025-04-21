#!/usr/bin/env python3
import requests
import csv
import json
from pathlib import Path

API_BASE = "https://rickandmortyapi.com/api/character"
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "characters.csv"

def fetch_characters():
    results = []
    page = 1

    while True:
        resp = requests.get(API_BASE, params={"page": page})
        resp.raise_for_status()
        data = resp.json()
        for char in data["results"]:
            if (
                char["species"] == "Human" and
                char["status"] == "Alive" and
                "Earth" in char["origin"]["name"]
            ):
                results.append({
                    "name": char["name"],
                    "location": char["location"]["name"],
                    "image": char["image"]
                })
        if data["info"]["next"]:
            page += 1
        else:
            break

    return results

def write_to_csv(characters, filepath):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Location", "Image"])
        for c in characters:
            writer.writerow([c["name"], c["location"], c["image"]])
    print(f"Wrote {len(characters)} characters to '{filepath}'")

if __name__ == "__main__":
    chars = fetch_characters()
    # תדפיס גם את המערך כדי שתראה אותו במסך
    print(json.dumps(chars, indent=2, ensure_ascii=False))
    write_to_csv(chars, OUTPUT_FILE)
