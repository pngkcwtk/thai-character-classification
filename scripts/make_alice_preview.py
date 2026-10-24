"""Create a labeled contact sheet from the packaged ALICE-THI examples."""

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1] / "data" / "local" / "TH_Characters_External_ALICE"
OUT = Path(__file__).resolve().parents[1] / "docs" / "images" / "ALICE_THI_kor_kai_grid.png"
TARGET_CHARACTER = "ก"


def main() -> None:
    with (ROOT / "ground_truth.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    selected = [row for row in rows if row["char"] == TARGET_CHARACTER][:20]
    if len(selected) != 20:
        raise RuntimeError(f"Expected 20 samples for {TARGET_CHARACTER}, found {len(selected)}")

    columns, cell, border = 5, 128, 4
    canvas = Image.new("RGB", (columns * cell, 4 * cell), "white")
    for index, row in enumerate(selected):
        image = Image.open(ROOT / "images" / row["filename"]).convert("RGB")
        image.thumbnail((96, 96))
        x = (index % columns) * cell + (cell - image.width) // 2
        y = (index // columns) * cell + (cell - image.height) // 2
        canvas.paste(image, (x, y))

    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, canvas.width - 1, canvas.height - 1), outline="#8957ff", width=border)

    canvas.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
