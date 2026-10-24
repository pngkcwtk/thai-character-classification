"""Create a 500-image mock instructor test package for Project 1.

The ZIP is intentionally unlabeled. Ground truth is written outside the ZIP for
local verification only.
"""

from __future__ import annotations

import csv
import io
import random
import zipfile
from collections import defaultdict
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROOT = PROJECT_ROOT / "data" / "local"
ALICE_ROOT = ROOT / "TH_Characters_External_ALICE"
PRINT_ROOT = ROOT / "TH_Characters_PrintFont_Large_Test"
DATA_DICT = PROJECT_ROOT / "data" / "metadata" / "Project_1-data_dict.csv"
INPUT_OUTPUT = PROJECT_ROOT / "data" / "metadata" / "Project_1-InputOutput.csv"
OUTPUT_DIR = ROOT / "Project_1_Mock_Instructor_Test"
TEST_ZIP = ROOT / "PROJECT_1_MOCK_INSTRUCTOR_TEST.zip"
TEMPLATE_CSV = ROOT / "Project_1-InputOutput_MOCK.csv"
TRUTH_CSV = OUTPUT_DIR / "MOCK_ground_truth_DO_NOT_UPLOAD.csv"
SEED = 42
N_IMAGES = 500


def read_csv(path: Path) -> list[dict[str, str]]:
    for encoding in ("utf-8-sig", "cp874", "tis-620"):
        try:
            with path.open(encoding=encoding, newline="") as handle:
                return list(csv.DictReader(handle))
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Cannot decode {path}")


def read_header(path: Path) -> list[str]:
    for encoding in ("utf-8-sig", "cp874", "tis-620"):
        try:
            with path.open(encoding=encoding, newline="") as handle:
                return next(csv.reader(handle))
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Cannot decode {path}")


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    if OUTPUT_DIR.exists() or TEST_ZIP.exists() or TEMPLATE_CSV.exists():
        raise FileExistsError("Mock outputs already exist. Remove them explicitly before rebuilding.")

    dictionary_rows = [
        row for row in read_csv(DATA_DICT) if row.get("folder") and row.get("class_id")
    ]
    folder_to_class_id = {
        str(int(float(row["folder"]))): int(float(row["class_id"]))
        for row in dictionary_rows
    }
    if len(folder_to_class_id) != 72:
        raise ValueError(f"Expected 72 Project 1 classes, found {len(folder_to_class_id)}")

    source_rows = read_csv(ALICE_ROOT / "ground_truth.csv")
    by_folder: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in source_rows:
        if row["class"] in folder_to_class_id:
            row["image_path"] = str(ALICE_ROOT / "images" / row["filename"])
            by_folder[row["class"]].append(row)
    # ALICE-THI does not contain folders 225 and 229. Add those two classes from
    # the printed-font mock only so the Project 1 mapping is covered end-to-end.
    alice_folders = set(by_folder)
    for row in read_csv(PRINT_ROOT / "ground_truth.csv"):
        folder = str(row["tis620"])
        if folder in folder_to_class_id and folder not in alice_folders:
            by_folder[folder].append(
                {
                    "class": folder,
                    "char": row["char"],
                    "filename": row["filename"],
                    "source_filename": f"printed_font/{row['filename']}",
                    "image_path": str(PRINT_ROOT / row["filename"]),
                }
            )
    if set(by_folder) != set(folder_to_class_id):
        missing = sorted(set(folder_to_class_id).difference(by_folder))
        raise ValueError(f"Mock source misses Project 1 folders: {missing}")

    rng = random.Random(SEED)
    selected: list[dict[str, str]] = []
    # 68 classes receive 7 samples; 4 receive 6. Total = 500.
    for position, folder in enumerate(sorted(folder_to_class_id, key=int)):
        selected.extend(rng.sample(by_folder[folder], 7 if position < 68 else 6))
    rng.shuffle(selected)
    if len(selected) != N_IMAGES:
        raise AssertionError(f"Expected {N_IMAGES}, got {len(selected)}")

    OUTPUT_DIR.mkdir()
    truth_rows: list[dict[str, object]] = []
    with zipfile.ZipFile(TEST_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for number, row in enumerate(selected, start=1):
            filename = f"ts_img_{number:03d}.jpg"
            with Image.open(row["image_path"]) as image:
                rgb = image.convert("RGB")
                buffer = io.BytesIO()
                rgb.save(buffer, format="JPEG", quality=95, optimize=True)
            archive.writestr(f"test_dataset/{filename}", buffer.getvalue())
            truth_rows.append(
                {
                    "gt_path": f"./test_dataset/ts_img_{number:03d}",
                    "gt_label": row["char"],
                    "gt_class_id": folder_to_class_id[row["class"]],
                    "source_filename": row["source_filename"],
                }
            )

    template_headers = read_header(INPUT_OUTPUT)
    if "test" not in template_headers:
        raise ValueError("Project_1-InputOutput.csv has no 'test' column")
    with TEMPLATE_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=template_headers)
        writer.writeheader()
        for row in truth_rows:
            output_row = {header: "" for header in template_headers}
            output_row["gt_path"] = row["gt_path"]
            writer.writerow(output_row)

    with TRUTH_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(truth_rows[0]))
        writer.writeheader()
        writer.writerows(truth_rows)

    (OUTPUT_DIR / "README.txt").write_text(
        "MOCK instructor test for pipeline verification only.\n"
        "Use PROJECT_1_MOCK_INSTRUCTOR_TEST.zip as TEST_ZIP_PATH and\n"
        "Project_1-InputOutput_MOCK.csv as SUBMISSION_TEMPLATE_PATH.\n"
        "Do not submit this mock package to the instructor.\n"
        "MOCK_ground_truth_DO_NOT_UPLOAD.csv is kept outside the ZIP for local scoring.\n",
        encoding="utf-8",
    )
    print(f"Created: {TEST_ZIP}")
    print(f"Created: {TEMPLATE_CSV}")
    print(f"Created: {TRUTH_CSV}")


if __name__ == "__main__":
    main()
