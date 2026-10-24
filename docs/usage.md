# คู่มือใช้งาน

[กลับไปหน้าหลัก](../README.md)



## เตรียมไฟล์บน Google Drive

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



## ติดตั้งและรันสคริปต์ในเครื่อง

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



## ไฟล์ที่เก็บเฉพาะในเครื่อง

ชุดข้อมูล (`data/local/`), checkpoint (`models/`), ฟอนต์ (`assets/fonts/`),
ZIP (`archives/`), ผลส่งคำตอบ (`results/submissions/`), notebook เก่า
(`notebooks/legacy/`) และ Drive export (`archive_local/`) ถูกยกเว้นด้วย `.gitignore`
จึงไม่รวมอยู่เมื่อ clone โครงการ

บันทึกการจัดไฟล์: [รายการย้ายและลบสำเนา](cleanup_manifest.json),
[รายการไฟล์เดิม](original_inventory.csv) และ [ผลการตรวจสอบ](verification.md)




## ตั้งค่าก่อนสร้างไฟล์ส่งคำตอบ

1. ตั้ง `MODEL_PATH`, `DATA_DICT_PATH` และ `SUBMISSION_TEMPLATE_PATH` ให้ตรงกับไฟล์บน Drive
2. ตั้ง `TEST_ZIP_PATH` หรือ `TEST_FOLDER_PATH` ให้เป็นชุดที่ต้องการทำนาย
3. เปลี่ยน `TEAM_COLUMN` ให้ตรงกับชื่อคอลัมน์กลุ่มใน template
4. รันตามลำดับ แล้วตรวจ `submission.csv` และ `submission_detailed.csv`

Notebook ส่งงานกรอง logits ให้เหลือ 72 คลาสตาม dictionary ก่อนเลือกคำตอบ
จากนั้นเทียบชื่อไฟล์กับ `gt_path` ใน template โดยรองรับการเทียบเลขท้ายชื่อไฟล์
และตรวจจำนวนภาพ จำนวนแถว และชื่อไฟล์ซ้ำก่อนสร้างผลลัพธ์
ค่าที่ส่งเป็น `class_id` ของ Project 1 ไม่ใช่ TIS-620 หรือ model index

## ผลลัพธ์จาก notebook ประเมิน

`predictions.csv` เก็บคำทำนายและความมั่นใจรายภาพ ส่วน `evaluation_summary.json`
เก็บจำนวนภาพ เวลา inference และ SHA-256 ของ checkpoint
เมื่อมีเฉลยจะสร้าง `classification_report.csv`, `scored_predictions.csv`,
`confusion_matrix.png` และ `top_confusions.csv` เพิ่มด้วย

เฉลยรองรับ `ground_truth.csv` หรือโฟลเดอร์ที่ตั้งชื่อตามคลาสของโมเดล
หากไม่มีเฉลยยังสร้างคำทำนายได้ แต่จะไม่คำนวณตัวชี้วัด

## การเตรียมภาพให้ตรงกับตอนฝึก

ใช้ภาพ RGB ขนาด 160 × 160 พิกเซล เติมขอบสีขาวแบบ letterbox
และ normalize ด้วย ImageNet mean `[0.485, 0.456, 0.406]`
และ standard deviation `[0.229, 0.224, 0.225]`
Evaluation อ่านขนาดภาพและลำดับคลาสจาก checkpoint โดยตรง
