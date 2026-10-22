import pdfplumber
import logging
import re
from pathlib import Path
import json

logging.getLogger("pdfminer").setLevel(logging.ERROR)

doc_name = Path("menual/KHP-200_기술매뉴얼.pdf").stem.split("_")

HEADER_CUT = 40     # 이 위는 머리말 영역
FOOTER_CUT = 800    # 이 아래는 쪽번호 영역



def clean_table(table):
    cleaned_table = []
    for row in table:
        clean_row = []
        for cell in row:
            if cell is None:
                cell = ""
            clean_cell= cell.replace("-\n", "-")
            clean_cell = clean_cell.replace("\n", " ")
            clean_row.append(clean_cell)
        cleaned_table.append(clean_row)
    return cleaned_table


def extract_pdf(pdf_path):
    doc_name= Path(pdf_path).stem.split("_")[0]
    full_tables = []
    full_texts = []
    doc_info = {"doc": doc_name}
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            body_page = page.crop((0, HEADER_CUT, page.width, FOOTER_CUT))
            if page_num == 1:
                cover_text = body_page.extract_text()
                cover_lines = cover_text.split("\n")
                for line in cover_lines:
                    if line.startswith("문서번호"):
                        doc_info["doc_no"] = line.replace("문서번호", "").strip()
                    if line.startswith("Rev."):
                        doc_info["rev"] = line
                continue
            
            tables = page.find_tables()
            
            for table in tables:
                table_info = {"doc": doc_name,"page" : page_num, "table": clean_table(table.extract())}
                full_tables.append(table_info)

            text_page = body_page
            for table in tables:
                text_page = text_page.outside_bbox(table.bbox)
            text = text_page.extract_text()
            text_info = {"doc": doc_name,"page": page_num, "text": text}
            full_texts.append(text_info)

    return doc_info, full_tables, full_texts

pdf_dir = Path("menual")
all_docs = []
all_tables = []
all_texts = []
for pdf_path in pdf_dir.glob("*.pdf"):
    doc_info, full_tables, full_texts = extract_pdf(pdf_path)
    all_docs.append(doc_info)
    all_tables.extend(full_tables)
    all_texts.extend(full_texts)

output_path = Path("data/extracted.json")
output_path.parent.mkdir(exist_ok=True)

result = {
    "documents": all_docs,
    "tables": all_tables,
    "texts": all_texts,
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

with open(output_path, "r", encoding="utf-8") as f:
    json.load(f)
    loaded= result
    print(len(loaded["tables"]))
    print(len(loaded["texts"]))
    print(len(loaded["documents"]))

for doc in loaded["documents"]:
    doc_name = doc["doc"]
    table_count = len([t for t in loaded["tables"] if t["doc"] == doc_name])
    text_count = len([i for i in loaded["texts"] if i["doc"] == doc_name])
    print(f"{doc_name}: 표 {table_count}개, 텍스트 {text_count}")