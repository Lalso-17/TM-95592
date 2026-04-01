import os
import glob
import json
import xml.etree.ElementTree as ET

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

def check_a11y(path):
    gaps = []

    for file in glob.glob(os.path.join(path, "**", "*.xml"), recursive=True):
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            for elem in root.iter():
                node_text = elem.get(f"{ANDROID_NS}text")
                node_desc = elem.get(f"{ANDROID_NS}contentDescription")
                node_id = elem.get(f"{ANDROID_NS}id")
                tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag

                # 🔴 KLUCZOWY WARUNEK
                if node_text and not node_desc:
                    gaps.append({
                        "file": os.path.basename(file),
                        "tag": tag,
                        "id": node_id.split("/")[-1] if node_id else "no-id",
                        "text": node_text,
                        "issue": "Brak contentDescription"
                    })

        except Exception as e:
            print(f"Błąd parsowania {file}: {e}")

    return gaps


def main():
    layout_path = "Artefakt02/decompiled_apk/res/layout"
    report = check_a11y(layout_path)

    with open("a11y_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f"Znaleziono {len(report)} problemów (A11y gaps)")

if __name__ == "__main__":
    main()