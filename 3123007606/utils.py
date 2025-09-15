def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
