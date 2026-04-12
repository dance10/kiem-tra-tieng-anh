import glob

files = glob.glob('Exam/*.html') + glob.glob('Template/*.html')
for f in files:
    if 'congratulations.html' in f: continue
    
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if '../index.html' not in content and './index.html' not in content and 'Trang Chủ' not in content:
        lines = content.split('\n')
        injected = False
        for i, line in enumerate(lines):
            if '<header' in line:
                for j in range(i, min(i+15, len(lines))):
                    if '<div class="flex items-center' in lines[j] or '<div class="flex gap-3 items-center' in lines[j]:
                        link = '<a href="../index.html" class="bg-white text-gray-700 hover:bg-gray-100 font-bold text-xs px-3 py-1.5 rounded-lg shadow-sm transition-all flex items-center gap-1 no-underline">🏠 Trang Chủ</a>'
                        lines.insert(j + 1, '            ' + link)
                        injected = True
                        break
                break
                
        if injected:
            new_content = '\n'.join(lines)
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print('Injected home link to ' + f)
