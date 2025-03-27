import json
import os

def image_has_label(json_path, target_label):
    """
    Returns True if the annotation JSON contains the target label.
    """
    if not os.path.exists(json_path):
        return False

    with open(json_path) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️ Failed to parse {json_path}")
            return False

        for annotation in data.get("annotations", []):
            if annotation.get("name", "").lower() == target_label.lower():
                return True
        return False
