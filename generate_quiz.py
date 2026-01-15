import os
import json
import re

# הגדרות
root_images_folder = 'images'
output_file = 'questions.js'
valid_extensions = ('.jpg', '.jpeg', '.png', '.gif')
FIXED_NUM_OPTIONS = 8

questions = []

print(f"--- מתחיל סריקה בתיקיית {root_images_folder} ---")

# סורק את כל התיקיות ותתי-התיקיות (os.walk)
for subdir, dirs, files in os.walk(root_images_folder):
    # דילוג על התיקייה הראשית עצמה, רוצים רק תתי-תיקיות
    if subdir == root_images_folder:
        continue

    # שם התיקייה הופך ל"נושא" (למשל: "קינמטיקה")
    topic_name = os.path.basename(subdir)

    # דילוג על תיקיות מערכת או תיקיית הדמות
    if topic_name.startswith('.') or topic_name == 'mascot':
        continue

    print(f"סורק נושא: {topic_name}")

    for filename in files:
        if filename.lower().endswith(valid_extensions):
            name_part = os.path.splitext(filename)[0]

            # זיהוי תשובה
            correct_answer = 0
            ans_match = re.search(r'_ans(\d+)', name_part)
            if ans_match:
                correct_answer = int(ans_match.group(1)) - 1

            if correct_answer >= FIXED_NUM_OPTIONS: correct_answer = 0

            # בניית נתיב יחסי לתמונה
            rel_path = os.path.join(subdir, filename).replace("\\", "/")

            q_obj = {
                "topic": topic_name,
                "image": rel_path,
                "options": [""] * FIXED_NUM_OPTIONS,
                "answer": correct_answer
            }
            questions.append(q_obj)

# שמירה
js_content = f"const questions = {json.dumps(questions, indent=4, ensure_ascii=False)};"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"--- סיימנו! ---")
print(f"נוצרו {len(questions)} שאלות סך הכל.")