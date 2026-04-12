import glob

for f in glob.glob('Exam/*.html') + glob.glob('Template/*.html'):
    if 'congratulations.html' in f: continue
    
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if 'congratulations.html' not in content:
        print(f"Missing congratulations redirect in: {f}")
