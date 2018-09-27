from html.parser import HTMLParser

class PRDParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == 'div' and ('class', 'body-content') in attrs:
            import pdb; pdb.set_trace()
            print(attrs)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

if __name__ == '__main__':
    with open('../../../paizoprd/paizo.com/pathfinderRPG/prd/coreRulebook/spells/acidArrow.html') as f:
        aar = f.read()
    htm = PRDParser()
    htm.feed(aar)
