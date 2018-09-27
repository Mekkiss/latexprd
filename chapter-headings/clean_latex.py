import sys
from lxml import etree as ET

def get_content():
    pass

def handle_table(document, html):

    # Starts with % <div class="table">

    # id is shortly after this: % <thead id="table-3-3-bard">

    id_tag = document[document.index('thead id='):]
    id_tag = id_tag[:id_tag.index('">')+2]
    print(id_tag)
    table_id = id_tag[id_tag.index('"') + 1:id_tag.rindex('"')]
    print(table_id)

    # end of the table is the first /div
    table = document[document.index('thead id'):]
    table = table[:table.index('\n')]

    # find the html table
    
    htables = ET.HTML(html).findall('.//table')
    htmltable = None
    for htable in htables:
        if htable is not None and ('id', table_id) in htable.items():
            htmltable = htable
            break  # htable is the table we want

    if htmltable is None:
        return document

    print(htmltable.text)
    rows = iter(htable)
    caption = next(rows).text

    header = next(rows)

    latexhead = ''
    # Parse the header
    for headerrow in header.getchildren():
        hrow = []
        for tag in headerrow.getchildren():
            if tag.text is None:
                
                hrow.append(tag.getchildren()[0].text)
            else:
                hrow.append(tag.text)
        hrow = [str(x) for x in hrow]
        latexhead += ' & '.join(hrow) + '\\\\\n'

    # the rest are typical rows
    try:
        while True:
            row = next(rows)
            drow = []
            for col in row.getchildren():
               # import pdb; pdb.set_trace()
                if col.text is not None:
                    drow.append(col.text)
                else:
                    drow.append(textify(col))
                    
            print(drow)
            latexhead += ' & '.join(drow) + '\\\\\n'
            numcols = len(drow)
    except StopIteration:
        pass

    assert numcols > 0
    
    latex = '\n' + r'\begin{table}[]' + '\n'
    latex += r'\caption{' + caption + '}\n'
    latex += r'\begin{tabular}{' + 'l' * numcols + '}\n'
    latex += latexhead
    latex += r'\end{tabular}' + '\n' + r'\end{table}'

    return document.replace(table, latex)

def textify(node):
    if node.text is not None:
        return node.text
    else:
        parts = []
        for child in node.getchildren():
            parts.append(textify(child))
        return ", ".join(parts)

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname) as f:
        data = f.read()
    
    data = data[data.index('\\chapter'):]
    data = data.replace('\\section', '\\subsection')
    data = data.replace('\\chapter', '\\section')
    data = data[:data.index('% <div class="footer">')]

    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            html = f.read()
        while r'thead id="' in data:
            data = handle_table(data, html)

    with open(fname, 'wt') as f:
        f.write(data)
