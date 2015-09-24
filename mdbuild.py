#!/usr/bin/env python3

__author__ = 'Michael Niewoehner <c0d3z3r0>'
__email__ = 'mniewoeh@stud.hs-offenburg.de'

import os
import sys
import re
import base64
import subprocess
import argparse

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
<title>%s</title>
</head>
<body>""".splitlines(keepends=True))

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
    md = ['\n\n']
    md.extend(subprocess.getoutput(
        'hoedown --all-block --all-flags --all-negative --all-span %s' % file
    ).splitlines(keepends=True))

    for m in md:
        if args.docs.index(file) == 0 and '<h1>' in m:
            md[md.index(m)] = re.sub(
                '<h1>', '<h1 style=\'page-break-before: avoid;\'>', m)
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

    for doc in args.docs:
        output.extend(markdown2Html(doc))

    output.extend(getFooter())
    writeListToFile('%s.html' % args.output, output)
    print('Generating the PDF will take some time. Please wait.')
    html2pdf('%s.html' % args.output, args.output, '%s.pdf' % args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='mdbuild')
    parser.add_argument('output', help='output filename')
    parser.add_argument('docs', nargs='+', help='documents to include')
    args = parser.parse_args()

    main()