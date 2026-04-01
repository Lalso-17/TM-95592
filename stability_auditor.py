import os
import glob
import json
import xml.etree.ElementTree as ET
from collections import Counter

def audit_stability(path):
    class_counts = Counter()
    total_elements = 0

    for file in glob.glob(os.path.join(path, "**", "*.xml"), recursive=True):
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            for elem in root.iter():
                tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
                class_counts[tag] += 1
                total_elements += 1
        except Exception as e:
            print(f"Błąd parsowania {file}: {e}")

    metrics = {}
    for cls, count in class_counts.items():
        percentage = round((count / total_elements) * 100, 2) if total_elements else 0
        metrics[cls] = {
            "count": count,
            "percentage": percentage
        }

    dominant_class = None
    dominant_percentage = 0

    for cls, data in metrics.items():
        if data["percentage"] > dominant_percentage:
            dominant_class = cls
            dominant_percentage = data["percentage"]

    if dominant_percentage > 50:
        verdict = "HIGH RISK"
    elif dominant_percentage > 35:
        verdict = "MEDIUM RISK"
    else:
        verdict = "LOW RISK"

    report = {
        "total_elements": total_elements,
        "dominant_class": dominant_class,
        "dominant_class_percentage": dominant_percentage,
        "verdict": verdict,
        "metrics": metrics
    }

    return report

def main():
    layout_path = "Artefakt02/decompiled_apk/res/layout"
    report = audit_stability(layout_path)

    with open("stability_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f'Audit complete. Verdict: {report["verdict"]}')

if __name__ == "__main__":
    main()