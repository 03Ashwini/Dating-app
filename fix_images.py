from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for filename in ["person1.jpg", "person2.jpg"]:
    path = os.path.join(BASE_DIR, "test_faces", filename)
    try:
        img = Image.open(path)
        rgb_img = img.convert('RGB')  # Ensure it's proper JPEG RGB
        rgb_img.save(path, format='JPEG')
        print(f"✅ Re-saved {filename}")
    except Exception as e:
        print(f"❌ Failed to fix {filename}: {e}")
