#!/usr/bin/env python
import os
import sys
from pandocfilters import toJSONFilter, Para, Image, get_caption, get_filename4code, get_extension
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ImageFormatter


def log(msg):
    sys.stderr.write(msg + '\n')


def abc(key, value, format, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value
        caption, typef, keyvals = get_caption(keyvals)
        outfile = get_filename4code("pandoc_code", code)
        dest = f"{outfile}.png"

        lexer = get_lexer_by_name(classes[0], stripall=True)
        code_img = highlight(code, lexer, ImageFormatter(
            image_format="PNG", font_size=18))
        with open(dest, "wb") as f:
            f.write(code_img)
        return Para([Image([ident, [], keyvals], caption, [dest, typef])])


if __name__ == "__main__":
    toJSONFilter(abc)
