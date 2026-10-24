> เอกสารส่งต่อเดิม: โครงสร้างไฟล์ในเอกสารนี้เป็นโครงสร้างก่อนจัด repository
> สำหรับ path ปัจจุบันดู [README หลัก](../../README.md) และ [Model guide](../../models/README.md)

# Person 3 - MobileNetV3 Evaluation Package

ไฟล์สำหรับส่งต่อให้ทีม Evaluation โดยไม่ต้องใช้ชุด Train หรือรันการฝึกใหม่

## ส่งให้ทีม Eva

1. `person3_mobilenetv3_evaluation_colab.ipynb`
2. `labels.csv`
3. `mobilenetv3_large_best.pt` จาก Google Drive

ค่าเริ่มต้นใน notebook คาดว่าไฟล์โมเดลอยู่ที่:

`/content/drive/MyDrive/dl/thai_char_person3_outputs/mobilenetv3_large_best.pt`

ทีม Eva แก้เฉพาะ `TEST_ZIP_PATH` หรือ `TEST_FOLDER_PATH` ให้ตรงกับชุด Test แล้ว
กด Run all ได้เลย Notebook จะสร้าง `predictions.csv` เสมอ และจะสร้าง Accuracy,
F1, classification report และ confusion matrix เมื่อพบ `ground_truth.csv` หรือเมื่อ
ชุด Test แบ่งโฟลเดอร์ตามรหัสคลาส

## Model contract

- Architecture: MobileNetV3-Large
- Outputs: 80 classes
- Input: RGB 160 x 160
- Resize: white letterbox, no stretching
- Normalization: ImageNet mean/std
- Class order: stored in checkpoint key `class_to_idx`
- Checkpoint selection: highest validation accuracy

ทีม Eva ควรใช้ Test ชุดเดียวกันกับทั้งสามโมเดล และไม่ส่งผล Test กลับมาเพื่อปรับ
โมเดลหรือ hyperparameters ก่อนสรุปอันดับ
