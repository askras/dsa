---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.17.3
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python editable=true slideshow={"slide_type": ""}
import json
import base64

from jupyterquiz import display_quiz


def quiz(lab_n, questions_num=10):

    with open(f'questions_{str(lab_n).zfill(2)}.bin', 'rb') as f:
        questions = json.loads(base64.b64decode(f.read()).decode('utf-8'))
    display_quiz(questions, num=questions_num, shuffle_questions=True, shuffle_answers=True)
```

```python editable=true slideshow={"slide_type": ""}
quiz(5)
```

```python
json_file = 'questions_11.json'
bin_file = 'questions_11.bin'

with open(json_file, 'rb') as input_file, open(bin_file, 'wb') as output_file:
    base64.encode(input_file, output_file)

with open(f'questions_11.bin', 'rb') as f:
    questions = json.loads(base64.b64decode(f.read()).decode('utf-8'))
display_quiz(questions, 
             #num=5, 
             shuffle_questions=False, 
             shuffle_answers=False,
             preserve_responses=True,
)
```

```python editable=true slideshow={"slide_type": ""}

```
