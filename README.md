# Thai Character Classification — MobileNetV3-Large

โปรเจกต์ Deep Learning สำหรับจำแนกตัวอักษรไทย 80 คลาสด้วย PyTorch และ
MobileNetV3-Large มี notebook สำหรับฝึกโมเดล ประเมินผล และสร้างไฟล์ submission
บน Google Colab รวมถึงสคริปต์สร้างชุดทดสอบตัวพิมพ์และ mock test

## เริ่มจากไฟล์ไหน

| งาน | ไฟล์ |
| --- | --- |
| ฝึกโมเดล | [Training notebook](notebooks/person3_mobilenetv3_colab.ipynb) |
| ประเมิน checkpoint | [Evaluation notebook](notebooks/person3_mobilenetv3_evaluation_colab.ipynb) |
| สร้าง submission | [Submission notebook](notebooks/person3_mobilenetv3_submission_colab.ipynb) |
| รายละเอียดโมเดล | [Model card](docs/evaluation/model_card.json) |
| จัดเตรียมข้อมูล | [Data guide](data/README.md) |

## โครงสร้าง

```text
notebooks/        notebook หลัก 3 ขั้นตอน
scripts/          สร้างชุดทดสอบและภาพตัวอย่าง
data/metadata/    labels, dictionary และ submission template
docs/             เอกสารประกอบ ภาพตัวอย่าง และบันทึกการจัดไฟล์
models/           checkpoint ในเครื่อง (ไม่ขึ้น Git)
data/local/       dataset ในเครื่อง (ไม่ขึ้น Git)
assets/fonts/     ฟอนต์สำหรับสร้างภาพ (ไม่ขึ้น Git)
archives/         ZIP ต้นฉบับในเครื่อง (ไม่ขึ้น Git)
results/          ผล submission ในเครื่อง (ไม่ขึ้น Git)
archive_local/    ไฟล์จาก Drive export ที่ต่างจากเวอร์ชันหลัก (ไม่ขึ้น Git)
notebooks/legacy/ notebook เก่าหรือเวอร์ชันทดลอง (ไม่ขึ้น Git)
```

## ใช้งานบน Google Colab

1. เปิด notebook ที่ต้องการจากตารางด้านบนใน Colab
2. เลือก GPU runtime แล้ว mount Google Drive ตาม cell แรก
3. อัปโหลดข้อมูลหรือ checkpoint ที่จำเป็นไป Drive และแก้ path ใน cell ตั้งค่า
4. รัน cell ตามลำดับ ตรวจชื่อคลาสและ submission template ก่อนนำผลไปส่ง

Notebook ใช้ path บน Drive เดิม ไม่ใช่ path ของโฟลเดอร์ใน repository นี้:

- Training ZIP: `/content/drive/MyDrive/dl/TH_Characters.zip`
- Checkpoint: `/content/drive/MyDrive/dl/thai_char_person3_outputs/mobilenetv3_large_best.pt`
- Evaluation labels: `/content/drive/MyDrive/dl/person3_evaluation/labels.csv`
  (อัปโหลดจาก `data/metadata/labels.csv`)
- Test ZIP/folder และ output: แก้ค่าที่ต้น notebook ตามชุดที่ต้องการใช้
- Submission notebook: ตั้งค่า checkpoint, test input, dictionary และ template
  ให้ตรงกับตัวแปรใน cell ตั้งค่าของ notebook

ข้อมูลและโมเดลไม่ได้รวมในการ clone repository และยังไม่มีลิงก์ดาวน์โหลดสาธารณะ
ให้ใช้ไฟล์เดิมในเครื่องหรือขอจากเจ้าของข้อมูล ดู [ขอบเขตสิทธิ์](THIRD_PARTY_NOTICES.md)

## รันสคริปต์ในเครื่อง

ต้องใช้ Python 3.10 ขึ้นไป ติดตั้ง dependencies:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

requirements เป็นรายการแพ็กเกจจากโค้ดเดิม ยังไม่มี lockfile ของ environment ต้นฉบับ
ส่วน `google.colab` ใช้ใน Colab เท่านั้น

เตรียม `data/metadata/labels.csv` และฟอนต์ `.ttf` ใน `assets/fonts/` ตามชื่อที่ระบุ
ในสคริปต์ แล้วรันจาก root ของโปรเจกต์:

```bash
python scripts/build_print_font_test.py
python scripts/build_print_font_large_test.py --finalize
python scripts/build_project1_mock_test.py
python scripts/make_alice_preview.py
```

สคริปต์สร้าง dataset และ ZIP ใน `data/local/` ตัวเล็กจะหยุดถ้ามี output เดิม
ตัว Large รองรับ `--start`, `--count` สำหรับแบ่งรอบ และต้องใช้ `--finalize` เพื่อสร้าง
metadata/ZIP โดย `--clean` จะลบ output Large เดิมก่อนสร้างใหม่
สคริปต์ mock test ต้องใช้ชุด ALICE และ PrintFont
Large ที่แตกไฟล์ไว้แล้ว พร้อม dictionary/template ใน `data/metadata/`
ผล mock ใหม่อยู่ใน `data/local/` ส่วนผลเดิมที่ย้ายมาจาก root อยู่ใน `results/submissions/`

## ขอบเขตผลประเมิน

โมเดลใช้ภาพ RGB 160×160 แบบ white letterbox และ ImageNet normalization
ลำดับคลาสอ้างอิง `class_to_idx` ใน checkpoint ไม่ควรเดาจากลำดับชื่อไฟล์
ค่า validation accuracy ใน model card เดิมคือ 99.54% และ mock accuracy 99.50%
เป็นค่าที่บันทึกไว้เดิม ไม่ใช่ผลรันทดสอบใหม่จากการจัด repository ครั้งนี้
mock set เป็นส่วนหนึ่งของ validation ตามคำเตือนใน model card จึงไม่ใช่ unseen test
ชุด ALICE ครอบคลุม 77 จาก 80 คลาส ส่วน printed-font test เป็นข้อมูลตัวพิมพ์
ควรรายงานผลแต่ละชุดแยกกัน

## เตรียมขึ้น GitHub

```bash
git init
git add .
git status --short
git diff --cached --stat
git commit -m "Organize Thai character classification project"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

ตรวจรายการ staged ก่อน commit: `.gitignore` แยก dataset, ZIP, checkpoint,
ฟอนต์, notebook เก่า และผล submission ออกไว้ในเครื่องแล้ว
ยังไม่ได้สร้าง remote หรืออัปโหลดขึ้น GitHub จากการจัดไฟล์ครั้งนี้

## การจัดไฟล์และ License

[Cleanup manifest](docs/cleanup_manifest.json) บันทึก path เดิม/ใหม่และ SHA-256
ของสำเนาที่ลบ ส่วน [Original inventory](docs/original_inventory.csv) เป็นรายการ
ไฟล์ก่อนจัดโฟลเดอร์ เก็บเวอร์ชันที่เนื้อหาต่างกันไว้ ไม่ลบภาพซ้ำภายใน dataset
และล้าง output ของ notebook หลักเพื่อให้อ่าน diff ได้ง่าย

เลือกใช้ [MIT License](LICENSE) สำหรับโค้ดและเอกสารที่ทีมเป็นผู้สร้าง
dataset, ฟอนต์ และเอกสารของบุคคลอื่นมีสิทธิ์แยกตาม
[Third-party notices](THIRD_PARTY_NOTICES.md)
