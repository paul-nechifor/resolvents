#!/usr/bin/env python2

import sys
import re

template = r"""\documentclass[12pt]{article}

\usepackage{amsmath}
\usepackage{multirow}

\begin{document}
\begin{equation}
\begin{array}{l l l}
%s
\end{array}
\notag
\end{equation}
\end{document}
"""

def main():
    input = sys.stdin.read()

    list = [
        (r'--[-]*', ''),
        (r'\n\n', r'\n'),
        (r'\|', r'\\vee'),
        (r'&', r'\\wedge'),
        (r'=', '&=&'),
        (r'Res ([0-9*]*)', r'R_\1'),
        (r'reunit cu', r'\cup'),
        (r', ,', r','),
        (r', }', r'}'),
        (r'{ ,', r'{'),
        (r'{', r'\\{'),
        (r'}', r'\\}'),
        (r'!', r'\\neg{}'),
        (r'\n', r'\\\\\n'),
    ]

    for regex, repl in list:
        input = re.sub(regex, repl, input)

    sys.stdout.write(template % input)

if __name__ == '__main__':
    main()
