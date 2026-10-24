"""Build a reproducible printed-Thai-character external test set."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROOT = PROJECT_ROOT / "data" / "local"
OUTPUT = ROOT / "TH_Characters_PrintFont_Test"
ZIP_PATH = ROOT / "TH_Characters_PrintFont_Test.zip"
LABELS = PROJECT_ROOT / "data" / "metadata" / "labels.csv"
FONTS = {
    "NotoSansThai": PROJECT_ROOT / "assets" / "fonts" / "NotoSansThai-Variable.ttf",
    "NotoSerifThai": PROJECT_ROOT / "assets" / "fonts" / "NotoSerifThai-Variable.ttf",
    "NotoSansThaiLooped": PROJECT_ROOT / "assets" / "fonts" / "NotoSansThaiLooped-Variable.ttf",
}

VARIANTS = (
    (300, 72.0, 118, -3, -2),
    (400, 86.0, 126, 2, -1),
    (600, 100.0, 136, -2, 2),
    (800, 100.0, 146, 2, 1),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def make_font(path: Path, size: int, weight: int, width: float) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(path, size=size)
    axes = font.get_variation_axes()
    values = [axis["default"] for axis in axes]
    for index, axis in enumerate(axes):
        name = axis["name"].decode("ascii", errors="ignore").lower()
        if "weight" in name:
            values[index] = weight
        elif "width" in name:
            values[index] = width
    font.set_variation_by_axes(values)
    return font


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        raise FileExistsError(f"Output already exists: {OUTPUT}. Move it before rebuilding.")
    OUTPUT.mkdir()
    images_dir = OUTPUT / "images"
    images_dir.mkdir()

    with LABELS.open("r", encoding="utf-8-sig", newline="") as handle:
        labels = list(csv.DictReader(handle))

    rows: list[dict[str, object]] = []
    image_number = 0
    for label in labels:
        for family, font_path in FONTS.items():
            for variant, (weight, width, size, x_offset, y_offset) in enumerate(VARIANTS, start=1):
                font = make_font(font_path, size, weight, width)
                canvas = Image.new("RGB", (256, 256), "white")
                draw = ImageDraw.Draw(canvas)
                box = draw.textbbox((0, 0), label["char"], font=font)
                glyph_width = box[2] - box[0]
                glyph_height = box[3] - box[1]
                x = (256 - glyph_width) // 2 - box[0] + x_offset
                y = (256 - glyph_height) // 2 - box[1] + y_offset
                draw.text((x, y), label["char"], font=font, fill="black")

                filename = f"printed_{image_number:05d}.png"
                canvas.save(images_dir / filename, optimize=True)
                rows.append(
                    {
                        "filename": f"images/{filename}",
                        "class_id": label["class_id"],
                        "tis620": label["tis620"],
                        "char": label["char"],
                        "name_en": label["name_en"],
                        "font_family": family,
                        "font_weight": weight,
                        "font_width": width,
                        "variant": variant,
                    }
                )
                image_number += 1

    fields = list(rows[0])
    with (OUTPUT / "ground_truth.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    coverage = []
    for label in labels:
        coverage.append(
            {
                "class_id": label["class_id"],
                "tis620": label["tis620"],
                "char": label["char"],
                "name_en": label["name_en"],
                "n_images": 12,
            }
        )
    with (OUTPUT / "class_coverage.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(coverage[0]))
        writer.writeheader()
        writer.writerows(coverage)

    font_metadata = [
        {"family": family, "file": path.name, "sha256": sha256(path)}
        for family, path in FONTS.items()
    ]
    (OUTPUT / "manifest.json").write_text(
        json.dumps(
            {
                "dataset": "TH_Characters_PrintFont_Test",
                "n_classes": len(labels),
                "n_images": len(rows),
                "images_per_class": 12,
                "generator": "build_print_font_test.py",
                "font_metadata": font_metadata,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (OUTPUT / "README.md").write_text(
        """# TH_Characters_PrintFont_Test

External synthetic test set for Thai printed-character classification.

- 80 classes, 12 images per class, 960 PNG images total.
- Generated from Noto Sans Thai, Noto Serif Thai, and Noto Sans Thai Looped.
- Each image is a newly rendered 256x256 white-background glyph. It is not copied from the course TH_Characters archive.
- Font families and rendering variants are recorded in `ground_truth.csv`; do not feed that CSV to inference code.
- Use only for external-domain evaluation. Do not tune or retrain a model against this set if reporting it as a held-out test.

## Source and license

Fonts were downloaded from the Google Fonts repository and are licensed under SIL Open Font License 1.1 (OFL-1.1):

- https://github.com/google/fonts/tree/main/ofl/notosansthai
- https://github.com/google/fonts/tree/main/ofl/notoserifthai
- https://github.com/google/fonts/tree/main/ofl/notosansthailooped

This package contains rendered images, metadata, and labels; it does not redistribute the font binaries.
""",
        encoding="utf-8",
    )

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    shutil.make_archive(str(ZIP_PATH.with_suffix("")), "zip", ROOT, OUTPUT.name)
    print(f"Created {len(rows)} images in {OUTPUT}")
    print(f"Created {ZIP_PATH}")


if __name__ == "__main__":
    main()
