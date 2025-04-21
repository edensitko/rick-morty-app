import requests
import csv
import os

API_URL = "https://rickandmortyapi.com/api/character"
OUTPUT_CSV = "characters.csv"

def fetch_characters():
    results = []
    url = API_URL
    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for char in data['results']:
            if (
                char.get('species') == 'Human' and
                char.get('status') == 'Alive' and
                char.get('origin', {}).get('name') == 'Earth'
            ):
                results.append({
                    'Name': char['name'],
                    'Location': char['location']['name'],
                    'Image': char['image']
                })
        url = data.get('info', {}).get('next')
    return results

def write_csv(data):
    cwd = os.getcwd()
    out_path = os.path.join(cwd, OUTPUT_CSV)
    print(f"CWD: {cwd}")
    print(f"Writing CSV to: {out_path}")
    with open(out_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Location', 'Image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

def main():
    print("Fetching characters from Rick and Morty API...")
    characters = fetch_characters()
    print(f"Found {len(characters)} matching characters.")
    write_csv(characters)
    print("Done.")

if __name__ == "__main__":
    main()
