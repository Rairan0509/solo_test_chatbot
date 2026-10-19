import pdfplumber
import logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)

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

with pdfplumber.open("menual/KVM-850_기술매뉴얼.pdf") as kvm:
    for page_num, page in enumerate(kvm.pages, start=1):
        tables = page.extract_tables()
        for table in tables:
            table_info = {"page" : page_num, "table": clean_table(table)}
            full_tables.append(table_info)
print(len(full_tables))
print(full_tables)