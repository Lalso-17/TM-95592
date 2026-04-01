import json

def main():
    with open("miner_report.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    user_id = input("Podaj id: ").strip()
    user_tag = input("Podaj tag: ").strip()

    matches = []

    for item in data:
        if item.get("id") == user_id and item.get("tag") == user_tag:
            matches.append(item)

    print(f"Znaleziono {len(matches)} dopasowań.")

    if len(matches) == 1:
        print("STATUS: ZALICZONE! Twój selektor jest unikalny.")
    else:
        print("STATUS: NIEZALICZONE! Selektor nie jest unikalny.")

if __name__ == "__main__":
    main()