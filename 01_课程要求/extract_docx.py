import sys, zipfile, re, os

def extract_docx(path):
    text = []
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf-8')
    # split by paragraph
    paras = re.split(r'</w:p>', xml)
    for p in paras:
        # collect all text runs
        runs = re.findall(r'<w:t[^>]*>(.*?)</w:t>', p, re.DOTALL)
        line = ''.join(runs)
        line = re.sub(r'<[^>]+>', '', line)
        if line.strip():
            text.append(line)
    return '\n'.join(text)

if __name__ == '__main__':
    for fn in sys.argv[1:]:
        print('\n\n========== FILE: ' + os.path.basename(fn) + ' ==========\n')
        if fn.lower().endswith('.docx'):
            print(extract_docx(fn))
