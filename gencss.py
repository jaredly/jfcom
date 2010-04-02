#!/usr/bin/env python
# Call it this way:
# python gen_css.py pygments.css
import sys

from pygments.formatters import HtmlFormatter

f = open(sys.argv[1], 'w')
if len(sys.argv)>2:
    style = sys.argv[2]
else:
    style = 'default'

# You can change style and the html class here:
f.write(HtmlFormatter(style=style).get_style_defs('.highlight'))

f.close()

# vim: et sw=4 sts=4
