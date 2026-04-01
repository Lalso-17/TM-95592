import os
import glob
import json
import xml.etree.ElementTree as ET

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

def mine_selectors(path):
    results = []

    for file in glob.glob(os.path.join(path, "**", "*.xml"), recursive=True):
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            for elem in root.iter():
                res_id = elem.get(f"{ANDROID_NS}id")
                tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
                content_desc = elem.get(f"{ANDROID_NS}contentDescription")

                if res_id:
                    results.append({
                        "file": os.path.basename(file),
                        "id": res_id.split("/")[-1],
                        "tag": tag,
                        "contentDescription": content_desc if content_desc else ""
                    })
        except Exception as e:
            print(f"Błąd parsowania {file}: {e}")

    return results

def main():
    layout_path = "Artefakt02/decompiled_apk/res/layout"
    data = mine_selectors(layout_path)

    with open("miner_report.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Zapisano {len(data)} rekordów do miner_report.json")

if __name__ == "__main__":
    main()