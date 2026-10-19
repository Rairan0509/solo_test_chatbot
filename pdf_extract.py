import pdfplumber

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

with pdfplumber.open("menual/KVM-850_기술매뉴얼.pdf") as kvm:
    tables = kvm.pages[2].extract_tables()

for table in tables:
    print(clean_table(table))


