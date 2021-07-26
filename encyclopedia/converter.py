import markdown2

def convert(file_name):
    with open(f'{file_name}.md', 'r') as f:
        text = f.read()
        html = markdown2.markdown(text)

    with open(f'{file_name}.html', 'w') as f:
        f.write(html)
