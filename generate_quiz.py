import os
import json
import re

root_images_folder = 'images'
output_file = 'questions.js'
valid_extensions = ('.jpg', '.jpeg', '.png', '.gif')
FIXED_NUM_OPTIONS = 8

questions = []

print(f"--- מתחיל סריקה בתיקיית {root_images_folder} ---")

for subdir, dirs, files in os.walk(root_images_folder):
    if subdir == root_images_folder:
        continue

    folder_name = os.path.basename(subdir)

    if folder_name.startswith('.') or folder_name == 'mascot':
        continue

    display_name = folder_name.replace('_', ' ').title()

    print(f"סורק: {folder_name} -> יוצג כ: {display_name}")

    for filename in files:
        if filename.lower().endswith(valid_extensions):
            name_part = os.path.splitext(filename)[0]

            correct_answer = 0
            ans_match = re.search(r'_ans(\d+)', name_part)
            if ans_match:
                correct_answer = int(ans_match.group(1)) - 1
            if correct_answer >= FIXED_NUM_OPTIONS: correct_answer = 0

            rel_path = os.path.join(subdir, filename).replace("\\", "/")

            q_obj = {
                "topic": display_name,
                "image": rel_path,
                "options": [""] * FIXED_NUM_OPTIONS,
                "answer": correct_answer
            }
            questions.append(q_obj)

js_content = f"const questions = {json.dumps(questions, indent=4, ensure_ascii=False)};"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("--- סיימנו! ---")