import pdfplumber
import logging
import re
logging.getLogger("pdfminer").setLevel(logging.ERROR)

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

full_tables = []
full_texts = []
with pdfplumber.open("menual/KVM-850_기술매뉴얼.pdf") as kvm:
    for page_num, page in enumerate(kvm.pages, start=1):
        tables = page.find_tables()
        
        for table in tables:
            table_info = {"page" : page_num, "table": clean_table(table.extract())}
            full_tables.append(table_info)

        text_page = page.crop((0, 40, page.width, 800))
        for table in tables:
            text_page = text_page.outside_bbox(table.bbox)
        text = text_page.extract_text()
        text_info = {"page": page_num, "text": text}
        full_texts.append(text_info)
