"""Build a 32,000-image printed Thai character evaluation set.

Every image is rendered from an OFL-licensed font. No handwriting source is used.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROOT = PROJECT_ROOT / "data" / "local"
OUTPUT = ROOT / "TH_Characters_PrintFont_Large_Test"
ZIP_PATH = ROOT / "TH_Characters_PrintFont_Large_Test.zip"
LABELS = PROJECT_ROOT / "data" / "metadata" / "labels.csv"

# Twenty font instances x twenty rendering contexts = 400 images per class.
STATIC_FONTS = [
    ("Kanit-Regular", PROJECT_ROOT / "assets" / "fonts" / "Kanit-Regular.ttf"),
    ("Kanit-Bold", PROJECT_ROOT / "assets" / "fonts" / "Kanit-Bold.ttf"),
    ("Prompt-Regular", PROJECT_ROOT / "assets" / "fonts" / "Prompt-Regular.ttf"),
    ("Prompt-Bold", PROJECT_ROOT / "assets" / "fonts" / "Prompt-Bold.ttf"),
    ("Sarabun-Regular", PROJECT_ROOT / "assets" / "fonts" / "Sarabun-Regular.ttf"),
    ("Sarabun-Bold", PROJECT_ROOT / "assets" / "fonts" / "Sarabun-Bold.ttf"),
    ("BaiJamjuree-Regular", PROJECT_ROOT / "assets" / "fonts" / "BaiJamjuree-Regular.ttf"),
    ("BaiJamjuree-Bold", PROJECT_ROOT / "assets" / "fonts" / "BaiJamjuree-Bold.ttf"),
    ("ChakraPetch-Regular", PROJECT_ROOT / "assets" / "fonts" / "ChakraPetch-Regular.ttf"),
    ("ChakraPetch-Bold", PROJECT_ROOT / "assets" / "fonts" / "ChakraPetch-Bold.ttf"),
    ("Mitr-Regular", PROJECT_ROOT / "assets" / "fonts" / "Mitr-Regular.ttf"),
    ("Mitr-Bold", PROJECT_ROOT / "assets" / "fonts" / "Mitr-Bold.ttf"),
    ("Pridi-Regular", PROJECT_ROOT / "assets" / "fonts" / "Pridi-Regular.ttf"),
    ("Pridi-Bold", PROJECT_ROOT / "assets" / "fonts" / "Pridi-Bold.ttf"),
    ("Taviraj-Regular", PROJECT_ROOT / "assets" / "fonts" / "Taviraj-Regular.ttf"),
    ("Taviraj-Bold", PROJECT_ROOT / "assets" / "fonts" / "Taviraj-Bold.ttf"),
]
VARIABLE_FONTS = [
    ("NotoSansThai-Regular", PROJECT_ROOT / "assets" / "fonts" / "NotoSansThai-Variable.ttf", 400, 100.0),
    ("NotoSansThai-Bold", PROJECT_ROOT / "assets" / "fonts" / "NotoSansThai-Variable.ttf", 750, 86.0),
    ("NotoSerifThai-Regular", PROJECT_ROOT / "assets" / "fonts" / "NotoSerifThai-Variable.ttf", 400, 100.0),
    ("NotoSansThaiLooped-Semibold", PROJECT_ROOT / "assets" / "fonts" / "NotoSansThaiLooped-Variable.ttf", 650, 86.0),
]
CONTEXTS = [
    (size, x_offset, y_offset)
    for size in (92, 102, 112, 122, 132)
    for x_offset, y_offset in ((-3, -2), (3, 2), (-2, 3), (2, -3))
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def static_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def variable_font(path: Path, size: int, weight: int, width: float) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(path, size=size)
    values = [axis["default"] for axis in font.get_variation_axes()]
    for index, axis in enumerate(font.get_variation_axes()):
        axis_name = axis["name"].decode("ascii", errors="ignore").lower()
        if "weight" in axis_name:
            values[index] = weight
        elif "width" in axis_name:
            values[index] = width
    font.set_variation_by_axes(values)
    return font


def render(char: str, font: ImageFont.FreeTypeFont, x_offset: int, y_offset: int) -> Image.Image:
    canvas = Image.new("RGB", (256, 256), "white")
    draw = ImageDraw.Draw(canvas)
    box = draw.textbbox((0, 0), char, font=font)
    x = (256 - (box[2] - box[0])) // 2 - box[0] + x_offset
    y = (256 - (box[3] - box[1])) // 2 - box[1] + y_offset
    draw.text((x, y), char, font=font, fill="black")
    return canvas


def rows_for_range(
    labels: list[dict[str, str]], images_dir: Path, start: int, stop: int
) -> list[dict[str, object]]:
    font_instances = [(name, path, None, None) for name, path in STATIC_FONTS]
    font_instances.extend(VARIABLE_FONTS)
    rows: list[dict[str, object]] = []
    for image_id in range(start, stop):
        label = labels[image_id // 400]
        variant_id = image_id % 400
        font_name, font_path, weight, width = font_instances[variant_id // len(CONTEXTS)]
        context_id, (size, x_offset, y_offset) = divmod(variant_id, len(CONTEXTS))[1], CONTEXTS[variant_id % len(CONTEXTS)]
        font = (
            static_font(font_path, size)
            if weight is None
            else variable_font(font_path, size, weight, width)
        )
        filename = f"printed_{image_id:06d}.png"
        render(label["char"], font, x_offset, y_offset).save(
            images_dir / filename, compress_level=6
        )
        rows.append(
            {
                "filename": f"images/{filename}",
                "class_id": label["class_id"],
                "tis620": label["tis620"],
                "char": label["char"],
                "name_en": label["name_en"],
                "font_instance": font_name,
                "font_file": font_path.name,
                "font_weight": weight or "embedded_static_style",
                "font_width": width or "embedded_static_style",
                "font_size_px": size,
                "x_offset_px": x_offset,
                "y_offset_px": y_offset,
                "context_id": context_id + 1,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=32_000)
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    missing = [str(path) for _, path in STATIC_FONTS if not path.exists()]
    missing += [str(path) for _, path, _, _ in VARIABLE_FONTS if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing font files:\n" + "\n".join(missing))
    if args.clean and OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    images_dir = OUTPUT / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    with LABELS.open("r", encoding="utf-8-sig", newline="") as handle:
        labels = list(csv.DictReader(handle))

    total = len(labels) * 400
    start = max(0, args.start)
    stop = min(total, start + max(0, args.count))
    if stop > start:
        rows_for_range(labels, images_dir, start, stop)
        print(f"Rendered images {start:,} through {stop - 1:,}.")
    if not args.finalize:
        return

    rows = rows_for_range(labels, images_dir, total, total)
    # Build metadata without rendering a second copy of the image set.
    font_instances = [(name, path, None, None) for name, path in STATIC_FONTS]
    font_instances.extend(VARIABLE_FONTS)
    for image_id in range(total):
        label = labels[image_id // 400]
        variant_id = image_id % 400
        font_name, font_path, weight, width = font_instances[variant_id // len(CONTEXTS)]
        context_id = variant_id % len(CONTEXTS)
        size, x_offset, y_offset = CONTEXTS[context_id]
        rows.append({"filename": f"images/printed_{image_id:06d}.png", "class_id": label["class_id"], "tis620": label["tis620"], "char": label["char"], "name_en": label["name_en"], "font_instance": font_name, "font_file": font_path.name, "font_weight": weight or "embedded_static_style", "font_width": width or "embedded_static_style", "font_size_px": size, "x_offset_px": x_offset, "y_offset_px": y_offset, "context_id": context_id + 1})

    with (OUTPUT / "ground_truth.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    coverage = [
        {
            "class_id": label["class_id"],
            "tis620": label["tis620"],
            "char": label["char"],
            "name_en": label["name_en"],
            "n_images": 400,
        }
        for label in labels
    ]
    with (OUTPUT / "class_coverage.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(coverage[0]))
        writer.writeheader()
        writer.writerows(coverage)

    unique_fonts = {path for _, path in STATIC_FONTS}
    unique_fonts.update(path for _, path, _, _ in VARIABLE_FONTS)
    manifest = {
        "dataset": "TH_Characters_PrintFont_Large_Test",
        "n_classes": len(labels),
        "n_images": len(rows),
        "images_per_class": 400,
        "n_font_instances": len(font_instances),
        "contexts_per_font_instance": len(CONTEXTS),
        "generator": "build_print_font_large_test.py",
        "font_files": [
            {"file": path.name, "sha256": sha256(path)} for path in sorted(unique_fonts)
        ],
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUTPUT / "README.md").write_text(
        """# TH_Characters_PrintFont_Large_Test

Large external evaluation set for printed Thai-character classification.

- 80 classes, 400 images per class, 32,000 PNG images total.
- Images are freshly rendered black glyphs on white 256x256 canvases from 20 font instances.
- There is no handwriting source and no course-dataset image copied into this package.
- Rendering diversity is restricted to typeface, embedded style/weight, size, and small position offsets. No handwritten stroke, noise, blur, elastic transform, or other handwriting-like augmentation is used.
- `ground_truth.csv` contains labels and rendering metadata. Keep it separate from inference input.
- Use as an external printed-font benchmark. Do not tune a model against it and then report the same score as held-out performance.

## Font source and license

All source font files came from Google Fonts and are licensed under SIL Open Font License 1.1 (OFL-1.1). Font folders are under https://github.com/google/fonts/tree/main/ofl/ :

- notosansthai, notoserifthai, notosansthailooped
- kanit, prompt, sarabun, baijamjuree
- chakrapetch, mitr, pridi, taviraj

The archive distributes rendered images and metadata only, not the font binaries.
""",
        encoding="utf-8",
    )

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    shutil.make_archive(str(ZIP_PATH.with_suffix("")), "zip", ROOT, OUTPUT.name)
    print(f"Created {len(rows):,} images ({len(rows) // len(labels):,} per class).")
    print(f"Created {ZIP_PATH}")


if __name__ == "__main__":
    main()
