import glob
import re

print("Starting audit...")
files = glob.glob('Exam/*.html') + glob.glob('Template/*.html')

for f in files:
    if 'congratulations.html' in f: continue
    
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    fails = []
    
    # 1. Google sheet URL
    if 'AKfycbwrDJupIOU4PY92cMNRfafeQ-RH9Pra5EaHrnlELAnwsaVqaWiWzuIanPRY_BCM8Ohv' not in content:
        fails.append("Wrong Google Sheet URL")
        
    # 2. Validation ten hoc sinh (trim, alert roi return)
    if 'alert' not in content and 'elNameError' not in content:
        fails.append("Missing validation ten hoc sinh")
        
    # 3. Link nut Trang chu (../index.html)
    if 'href="../index.html"' not in content and '🏠 Trang Chủ' not in content:
        fails.append("Missing Trang chu link")
        
    # 4. exam_type phai dung keyword (Starters, Movers, Flyers, KET, PET, TOEIC, IELTS, Tuyen Sinh) 
    # Just check if it has student_name and exam_type properties in the JSON.stringify
    if 'student_name:' not in content and "'student_name':" not in content and '"student_name":' not in content:
        # Some use name instead...
        if 'exam_type' not in content:
            fails.append("Missing data submission params (student_name, exam_type)")
            
    # 5. Congratulations redirect
    if 'ielts-writing' not in f and 'congratulations.html' not in content:
        fails.append("Missing congratulations redirect")
        
    if len(fails) > 0:
        print(f"{f}: {', '.join(fails)}")

print("Audit complete.")
