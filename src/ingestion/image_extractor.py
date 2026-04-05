import fitz
import os

def extract_images(pdf_path, output_dir="images"):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    image_paths = []

    for i, page in enumerate(doc):
        images = page.get_images(full=True)
        for j, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]

            path = f"{output_dir}/page_{i}_{j}.png"
            with open(path, "wb") as f:
                f.write(img_bytes)

            image_paths.append(path)

    return image_paths