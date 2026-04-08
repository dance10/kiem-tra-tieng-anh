const fs = require('fs');
for (let num of [4, 5, 6]) {
    let p = 'Exam/ielts-reading-' + num + '.html';
    let c = fs.readFileSync(p, 'utf-8');
    c = c.replace(/answers:\s*JSON\.stringify\(answersSubmitted\)/g, 'answers: answersSubmitted');
    fs.writeFileSync(p, c);
}
