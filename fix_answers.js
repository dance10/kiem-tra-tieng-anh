const fs = require('fs');

function fixExam4() {
    let p = 'Exam/ielts-reading-4.html';
    let c = fs.readFileSync(p, 'utf-8');
    if (!c.includes('answers: answersSubmitted')) {
        c = c.replace(/const answersSubmitted = \{\};\n.*?for/, 'const answersSubmitted = {};\n        for');
        // add answersSubmitted into loop
        if (!c.includes('answersSubmitted[i] = userAns;')) {
            c = c.replace(/const userAns = getUserAnswer\(qId\)/, 'const userAns = getUserAnswer(qId);\n            answersSubmitted[i] = userAns.toUpperCase();\n            // const userAns = getUserAnswer(qId)');
        }
        
        // add to fetch payload
        c = c.replace(
            /band: \(totalScore \/ 40 \* 9\)\.toFixed\(1\)\s*\}\)/s,
            'band: (totalScore / 40 * 9).toFixed(1),\n                        answers: JSON.stringify(answersSubmitted)\n                    })'
        );
        fs.writeFileSync(p, c);
        console.log("Fixed 4");
    }
}

function fixExam5_6(num) {
    let p = `Exam/ielts-reading-${num}.html`;
    let c = fs.readFileSync(p, 'utf-8');
    if (!c.includes('answers: JSON.stringify(answersSubmitted)')) {
        // add dictionary
        if (!c.includes('let answersSubmitted = {};')) {
            c = c.replace(/let feedback = '';/, "let feedback = '';\n            let answersSubmitted = {};");
        }
        
        if (!c.includes('answersSubmitted[i] = input.value;')) {
            c = c.replace(/const studentVal = input\.value\.trim\(\)\.toLowerCase\(\);/, "const studentVal = input.value.trim().toLowerCase();\n                answersSubmitted[i] = input.value;");
        }

        // add to JSON payload
        c = c.replace(
            /(time: timeElapsed \+ 's')(\s*\})/,
            '$1,\n                    answers: JSON.stringify(answersSubmitted)$2'
        );
        fs.writeFileSync(p, c);
        console.log("Fixed " + num);
    }
}

fixExam4();
fixExam5_6(5);
fixExam5_6(6);
