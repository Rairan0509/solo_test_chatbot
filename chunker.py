import json
from pathlib import Path
import re


input_path = Path("data/extracted.json")
with open(input_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)

doc_lines = []
for text_info in loaded["texts"]:
    if text_info["doc"] == "KRX-R600":
        for line in text_info["text"].split("\n"):
            doc_lines.append((text_info["page"], line))

print(len(doc_lines))
print(doc_lines[:3])

SECTION_PATTERN = r"^(\d+)\.(\d+)\s+(.+)"
CHAPTER_PATTERN = r"^(\d+)\.\s+(.+)" 

test_lines = [
    "3.3 제어기 KRC-40 사양",
    "4. 설치",
    "4.1 설치 환경 조건",
    "4.2 베이스 고정",
    "1. 베이스 플레이트를 앵커볼트 M20 × 8개로 바닥에 고정한다.",
    "4. 체결 후 24시간 운전 후 토크를 재확인한다.",
    "4.3 케이블 연결",
    "5. 운전",
]

current_chapter = 3 

# for test_line in test_lines:
#     section_match = re.match(SECTION_PATTERN, test_line)
#     chapter_match = re.match(CHAPTER_PATTERN, test_line)

#     if section_match:
#         print("절 제목:", test_line)
#     elif chapter_match:
#         chapter_num = int(chapter_match.group(1))

#         is_next_chapter = chapter_num == current_chapter +1
#         is_not_sentence = not test_line.endswith("다.")
        
#         if is_next_chapter and is_not_sentence:
#             current_chapter = chapter_num
#             print("장 제목", test_line)
#         else:
#             print("번호 목록:", test_line)