import os
import argparse
from PIL import Image
import pillow_heif
from tqdm import tqdm

def convert_to_webp(
    input_folder, 
    output_folder, 
    quality=80, 
    max_width=None, 
    max_height=None
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Accept HEIC, JPG, JPEG and PNG
    valid_exts = ('.heic', '.jpg', '.jpeg', '.png')
    images = [
        f for f in os.listdir(input_folder) 
        if f.lower().endswith(valid_exts)
    ]
    for img_name in tqdm(images, desc="Converting"):
        input_path = os.path.join(input_folder, img_name)
        ext = os.path.splitext(img_name)[1].lower()
        # Open HEIC files using pillow_heif, others with PIL
        if ext == '.heic':
            heif_file = pillow_heif.read_heif(input_path)
            image = Image.frombytes(
                heif_file.mode, heif_file.size, heif_file.data, "raw"
            )
        else:
            image = Image.open(input_path)
        # Resize if needed
        if max_width or max_height:
            orig_width, orig_height = image.size
            aspect = orig_width / orig_height
            new_width, new_height = orig_width, orig_height
            if max_width and orig_width > max_width:
                new_width = max_width
                new_height = int(new_width / aspect)
            if max_height and new_height > max_height:
                new_height = max_height
                new_width = int(new_height * aspect)
            if (new_width, new_height) != (orig_width, orig_height):
                image = image.resize((new_width, new_height), Image.LANCZOS)
        # Save as webp
        output_name = os.path.splitext(img_name)[0] + ".webp"
        output_path = os.path.join(output_folder, output_name)
        image.save(output_path, "WEBP", quality=quality, optimize=True)
        print(f"Saved: {output_path} ({os.path.getsize(output_path)//1024} KB)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert HEIC/JPG/JPEG/PNG to WebP and reduce file size."
    )
    parser.add_argument("input_folder", help="Folder with images")
    parser.add_argument("output_folder", help="Folder to save WebP images")
    parser.add_argument(
        "-q", "--quality", type=int, default=80,
        help="WebP quality (0-100, default: 80)"
    )
    parser.add_argument(
        "--max-width", type=int, default=None,
        help="Resize image to this max width (pixels)"
    )
    parser.add_argument(
        "--max-height", type=int, default=None,
        help="Resize image to this max height (pixels)"
    )
    args = parser.parse_args()
    convert_to_webp(
        args.input_folder, 
        args.output_folder, 
        quality=args.quality, 
        max_width=args.max_width, 
        max_height=args.max_height
    )
