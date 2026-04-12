import glob

for f in glob.glob('Exam/*.html') + glob.glob('Template/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    dirty = False
    
    if 'href="index.html"' in content:
        content = content.replace('href="index.html"', 'href="../index.html"')
        dirty = True
        
    if 'href="./index.html"' in content:
        content = content.replace('href="./index.html"', 'href="../index.html"')
        dirty = True
        
    if dirty:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print('Fixed link in ' + f)
