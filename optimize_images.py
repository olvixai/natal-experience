import os
from PIL import Image

download_dir = r"C:\Users\hecgo\Downloads"
target_dir = r"e:\ANTIGRAVITY\NATALEXPERIENCE\img"
images = ["88.jpeg", "99.jpeg", "mejora_la_calidad_2K_202606261109.jpeg"]

for img_name in images:
    img_path = os.path.join(download_dir, img_name)
    if os.path.exists(img_path):
        try:
            with Image.open(img_path) as img:
                width, height = img.size
                print(f"File: {img_name}, original size: {width}x{height}")
                
                # Calculate new size max 1200px
                max_dim = 1200
                if width > max_dim or height > max_dim:
                    if width > height:
                        new_width = max_dim
                        new_height = int(max_dim * (height / width))
                    else:
                        new_height = max_dim
                        new_width = int(max_dim * (width / height))
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                else:
                    new_width, new_height = width, height
                
                # Save optimized
                base_name = img_name.split('.')[0]
                target_filename = f"buggy-norte-nuevo-{base_name}.jpg"
                target_path = os.path.join(target_dir, target_filename)
                
                # convert to RGB if needed (e.g. RGBA)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                    
                img.save(target_path, "JPEG", quality=85, optimize=True)
                print(f"Saved optimized to: {target_filename}, new size: {new_width}x{new_height}")
        except Exception as e:
            print(f"Error processing {img_name}: {e}")
    else:
        print(f"File not found: {img_path}")
