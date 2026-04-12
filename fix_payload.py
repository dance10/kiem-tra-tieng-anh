import re

def fix_payload(file_path, old_payload, new_payload):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We replace precisely
    new_content = content.replace(old_payload, new_payload)
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {file_path}")
    else:
        print(f"No changes in {file_path}")

fix_payload('Exam/ielts-reading-4.html',
'''                        action: 'saveResult',
                        name: studentName,
                        exam: 'IELTS Reading Test 4',
                        score: totalScore + '/40',
                        band: 'Band ' + band,
                        time: (3600 - timerSeconds) + 's',
                        answers: answersSubmitted''',
'''                        student_name: studentName,
                        exam_type: 'IELTS Reading Test 4',
                        score: totalScore,
                        total: 40,
                        band: 'Band ' + band,
                        answers: answersSubmitted'''
)

fix_payload('Exam/ielts-reading-5.html',
'''                    action: 'saveResult',
                    name: document.getElementById('studentName').value || "Ẩn danh",
                    exam: 'IELTS Reading Test 5',
                    score: score + '/40',
                    band: typeof assessment !== 'undefined' ? assessment : "Band " + ((score/40)*9).toFixed(1),
                    time: timeElapsed + 's',
                    answers: answersSubmitted''',
'''                    student_name: document.getElementById('studentName').value || "Ẩn danh",
                    exam_type: 'IELTS Reading Test 5',
                    score: score,
                    total: 40,
                    band: typeof assessment !== 'undefined' ? assessment : "Band " + ((score/40)*9).toFixed(1),
                    answers: answersSubmitted'''
)

fix_payload('Exam/ielts-reading-6.html',
'''                    action: 'saveResult',
                    name: document.getElementById('studentName').value || "Ẩn danh",
                    exam: 'IELTS Reading Test 6',
                    score: score + '/40',
                    band: typeof assessment !== 'undefined' ? assessment : "Band " + ((score/40)*9).toFixed(1),
                    time: timeElapsed + 's',
                    answers: answersSubmitted''',
'''                    student_name: document.getElementById('studentName').value || "Ẩn danh",
                    exam_type: 'IELTS Reading Test 6',
                    score: score,
                    total: 40,
                    band: typeof assessment !== 'undefined' ? assessment : "Band " + ((score/40)*9).toFixed(1),
                    answers: answersSubmitted'''
)
