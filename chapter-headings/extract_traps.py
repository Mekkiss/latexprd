from bs4 import BeautifulSoup
from pathlib import Path

def arrowtra(s):
    try:
        return s.attrs['id'] == 'arrow-trap'
    except:
        return False


out = ''

environmentpath = Path('../../../websites/paizoprd/paizo.com/pathfinderRPG/prd/coreRulebook/environment.html')

with environmentpath.open() as f:
    environmenthtml = f.read()
soup = BeautifulSoup(environmenthtml)

titles = soup.findAll(name='p', attrs={'class': 'stat-block-title'})
document = titles[0].parent
elements = list(document.children)
while not arrowtra(elements[0]):
    elements = elements[1:]

# Now elements contains all the trap entries
for line in elements:
    try:
        if line.attrs['id'] == 'designing-a-trap':
            break
    except:
        pass
    try:
    #    print(line.attrs)
        if 'stat-block-title' in line.attrs['class']:
            out += '\n' + r'\statblocktitle{' + line.text + '}\\\\\n'
            print(line)
        elif 'stat-block-breaker' in line.attrs['class']:
            out += r'\statblockbreaker{' + line.text + '}\\\\\n'
        else:
            for tag in line.contents:
                try:
                    if tag.name == 'b':
                        out += r'\textbf{' + tag.text + '}'
                    elif tag.name == 'i':
                        out += r'\textit{' + tag.text + '}'
                    else:
                        out += tag.text
                except:
                    if hasattr(tag, 'text'):
                        out += tag.text
                    else:
                        out += str(tag)
            out += '\\\\\n'
    except:
        print(line)
        pass

with open('traps.tex', 'w') as f:
    f.write(out)
