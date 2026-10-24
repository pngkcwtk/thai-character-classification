# จำแนกตัวอักษรไทยด้วย MobileNetV3-Large

โครงการจำแนกตัวอักษรไทย 80 คลาสด้วย PyTorch และ Transfer Learning จาก ImageNet
มีโค้ดสำหรับฝึกโมเดล ประเมินผล และสร้างไฟล์ส่งคำตอบบน Google Colab

## เริ่มใช้งาน

เลือก notebook ตามงานที่ต้องการ:

1. [ฝึกโมเดล](notebooks/person3_mobilenetv3_colab.ipynb)
2. [ประเมินผล](notebooks/person3_mobilenetv3_evaluation_colab.ipynb)
3. [สร้างไฟล์ส่งคำตอบ](notebooks/person3_mobilenetv3_submission_colab.ipynb)

เปิดไฟล์ใน Google Colab เลือก GPU runtime เชื่อมต่อ Google Drive
แล้วแก้ตำแหน่งไฟล์ใน cell ตั้งค่าก่อนรันตามลำดับ

ชุดข้อมูล โมเดลที่ฝึกแล้ว และฟอนต์ไม่ได้รวมอยู่ใน repository
ดูวิธีเตรียมไฟล์ได้ที่ [คู่มือข้อมูล](data/README.md) และ [คู่มือโมเดล](models/README.md)

## โครงสร้างโครงการ

```text
notebooks/          ฝึกโมเดล ประเมินผล และสร้างไฟล์ส่งคำตอบ
scripts/            สร้างชุดทดสอบและภาพตัวอย่าง
data/metadata/      รายการคลาส ตารางเทียบรหัส และแม่แบบส่งคำตอบ
docs/               รายละเอียดโมเดล ภาพประกอบ และสไลด์นำเสนอ
models/README.md    คู่มือเตรียมโมเดล
requirements.txt    ไลบรารีที่ใช้
```

## ผลประเมิน

ผลที่บันทึกใน [รายละเอียดโมเดล](docs/evaluation/model_card.json):

- Validation accuracy: **99.54%**
- Mock accuracy: **99.50%**

ชุด mock เป็นส่วนหนึ่งของ validation จึงไม่ใช่ผลทดสอบกับข้อมูลใหม่ที่แยกอิสระ
ค่าข้างต้นเป็นบันทึกเดิม ยังไม่ได้รันประเมินใหม่จากการจัด repository
ส่วนชุด ALICE ครอบคลุม 77 จาก 80 คลาส และชุดตัวพิมพ์ควรรายงานผลแยกจากชุดลายมือ

## รายละเอียดการใช้งาน

<details>
<summary>เตรียมไฟล์บน Google Drive</summary>

วางไฟล์ภายใต้ `/content/drive/MyDrive/dl/` หรือตั้งค่า path ใหม่ใน notebook:

```text
TH_Characters.zip
thai_char_person3_outputs/mobilenetv3_large_best.pt
person3_evaluation/labels.csv
Project_1-data_dict.csv
Project_1-InputOutput.csv
```

รายการคลาส ตารางเทียบรหัส และแม่แบบอยู่ใน `data/metadata/`
ส่วนชุดข้อมูลและ checkpoint ต้องเตรียมแยกเอง ยังไม่มีลิงก์ดาวน์โหลดสาธารณะ
ตั้งค่าไฟล์ทดสอบและตำแหน่งผลลัพธ์ให้ตรงกับงานใน notebook

โมเดลมี 80 คลาส แต่ Project 1 ใช้ตารางส่งคำตอบ 72 คลาส
ให้อ้างอิง `class_to_idx` ใน checkpoint และ dictionary ของงานในการเทียบรหัส

</details>

<details>
<summary>ติดตั้งและรันสคริปต์ในเครื่อง</summary>

ใช้ Python 3.10 ขึ้นไป และรันจากโฟลเดอร์หลักของโครงการ:

```bash
python -m venv .venv
```

เปิดใช้งาน environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

ติดตั้งไลบรารี:

```bash
python -m pip install -r requirements.txt
```

เตรียมฟอนต์ใน `assets/fonts/` ตามชื่อในสคริปต์ แล้วเลือกคำสั่งที่ต้องการ:

```bash
python scripts/build_print_font_test.py
python scripts/build_print_font_large_test.py --finalize
python scripts/build_project1_mock_test.py
python scripts/make_alice_preview.py
```

สคริปต์ mock ต้องใช้ชุด ALICE และ PrintFont Large ที่แตกไฟล์แล้ว
พร้อม dictionary และ template ใน `data/metadata/`
ชุดข้อมูลและ ZIP ที่สร้างใหม่อยู่ใน `data/local/` ส่วนภาพตัวอย่าง ALICE อยู่ใน `docs/images/`

สคริปต์ตัวพิมพ์ขนาดเล็กจะหยุดเมื่อมีผลลัพธ์เดิมอยู่
ตัว Large รองรับ `--start` และ `--count` เพื่อแบ่งรอบ และต้องใช้ `--finalize`
เพื่อสร้าง metadata และ ZIP ส่วน `--clean` จะลบผลลัพธ์ Large เดิมก่อนสร้างใหม่

รายการไลบรารียังไม่ได้ล็อกเวอร์ชันตาม environment ต้นฉบับ
และ `google.colab` ใช้เฉพาะบน Colab

</details>

<details>
<summary>ไฟล์ที่เก็บเฉพาะในเครื่อง</summary>

ชุดข้อมูล (`data/local/`), checkpoint (`models/`), ฟอนต์ (`assets/fonts/`),
ZIP (`archives/`), ผลส่งคำตอบ (`results/submissions/`), notebook เก่า
(`notebooks/legacy/`) และ Drive export (`archive_local/`) ถูกยกเว้นด้วย `.gitignore`
จึงไม่รวมอยู่เมื่อ clone โครงการ

บันทึกการจัดไฟล์: [รายการย้ายและลบสำเนา](docs/cleanup_manifest.json),
[รายการไฟล์เดิม](docs/original_inventory.csv) และ [ผลการตรวจสอบ](docs/verification.md)

</details>

## เอกสารและสิทธิ์การใช้งาน

[รายละเอียดโมเดล](docs/evaluation/model_card.json) ·
[สไลด์นำเสนอ](docs/slide_dl_presentation.pdf) ·
[MIT License](LICENSE) ·
[สิทธิ์ของเนื้อหาจากภายนอก](THIRD_PARTY_NOTICES.md)

MIT ครอบคลุมโค้ดและเอกสารที่ทีมสร้าง ส่วนชุดข้อมูล ฟอนต์ โมเดล
และเอกสารจากบุคคลอื่นมีเงื่อนไขสิทธิ์แยกต่างหาก
