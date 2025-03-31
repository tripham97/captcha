from darwin.client import Client
from pathlib import Path

# Load config
config_path = Path.home() / ".darwin" / "config.yaml"
client = Client.from_config(config_path)

# Replace with your dataset slug
dataset = client.get_remote_dataset("001_frs_item_recognition_batch_004")

# Fetch dataset items
items = list(dataset.fetch_remote_files())

# Print image URLs
for item in items:
    slot = item.slots[0]
    filename = slot.get("original_filename") or slot.get("filename") or slot.get("name")
    url = slot.get("signed_url") or slot.get("url") or slot.get("path")
    print(f"{filename}: {url}")
