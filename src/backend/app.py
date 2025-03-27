from flask import Flask, render_template, request, jsonify
import os, json, random
from label_checker import image_has_label
from flask_cors import CORS

app = Flask(__name__)

IMAGE_FOLDER = "static/images"
ANNOTATION_FOLDER = "annotations"
TARGET_LABEL = "Personal item" 

def get_all_labels():
    labels = set()
    for file in os.listdir(ANNOTATION_FOLDER):
        if file.endswith(".json"):
            with open(os.path.join(ANNOTATION_FOLDER, file)) as f:
                data = json.load(f)
                for annotation in data.get("annotations", []):
                    labels.add(annotation["name"])
    return list(labels)


@app.route("/")
def index():
    all_labels = get_all_labels()
    target_label = random.choice(all_labels)

    all_jsons = [f for f in os.listdir(ANNOTATION_FOLDER) if f.endswith(".json")]
    random.shuffle(all_jsons)

    selected_images = []
    print(target_label)
    for json_file in all_jsons:
        img_id = os.path.splitext(json_file)[0]
        img_filename = f"{img_id}.png"
        img_path = os.path.join(IMAGE_FOLDER, img_filename)
        annotation_path = os.path.join(ANNOTATION_FOLDER, json_file)

        if os.path.exists(img_path):
            selected_images.append({
                "filename": f"images/{img_filename}",
                "correct": image_has_label(annotation_path, target_label),
                "id": img_id
            })

        if len(selected_images) >= random.randint(6, 9):
            break

    return render_template("index.html", images=selected_images, label=target_label)


@app.route("/check", methods=["POST"])
def check():
    selected_ids = request.form.get("selected")
    selected_ids = json.loads(selected_ids)

    # Recreate the challenge to get the correct answers
    all_jsons = [f for f in os.listdir(ANNOTATION_FOLDER) if f.endswith(".json")]
    correct_ids = []

    for json_file in all_jsons:
        img_id = os.path.splitext(json_file)[0]
        annotation_path = os.path.join(ANNOTATION_FOLDER, json_file)
        if image_has_label(annotation_path, TARGET_LABEL):
            correct_ids.append(img_id)

    selected_set = set(selected_ids)
    correct_set = set(correct_ids)

    # Evaluate
    passed = selected_set.issubset(correct_set)
    print(f"Selected: {selected_set}, Correct: {correct_set}")
    return f"You {'passed ✅' if passed else 'failed ❌'} the CAPTCHA!"


CORS(app)  # Allow requests from localhost:3000 (Next.js)

@app.route("/api/captcha")
def api_captcha():
    all_labels = get_all_labels()
    target_label = random.choice(all_labels)

    all_jsons = [f for f in os.listdir(ANNOTATION_FOLDER) if f.endswith(".json")]
    random.shuffle(all_jsons)

    selected_images = []
    print(target_label)
    for json_file in all_jsons:
        img_id = os.path.splitext(json_file)[0]
        img_filename = f"{img_id}.png"
        img_path = os.path.join(IMAGE_FOLDER, img_filename)
        annotation_path = os.path.join(ANNOTATION_FOLDER, json_file)

        if os.path.exists(img_path):
            selected_images.append({
                "filename": f"images/{img_filename}",
                "correct": image_has_label(annotation_path, target_label),
                "id": img_id
            })

        if len(selected_images) >= random.randint(6, 9):
            break

    # Your existing logic from `/` route
    return jsonify({
        "label": target_label,
        "images": [{"id": img["id"], "filename": img["filename"]} for img in selected_images]
    })

@app.route("/api/check", methods=["POST"])
def api_check():
    data = request.json
    selected_ids = set(data.get("selected", []))
    label = data.get("label", "").lower()
    challenge_image_ids = data.get("images", [])

    if not label or not challenge_image_ids:
        return "Missing label or images ❌", 400

    # Determine which images in the challenge set are actually correct
    correct_ids = set()

    for img_id in challenge_image_ids:
        json_path = os.path.join(ANNOTATION_FOLDER, f"{img_id}.json")
        if image_has_label(json_path, label):
            correct_ids.add(img_id)

    # Logic: must match exactly
    missed = correct_ids - selected_ids
    wrong = selected_ids - correct_ids

    passed = len(missed) == 0 and len(wrong) == 0

    print("Selected:", selected_ids)
    print("Correct:", correct_ids)
    print("Missed:", missed)
    print("Wrong:", wrong)

    if missed or wrong:
        return "Missing or Wrong images ❌", 200
    else:
        return "You passed ✅ the CAPTCHA!", 200


if __name__ == "__main__":
    app.run(debug=True)
