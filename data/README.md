# Data placement

`metadata/` contains the 80-class model labels and the Project 1 dictionary and
submission template. Project 1 uses a separate 72-class submission mapping;
do not substitute one mapping for the other.

`local/` is ignored by Git. Existing datasets were moved here without deleting
duplicate image samples or changing their internal filenames:

| Folder | Purpose |
| --- | --- |
| TH_Characters_Test_5pct | Existing 5% mock evaluation set; see its README |
| TH_Characters_External_ALICE | External handwritten samples |
| TH_Characters_PrintFont_Test | Small printed-font benchmark |
| TH_Characters_PrintFont_Large_Test | Large printed-font benchmark |
| test_dataset | Supplied inference images |
| Project_1_Mock_Instructor_Test | Mock submission truth and notes |
| external_data | Original external source material |
| source_sample, preview_samples | Source and preview samples |

Original ZIP downloads are in `archives/`. They remain local as source packages;
an extracted dataset and its ZIP serve different purposes. No public dataset
download was provided. A fresh clone needs separately obtained data and fonts.

Local scripts create new dataset ZIPs beside their output folders in `local/`.
