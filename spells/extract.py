from bs4 import BeautifulSoup
from pathlib import Path

spellpath = Path('../../../websites/paizoprd/paizo.com/pathfinderRPG/prd/coreRulebook/spells/')

for spellfile in spellpath.glob('*.html'):
    with spellfile.open() as f:
        aar = f.read()
    soup = BeautifulSoup(aar)
    tag = soup.find(name='div', attrs={'class': 'body'})
    if tag is None:
        print('issue with {}'.format(spellfile))
        continue
    foot = tag.find(name='div', attrs={'class': 'footer'})
    foot.clear()
    title = tag.find(name='p', attrs={'class': 'stat-block-title'})
    if 'id' not in title.attrs:
        if 'Fog Cloud' in str(title):
            name = 'fog-cloud'
        else:
            print('ignoring {}'.format(str(title)))
        continue
    else:
        name = title.attrs['id']
    filecontents = ''
    if title.find('b') is None:
        spellname = title.find('strong').text
    else:
        spellname = title.find('b').text
    filecontents += r'\spellentry{' + spellname + '}\n'
    for line in tag.findAll(name='p')[1:]:
        for child in line.children:
            if not hasattr(child, 'text'):
                child.text = str(child)
            if child.name == 'b':
                filecontents += r'\textbf{' + child.text + '}'
            elif child.name == 'i':
                filecontents += r'\textit{' + child.text + '}'
            else:
                filecontents += child.text
        filecontents += '\\\\\n'
    with open(name + '.tex', 'w') as f:
        f.write(filecontents)

