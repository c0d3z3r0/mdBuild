#!/usr/bin/env python3

__author__ = 'Michael Niewoehner <c0d3z3r0>'
__email__ = 'mniewoeh@stud.hs-offenburg.de'

import os
import sys
import re
import base64
import subprocess


def checkDependencies():
    dep = ['hoedown', 'wkhtmltopdf']
    missing = []
    for d in dep:
        if subprocess.getstatusoutput('which ' + d)[0]:
            missing.append(d)
    if missing:
        print("Please install missing dependencies: " + ', '.join(missing))
        sys.exit(1)


def readFileToList(file):
    f = open(file, 'r')
    return f.readlines()


def file2base64(file):
    f = open(file, 'rb')
    return base64.b64encode(f.read()).decode()


def writeListToFile(file, lines):
    f = open(file, 'w')
    f.writelines(lines)
    f.close()


def readStyles(styles):
    st = []
    for style in styles:
        s = readFileToList(style)
        s.insert(0, '<style type="text/css">\n')
        s.append('</style>\n')
        st.extend(s)
    return st


def getHeader():
    header = []
    header.extend("""\
<!DOCTYPE html><html>
<head>
<meta charset="utf-8">
<title>CTF@HSO Documentation</title>
</head>
<body>
<h1 style='page-break-before: avoid;'>CTF@HSO Documentation</h1>
""".splitlines(keepends=True))

    styles = readStyles([
        'style/GitHub2.css', 'style/prism.css', 'style/custom.css'
    ])
    for s in styles:
        header.insert(-2, s)

    return header


def getFooter():
    footer = []

    footer.append('<script type="text/javascript">\n')
    footer.extend(readFileToList('style/prism.js'))
    footer.extend("""\
</script>
</body>

</html>""".splitlines(keepends=True))

    return footer


def markdown2Html(file):
    md = subprocess.getoutput(
        'hoedown --all-block --all-flags --all-negative --all-span ' +
        file
    ).splitlines(keepends=True)
    for m in md:
        if 'img src' in m:
            src = re.search('src="(.*?)"', m).group(1)
            ext = re.search('(?<=\.).{1,4}?$', src).group(0)
            b64 = file2base64(os.path.dirname(file) + '/' + src)
            newimg = 'data:image/' + ext + ';base64,' + b64
            md[md.index(m)] = re.sub(src, newimg, m)
    return md


def html2pdf(input, title, output):
    subprocess.getoutput(
        'wkhtmltopdf --print-media-type --title ' +
        ' '.join([title, input, output])
    )


def main():
    checkDependencies()

    output = []
    output.extend(getHeader())

    output.extend(markdown2Html('../README.md'))
    output.extend(markdown2Html('../GIT-Tutorial.md'))
    output.extend(markdown2Html('../TODO.md'))
    output.append('<h1>Infrastructure</h1>')
    output.extend(markdown2Html('../infrastructure/Server.md'))
    output.extend(markdown2Html('../infrastructure/Network.md'))
    output.extend(markdown2Html('../infrastructure/Containers.md'))
    output.extend(markdown2Html('../infrastructure/NetContainer.md'))
    output.extend(markdown2Html('../infrastructure/WebContainer.md'))
    output.extend(markdown2Html('../infrastructure/BuildChroot.md'))
    output.extend(markdown2Html('../docs/Infosites.md'))
    output.append('<h1>Challenges</h1>')
    output.extend(markdown2Html('../challenges/Challenges.md'))

    categories = ['', 'net', 'web']
    for cat in categories:
        for root, dirs, files in os.walk('../challenges/'):
            match = \
                re.match('../challenges/(%s)/' %
                         '|'.join([c for c in categories if c != cat]), root)
            if (not cat and match) or (cat and not match):
                continue
            for file in files:
                if not re.match('^.*?/[@.][^/]*/.*$', root) and \
                        re.match("README.*\.md", file):
                    output.extend(markdown2Html(os.path.join(root, file)))

    output.extend(getFooter())
    writeListToFile('CTF@HSO-Documentation.html', output)
    print('Generating the PDF will take some time. Please wait.')
    html2pdf('CTF@HSO-Documentation.html', 'CTF@HSO-Documentation',
             'CTF@HSO-Documentation.pdf')


if __name__ == '__main__':
    main()