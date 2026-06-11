from __future__ import annotations

import json
from pathlib import Path

import fitz
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = REPO_ROOT.parent / "GROSS標本.pdf"
IMAGE_DIR = REPO_ROOT / "assets" / "cards"
DATA_PATH = REPO_ROOT / "cards.js"

MAX_WIDTH = 1100
JPEG_QUALITY = 72
SCALE = 1.55


CARDS = [
    {"page": 3, "group": "GI tract", "answer": "Esophageal squamous cell carcinoma", "organ": "Esophagus"},
    {"page": 4, "group": "GI tract", "answer": "Gastric adenocarcinoma, diffuse type", "organ": "Stomach"},
    {"page": 5, "group": "GI tract", "answer": "Gastrointestinal stromal tumor (GIST)", "organ": "Stomach"},
    {"page": 6, "group": "GI tract", "answer": "Intussusception", "organ": "Small intestine"},
    {"page": 7, "group": "GI tract", "answer": "Intussusception", "organ": "Small intestine"},
    {"page": 8, "group": "GI tract", "answer": "Colon adenocarcinoma", "organ": "Colon"},
    {"page": 9, "group": "GI tract", "answer": "Diverticulosis", "organ": "Colon"},
    {"page": 10, "group": "GI tract", "answer": "Ulcerative colitis", "organ": "Colon"},
    {"page": 11, "group": "GI tract", "answer": "Crohn disease", "organ": "Ileum"},
    {"page": 12, "group": "Joint, soft tissue, and skin", "answer": "Desmoid-type fibromatosis", "organ": "Ileum"},
    {"page": 13, "group": "GI tract", "answer": "Familial adenomatous polyposis", "organ": "Colon / rectum"},
    {"page": 14, "group": "Joint, soft tissue, and skin", "answer": "Rhabdomyosarcoma", "organ": "Rectum / bladder"},
    {"page": 16, "group": "Cardiovascular system", "answer": "Cardiac myxoma", "organ": "Heart"},
    {"page": 17, "group": "Cardiovascular system", "answer": "Dilated cardiomyopathy", "organ": "Heart"},
    {"page": 18, "group": "Cardiovascular system", "answer": "Myocardial infarction", "organ": "Heart"},
    {"page": 20, "group": "Kidney and urinary tract", "answer": "Hydronephrosis", "organ": "Kidney"},
    {"page": 21, "group": "Kidney and urinary tract", "answer": "Non-invasive papillary urothelial carcinoma", "organ": "Kidney / renal pelvis"},
    {"page": 22, "group": "Kidney and urinary tract", "answer": "Renal cell carcinoma", "organ": "Kidney"},
    {"page": 23, "group": "Kidney and urinary tract", "answer": "Staghorn nephrolithiasis", "organ": "Kidney"},
    {"page": 24, "group": "Kidney and urinary tract", "answer": "Invasive urothelial carcinoma", "organ": "Renal pelvis"},
    {"page": 25, "group": "Kidney and urinary tract", "answer": "Adult polycystic kidney disease", "organ": "Kidney"},
    {"page": 26, "group": "Kidney and urinary tract", "answer": "Adult polycystic kidney disease", "organ": "Kidney"},
    {"page": 28, "group": "Liver and biliary tract", "answer": "Cholangiocarcinoma", "organ": "Liver"},
    {"page": 29, "group": "Liver and biliary tract", "answer": "Focal nodular hyperplasia", "organ": "Liver"},
    {"page": 30, "group": "Liver and biliary tract", "answer": "Liver hemangioma", "organ": "Liver"},
    {"page": 31, "group": "Liver and biliary tract", "answer": "Hepatocellular carcinoma", "organ": "Liver"},
    {"page": 32, "group": "Liver and biliary tract", "answer": "Cirrhosis", "organ": "Liver"},
    {"page": 34, "group": "Respiratory system", "answer": "Lung adenocarcinoma", "organ": "Lung"},
    {"page": 35, "group": "Respiratory system", "answer": "Bronchiectasis", "organ": "Lung"},
    {"page": 36, "group": "Respiratory system", "answer": "Bronchiectasis", "organ": "Lung"},
    {"page": 37, "group": "Respiratory system", "answer": "Mesothelioma", "organ": "Pleura"},
    {"page": 38, "group": "Respiratory system", "answer": "Lung squamous cell carcinoma", "organ": "Lung"},
    {"page": 39, "group": "Respiratory system", "answer": "Tuberculosis", "organ": "Lung"},
    {"page": 40, "group": "Respiratory system", "answer": "Pulmonary hamartoma", "organ": "Lung"},
    {"page": 41, "group": "Respiratory system", "answer": "Mesothelioma", "organ": "Pleura"},
    {"page": 43, "group": "Female genital system", "answer": "Peritoneal / omental carcinomatosis", "organ": "Omentum"},
    {"page": 44, "group": "Female genital system", "answer": "Ovarian fibroma", "organ": "Ovary"},
    {"page": 45, "group": "Female genital system", "answer": "Ovarian fibrothecoma", "organ": "Ovary"},
    {"page": 46, "group": "Female genital system", "answer": "Mature teratoma", "organ": "Ovary"},
    {"page": 47, "group": "Female genital system", "answer": "Mature teratoma", "organ": "Ovary"},
    {"page": 48, "group": "Female genital system", "answer": "Ovarian serous cystadenoma", "organ": "Ovary"},
    {"page": 49, "group": "Female genital system", "answer": "Ovarian serous carcinoma", "organ": "Ovary"},
    {"page": 50, "group": "Female genital system", "answer": "Ovarian serous carcinoma", "organ": "Ovary"},
    {"page": 51, "group": "Female genital system", "answer": "Ovarian mucinous cystadenoma", "organ": "Ovary"},
    {"page": 52, "group": "Female genital system", "answer": "Ovarian torsion", "organ": "Ovary"},
    {"page": 53, "group": "Female genital system", "answer": "Endometriotic cyst", "organ": "Ovary"},
    {"page": 54, "group": "Female genital system", "answer": "Ovarian / fallopian tube clear cell carcinoma", "organ": "Ovary / fallopian tube"},
    {"page": 55, "group": "Female genital system", "answer": "Molar pregnancy", "organ": "Placenta"},
    {"page": 56, "group": "Female genital system", "answer": "Placenta accreta", "organ": "Placenta"},
    {"page": 57, "group": "Female genital system", "answer": "Adenomyosis", "organ": "Uterus"},
    {"page": 58, "group": "Female genital system", "answer": "Endometrioid adenocarcinoma / endometrial carcinoma", "organ": "Uterus"},
    {"page": 59, "group": "Female genital system", "answer": "Cervical squamous cell carcinoma", "organ": "Uterus / cervix"},
    {"page": 60, "group": "Female genital system", "answer": "Leiomyoma", "organ": "Uterus"},
    {"page": 61, "group": "Female genital system", "answer": "Cervical squamous cell carcinoma", "organ": "Uterus / cervix"},
    {"page": 63, "group": "Breast", "answer": "Breast invasive carcinoma", "organ": "Breast"},
    {"page": 64, "group": "Breast", "answer": "Complex fibroadenoma", "organ": "Breast"},
    {"page": 65, "group": "Breast", "answer": "Phyllodes tumor", "organ": "Breast"},
    {"page": 67, "group": "Male genital system", "answer": "Prostate adenocarcinoma", "organ": "Prostate"},
    {"page": 68, "group": "Male genital system", "answer": "Benign prostatic hyperplasia", "organ": "Prostate"},
    {"page": 69, "group": "Male genital system", "answer": "Seminoma", "organ": "Testis"},
    {"page": 71, "group": "Pancreas", "answer": "Pancreatic ductal adenocarcinoma", "organ": "Pancreas"},
    {"page": 72, "group": "Pancreas", "answer": "Pancreatic neuroendocrine tumor", "organ": "Pancreas"},
    {"page": 73, "group": "Pancreas", "answer": "Intraductal papillary mucinous neoplasm (IPMN)", "organ": "Pancreas"},
    {"page": 74, "group": "Pancreas", "answer": "Pancreatic serous cystadenoma", "organ": "Pancreas"},
    {"page": 75, "group": "Pancreas", "answer": "Pancreatic mucinous cystic neoplasm", "organ": "Pancreas"},
    {"page": 76, "group": "Head and neck", "answer": "Pleomorphic adenoma", "organ": "Salivary gland"},
    {"page": 77, "group": "Head and neck", "answer": "Warthin tumor", "organ": "Parotid gland"},
    {"page": 78, "group": "Endocrine system", "answer": "Papillary thyroid carcinoma", "organ": "Thyroid"},
    {"page": 79, "group": "Endocrine system", "answer": "Medullary thyroid carcinoma", "organ": "Thyroid"},
    {"page": 80, "group": "Endocrine system", "answer": "Multinodular goiter", "organ": "Thyroid"},
    {"page": 81, "group": "Endocrine system", "answer": "Graves disease", "organ": "Thyroid"},
    {"page": 82, "group": "Endocrine system", "answer": "Adrenocortical adenoma", "organ": "Adrenal gland"},
    {"page": 83, "group": "Endocrine system", "answer": "Pheochromocytoma", "organ": "Adrenal gland"},
    {"page": 84, "group": "Endocrine system", "answer": "Pheochromocytoma", "organ": "Adrenal gland"},
    {"page": 86, "group": "Hematopoietic system", "answer": "Splenic lymphoma", "organ": "Spleen"},
    {"page": 87, "group": "Hematopoietic system", "answer": "Splenic lymphoma", "organ": "Spleen"},
    {"page": 88, "group": "Hematopoietic system", "answer": "Hairy cell leukemia", "organ": "Spleen"},
    {"page": 89, "group": "Hematopoietic system", "answer": "Hairy cell leukemia", "organ": "Spleen"},
    {"page": 90, "group": "Hematopoietic system", "answer": "Splenic infarction", "organ": "Spleen"},
    {"page": 91, "group": "Hematopoietic system", "answer": "Splenic lymphoma", "organ": "Spleen"},
    {"page": 92, "group": "Hematopoietic system", "answer": "Splenic low-grade B-cell lymphoma", "organ": "Spleen"},
    {"page": 93, "group": "Hematopoietic system", "answer": "Splenic hemangioma", "organ": "Spleen"},
    {"page": 94, "group": "Hematopoietic system", "answer": "Immunoblastic lymphoma", "organ": "Lymphoid tissue"},
    {"page": 95, "group": "Hematopoietic system", "answer": "Tonsillar mantle cell lymphoma", "organ": "Tonsil"},
    {"page": 96, "group": "Hematopoietic system", "answer": "Mediastinal Hodgkin lymphoma", "organ": "Mediastinum"},
    {"page": 98, "group": "Joint, soft tissue, and skin", "answer": "Gouty tophi", "organ": "Joint / soft tissue"},
    {"page": 99, "group": "Bone", "answer": "Chondrosarcoma", "organ": "Rib"},
    {"page": 100, "group": "Bone", "answer": "Chondrosarcoma", "organ": "Bone"},
    {"page": 101, "group": "Bone", "answer": "Chondrosarcoma", "organ": "Bone"},
    {"page": 102, "group": "Bone", "answer": "Chondrosarcoma", "organ": "Bone"},
    {"page": 103, "group": "Bone", "answer": "Osteochondroma", "organ": "Bone"},
    {"page": 104, "group": "Bone", "answer": "Osteochondroma", "organ": "Femur"},
    {"page": 105, "group": "Bone", "answer": "Osteochondroma", "organ": "Bone"},
    {"page": 106, "group": "Bone", "answer": "Osteosarcoma", "organ": "Bone"},
    {"page": 107, "group": "Bone", "answer": "Osteosarcoma", "organ": "Proximal tibia"},
    {"page": 108, "group": "Bone", "answer": "Osteosarcoma", "organ": "Radius"},
    {"page": 109, "group": "Bone", "answer": "Giant cell tumor of bone", "organ": "Bone"},
    {"page": 110, "group": "Bone", "answer": "Avascular necrosis", "organ": "Femoral head"},
    {"page": 111, "group": "Bone", "answer": "Fibrous dysplasia", "organ": "Rib"},
    {"page": 114, "group": "Joint, soft tissue, and skin", "answer": "Lipoma", "organ": "Soft tissue"},
    {"page": 115, "group": "Joint, soft tissue, and skin", "answer": "Liposarcoma", "organ": "Soft tissue"},
    {"page": 116, "group": "Joint, soft tissue, and skin", "answer": "Neurofibroma", "organ": "Pelvic soft tissue"},
    {"page": 118, "group": "Nervous system", "answer": "Hydrocephalus", "organ": "Cerebrum"},
    {"page": 119, "group": "Nervous system", "answer": "Cerebral metastatic carcinoma", "organ": "Cerebrum"},
    {"page": 120, "group": "Nervous system", "answer": "Glioblastoma multiforme", "organ": "Cerebrum"},
    {"page": 121, "group": "Nervous system", "answer": "Normal cerebrum", "organ": "Cerebrum"},
    {"page": 122, "group": "Nervous system", "answer": "Intraventricular hemorrhage", "organ": "Cerebrum"},
    {"page": 123, "group": "Nervous system", "answer": "Glioblastoma multiforme", "organ": "Cerebrum"},
    {"page": 124, "group": "Nervous system", "answer": "Oligodendroglioma", "organ": "Cerebrum"},
    {"page": 125, "group": "Nervous system", "answer": "Intraventricular and intracerebral hemorrhage", "organ": "Cerebrum"},
    {"page": 126, "group": "Nervous system", "answer": "Meningioma", "organ": "Meninx"},
    {"page": 128, "group": "Eye", "answer": "Retinoblastoma", "organ": "Eye"},
    {"page": 129, "group": "Eye", "answer": "Malignant melanoma", "organ": "Eye"},
    {"page": 130, "group": "Eye", "answer": "Malignant melanoma", "organ": "Eye"},
    {"page": 131, "group": "Eye", "answer": "Retinoblastoma", "organ": "Eye"},
    {"page": 133, "group": "Skin", "answer": "Angiosarcoma", "organ": "Skin"},
    {"page": 134, "group": "Skin", "answer": "Angiosarcoma", "organ": "Skin"},
]


def slugify(value: str) -> str:
    safe = []
    for char in value.lower():
        if char.isalnum():
            safe.append(char)
        else:
            safe.append("-")
    slug = "".join(safe)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def build_cards():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"Missing PDF: {PDF_PATH}")

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF_PATH)
    output_cards = []

    for index, card in enumerate(CARDS, start=1):
        page_number = card["page"]
        image_name = f"p{page_number:03d}.jpg"
        image_path = IMAGE_DIR / image_name

        if not image_path.exists():
            pix = doc[page_number - 1].get_pixmap(matrix=fitz.Matrix(SCALE, SCALE), alpha=False)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            if image.width > MAX_WIDTH:
                ratio = MAX_WIDTH / image.width
                image = image.resize((MAX_WIDTH, int(image.height * ratio)), Image.Resampling.LANCZOS)
            image.save(image_path, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)

        output_cards.append(
            {
                "id": f"card-{index:03d}",
                "page": page_number,
                "group": card["group"],
                "answer": card["answer"],
                "organ": card["organ"],
                "image": f"assets/cards/{image_name}",
                "slug": slugify(f"{card['group']}-{card['answer']}-{page_number}"),
            }
        )

    groups = []
    for card in output_cards:
        if card["group"] not in groups:
            groups.append(card["group"])

    payload = {
        "title": "Path Gross Flashcards",
        "subtitle": "Swipe right for familiar, left for unfamiliar. Tap the card to reveal the diagnosis.",
        "groups": groups,
        "cards": output_cards,
    }

    DATA_PATH.write_text(
        "window.PATH_GROSS_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(output_cards)} cards to {DATA_PATH}")
    print(f"Images in {IMAGE_DIR}")


if __name__ == "__main__":
    build_cards()
