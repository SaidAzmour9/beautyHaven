import pandas as pd
import os
from bing_image_downloader import downloader

# قراءة ملف CSV
df = pd.read_csv('cosmetics.csv')

# إنشاء مجلد لحفظ الصور
if not os.path.exists('product_images'):
    os.makedirs('product_images')

# دالة للبحث عن صور المنتجات
def fetch_image(product_name, limit=1):
    output_dir = f'product_images/{product_name}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    downloader.download(product_name, limit=limit, output_dir=output_dir, adult_filter_off=True, force_replace=False, timeout=60)
    for file in os.listdir(output_dir):
        if file.endswith(".jpg") or file.endswith(".png"):
            return os.path.join(output_dir, file)
    return None


for index, row in df.iterrows():
    product_name = row['Name']
    print(f"Fetching image for {product_name}...")
    img_path = fetch_image(product_name)
    
    if img_path:
        print(f"Image for {product_name} saved at {img_path}")
    else:
        print(f"No image found for {product_name}")

print("Image fetching complete.")
