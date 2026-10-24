<div align="center">

# 🇹🇭 Thai Character Classification

### จำแนกตัวอักษรไทยด้วย MobileNetV3-Large

ฝึกโมเดล · ประเมินผล · สร้างไฟล์ส่งคำตอบ

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-MobileNetV3--Large-EE4C2C?logo=pytorch&logoColor=white)
![Classes](https://img.shields.io/badge/Thai_characters-80_classes-0F766E)
[![License: MIT](https://img.shields.io/badge/Code_license-MIT-64748B)](LICENSE)

[เริ่มใช้งาน](#-เริ่มใช้งานบน-google-colab) · [ชุดข้อมูล](#-ชุดข้อมูลและผลประเมิน) · [โครงสร้าง](#-โครงสร้างโครงการ) · [เอกสาร](#-เอกสารเพิ่มเติม)

</div>

---

## 📖 เกี่ยวกับโครงการ

โครงการ Deep Learning สำหรับจำแนกตัวอักษรไทย **80 คลาส** ด้วย **PyTorch** และ
**MobileNetV3-Large** โดยใช้ Transfer Learning จาก ImageNet มี notebook สำหรับ
Google Colab ครบตั้งแต่การฝึกโมเดล การประเมิน checkpoint ไปจนถึงการสร้างไฟล์ส่งคำตอบ
พร้อมสคริปต์สร้างชุดทดสอบตัวพิมพ์และชุดทดสอบจำลอง

| ความสามารถ | รายละเอียด |
| :--- | :--- |
| ฝึกโมเดล | ฝึก classifier แล้ว fine-tune backbone เป็นสองช่วง |
| เตรียมภาพ | ภาพ RGB ขนาด 160 × 160 พิกเซล รักษาสัดส่วนด้วยพื้นหลังสีขาว |
| ประเมินผล | สร้างคำทำนาย และคำนวณตัวชี้วัดเมื่อมีเฉลย |
| ส่งคำตอบ | สร้างไฟล์ `submission.csv` ตามแม่แบบของ Project 1 |
| สร้างชุดทดสอบ | สร้างภาพตัวพิมพ์ ชุดทดสอบจำลอง และภาพตัวอย่าง |

> **ก่อนเริ่ม:** repository นี้มีโค้ดและเอกสาร ส่วนชุดข้อมูล checkpoint และฟอนต์
> ต้องเตรียมแยกต่างหาก ดู [คู่มือข้อมูล](data/README.md) และ [คู่มือโมเดล](models/README.md)

## 🚀 เริ่มใช้งานบน Google Colab

### 1. เลือกงานที่ต้องการ

| ขั้นตอน | Notebook | เปิดใช้งาน |
| :---: | :--- | :---: |
| **01 · ฝึกโมเดล** | [ฝึก MobileNetV3-Large](notebooks/person3_mobilenetv3_colab.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pngkcwtk/thai-character-classification/blob/main/notebooks/person3_mobilenetv3_colab.ipynb) |
| **02 · ประเมินผล** | [ประเมิน checkpoint](notebooks/person3_mobilenetv3_evaluation_colab.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pngkcwtk/thai-character-classification/blob/main/notebooks/person3_mobilenetv3_evaluation_colab.ipynb) |
| **03 · ส่งคำตอบ** | [สร้างไฟล์ submission](notebooks/person3_mobilenetv3_submission_colab.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pngkcwtk/thai-character-classification/blob/main/notebooks/person3_mobilenetv3_submission_colab.ipynb) |

> Repository แบบ **Private** อาจต้องเปิดผ่านเมนู GitHub ใน Colab และอนุญาตการเข้าถึง
> หรือดาวน์โหลดไฟล์ `.ipynb` แล้วอัปโหลดเข้า Colab ด้วยตนเอง

### 2. เตรียมไฟล์ใน Google Drive

Notebook ใช้ตำแหน่งไฟล์บน Drive ดังตาราง สามารถแก้ตัวแปรใน cell ตั้งค่าให้ตรงกับไฟล์ของตนเองได้

| ไฟล์ | ตำแหน่งเริ่มต้นภายใต้ `/content/drive/MyDrive/dl/` |
| :--- | :--- |
| ชุดข้อมูลฝึก | `TH_Characters.zip` |
| โมเดลที่ฝึกแล้ว | `thai_char_person3_outputs/mobilenetv3_large_best.pt` |
| รายการคลาส | `person3_evaluation/labels.csv` |
| ตารางเทียบรหัส Project 1 | `Project_1-data_dict.csv` |
| แม่แบบส่งคำตอบ | `Project_1-InputOutput.csv` |

ไฟล์รายการคลาส ตารางเทียบรหัส และแม่แบบส่งคำตอบอยู่ใน [`data/metadata/`](data/metadata/)
ส่วนชุดข้อมูลและ checkpoint ให้ใช้ไฟล์เดิมในเครื่องหรือขอจากเจ้าของข้อมูล
ปัจจุบันยังไม่มีลิงก์ดาวน์โหลดสาธารณะในโครงการ

### 3. ตั้งค่าแล้วรัน

1. เลือก GPU runtime ใน Colab แล้วเชื่อมต่อ Google Drive ตาม cell แรก
2. แก้ตำแหน่งข้อมูล โมเดล ชุดทดสอบ และโฟลเดอร์ผลลัพธ์ใน cell ตั้งค่า
3. รัน cell ตามลำดับของ notebook ที่เลือก
4. ตรวจรายการคลาส ชื่อคอลัมน์กลุ่ม และแม่แบบก่อนส่ง `submission.csv`

> **การเทียบคลาส:** โมเดลมี 80 คลาส แต่ Project 1 ใช้ตารางส่งคำตอบ 72 คลาส
> ให้อ้างอิง `class_to_idx` ใน checkpoint และ dictionary ของงาน ห้ามสลับใช้แทนกันโดยตรง

## 📊 ชุดข้อมูลและผลประเมิน

### ผลที่บันทึกไว้เดิม

| ตัวชี้วัด | ผล | ขอบเขต |
| :--- | ---: | :--- |
| Validation accuracy สูงสุด | **99.54%** | ค่าจาก model card เดิม |
| Mock accuracy | **99.50%** | ชุดจำลองที่เป็นส่วนหนึ่งของ validation |

> ค่าข้างต้นอ้างอิง [model card](docs/evaluation/model_card.json)
> ยังไม่ได้รันประเมินใหม่จากการจัด repository และ **ไม่ใช่ผลทดสอบกับข้อมูลที่โมเดลไม่เคยเห็นทั้งหมด**

### ชุดทดสอบที่เตรียมไว้

| ชุดข้อมูล | ลักษณะ | การตีความผล |
| :--- | :--- | :--- |
| Test 5% เดิม | ชุดจำลองที่มีอยู่ในโครงการ | อ่านที่มาและข้อจำกัดใน README ของชุดข้อมูล |
| ALICE-THI | ตัวอักษรลายมือจากแหล่งภายนอก | ครอบคลุม 77 จาก 80 คลาส |
| PrintFont Test | ตัวอักษรที่สร้างจากฟอนต์ | วัดความสามารถกับตัวพิมพ์ |
| PrintFont Large Test | ตัวพิมพ์ 32,000 ภาพ / 80 คลาส | วัดผลแยกจากชุดลายมือ |
| Project 1 Mock Test | ชุดจำลองสำหรับขั้นตอนส่งงาน | เก็บเฉลยแยกจากไฟล์นำเข้า |

ควรรายงานผลของแต่ละชุดแยกกัน และไม่นำผลทดสอบกลับไปปรับโมเดลแล้วรายงานเป็นผลทดสอบอิสระ

<details>
<summary><strong>ดูตัวอย่างภาพจากชุดทดสอบ</strong></summary>

#### ตัวอย่างลายมือ ALICE-THI — ก

![ตัวอย่างลายมือ ก จากชุด ALICE-THI](docs/images/ALICE_THI_kor_kai_grid.png)

#### ตัวอย่างภาพตัวพิมพ์

![ตัวอย่างชุดทดสอบตัวพิมพ์](docs/images/TH_Characters_PrintFont_Large_Test_preview.png)

</details>

## 🗂️ โครงสร้างโครงการ

```text
thai-character-classification/
├── notebooks/              # ฝึกโมเดล · ประเมินผล · สร้างไฟล์ส่งคำตอบ
├── scripts/                # สคริปต์สร้างชุดทดสอบและภาพตัวอย่าง
├── data/
│   ├── metadata/           # รายการคลาส ตารางเทียบรหัส และแม่แบบ
│   └── README.md           # คู่มือเตรียมข้อมูล
├── models/README.md        # คู่มือเตรียม checkpoint
├── docs/
│   ├── evaluation/         # รายละเอียดโมเดลและบันทึกการฝึก
│   ├── images/             # ภาพประกอบ
│   └── slide_dl_presentation.pdf
├── requirements.txt        # ไลบรารี Python ที่ใช้
├── .gitignore              # กฎยกเว้นไฟล์ในเครื่อง
├── .gitattributes          # กำหนดชนิดไฟล์ภาพและ PDF ให้ Git
├── LICENSE                 # MIT สำหรับโค้ดและเอกสารที่ทีมสร้าง
└── THIRD_PARTY_NOTICES.md   # ขอบเขตสิทธิ์ของเนื้อหาจากภายนอก
```

<details>
<summary><strong>โฟลเดอร์ที่เก็บเฉพาะในเครื่องและไม่ขึ้น GitHub</strong></summary>

| โฟลเดอร์ | เนื้อหา |
| :--- | :--- |
| `data/local/` | ชุดข้อมูลและผลสร้างชุดทดสอบ |
| `models/` ยกเว้น README | checkpoint ของโมเดล |
| `assets/fonts/` | ฟอนต์สำหรับสร้างภาพ |
| `archives/` | ไฟล์ ZIP ต้นฉบับ |
| `results/submissions/` | ผลส่งคำตอบเดิม |
| `notebooks/legacy/` | notebook เก่าและเวอร์ชันทดลอง |
| `archive_local/` | ไฟล์จาก Drive export และประวัติการจัดไฟล์ |

โฟลเดอร์เหล่านี้จะไม่ปรากฏเมื่อ clone ใหม่ ต้องเตรียมไฟล์ที่จำเป็นตามงานที่ต้องการรัน

</details>

## 💻 ใช้งานสคริปต์ในเครื่อง

### ติดตั้ง

ต้องใช้ **Python 3.10 ขึ้นไป** จากนั้น clone โครงการและสร้าง environment:

```bash
git clone https://github.com/pngkcwtk/thai-character-classification.git
cd thai-character-classification
python -m venv .venv
```

เปิดใช้งาน environment ให้ตรงกับระบบ:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` รวบรวมแพ็กเกจจากโค้ดเดิม ยังไม่มี lockfile ของ environment ต้นฉบับ
ส่วน `google.colab` ใช้งานภายใน Colab เท่านั้น

### เลือกสคริปต์

รันคำสั่งจากโฟลเดอร์หลักของโครงการ โดยเตรียมฟอนต์ `.ttf` ใน `assets/fonts/`
ตามชื่อที่สคริปต์ระบุ และตรวจไฟล์นำเข้าตามตารางก่อนรัน

| งาน | คำสั่ง | สิ่งที่ต้องเตรียม |
| :--- | :--- | :--- |
| สร้างชุดตัวพิมพ์ขนาดเล็ก | `python scripts/build_print_font_test.py` | รายการคลาสและฟอนต์ |
| สร้างชุดตัวพิมพ์ขนาดใหญ่ | `python scripts/build_print_font_large_test.py --finalize` | รายการคลาสและฟอนต์ |
| สร้างชุดจำลอง Project 1 | `python scripts/build_project1_mock_test.py` | ALICE, PrintFont Large, dictionary และ template |
| สร้างภาพตัวอย่าง ALICE | `python scripts/make_alice_preview.py` | ชุด ALICE ที่แตกไฟล์แล้ว |

- ชุดข้อมูลและ ZIP ที่สร้างใหม่อยู่ใน `data/local/` ส่วนภาพตัวอย่าง ALICE อยู่ใน `docs/images/`
- สคริปต์ชุดตัวพิมพ์ขนาดเล็กจะหยุดเมื่อมีโฟลเดอร์ผลลัพธ์เดิมอยู่
- สคริปต์ขนาดใหญ่รองรับ `--start` และ `--count` เพื่อแบ่งรอบ และใช้ `--finalize` เพื่อสร้าง metadata และ ZIP
- `--clean` ของสคริปต์ขนาดใหญ่จะลบผลลัพธ์ชุด Large เดิมก่อนสร้างใหม่
- ผล mock ที่สร้างใหม่อยู่ใน `data/local/` ส่วนผลส่งคำตอบเดิมอยู่ใน `results/submissions/`

## 📚 เอกสารเพิ่มเติม

| เอกสาร | เนื้อหา |
| :--- | :--- |
| [คู่มือข้อมูล](data/README.md) | ตำแหน่งและหน้าที่ของชุดข้อมูล |
| [คู่มือโมเดล](models/README.md) | การเตรียม checkpoint สำหรับใช้งาน |
| [รายละเอียดโมเดล](docs/evaluation/model_card.json) | สถาปัตยกรรม การเตรียมภาพ และผลที่บันทึกไว้ |
| [สไลด์นำเสนอ](docs/slide_dl_presentation.pdf) | เอกสารนำเสนอโครงการ |
| [บันทึกการจัดไฟล์](docs/cleanup_manifest.json) | ตำแหน่งเดิม/ใหม่และ SHA-256 ของสำเนาที่ลบ |
| [รายการไฟล์ต้นฉบับ](docs/original_inventory.csv) | รายการไฟล์ก่อนจัดโครงสร้าง |
| [บันทึกการตรวจสอบ](docs/verification.md) | ขอบเขตการตรวจโค้ดและไฟล์ |

## 📄 สิทธิ์การใช้งาน

โค้ดและเอกสารที่ทีมสร้างเผยแพร่ภายใต้ **[MIT License](LICENSE)**
ส่วนชุดข้อมูล ฟอนต์ โมเดล และเอกสารจากบุคคลอื่นมีเงื่อนไขสิทธิ์แยกต่างหาก
ตาม **[ข้อกำหนดเนื้อหาจากภายนอก](THIRD_PARTY_NOTICES.md)**
