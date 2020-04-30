#!/usr/bin/env python
import os
import sys
import re
import html
import pypandoc
from pandocfilters import CodeBlock, toJSONFilter
from premailer import transform
import htmlmin
import base64
import html
from datetime import datetime

from jinja2 import Environment


def log(msg):
    sys.stderr.write(msg + '\n')


def strip_entities(s: str):
    s = s.replace("\r\n", "\n")
    s = s.replace("\r", "\n")
    s = s.replace("{", "&#123;").replace("}", "&#125;").replace("\n", "<br>")
    return s


def shortcode_pattern(code: str):
    return re.compile(r"\["+code+"\](((?!\[\/"+code+"\]).)*)\[\/"+code+"\]", re.DOTALL)


def all_or_nothing(text: str):
    p = re.compile(r"(?<!\\)\{\+\+(((?!\+\}).)*)(?<!\\)\+\+\}", re.DOTALL)
    peq = re.compile(r"(?<!\\)=")
    ptild = re.compile(r"(?<!\\)~")

    def replacer(match):
        s = match.group(1)
        correct = len(re.findall(r"(?<!\\)=", s))
        s = ptild.sub(f"~%-100%", s)
        s = peq.sub(f"~%{(100/correct):.3f}%", s)

        return "{ "+s+" }"
    replacement = p.sub(replacer, text)
    return replacement


def jinjize(text: str):
    p = shortcode_pattern("jinja")

    def replacer(match):
        try:
            env = Environment(
                line_statement_prefix="$$>", variable_start_string="${", variable_end_string="}"
            )
            s = match.group(1)
            r = env.from_string(s).render()
        except Exception as err:
            lineno = err.lineno - 1
            line_start = text[:match.start()].count('\n')+1
            line_end = text[:match.end()].count('\n')+1
            text_with_lines = ""
            for i, l in enumerate(s.split("\n")):
                text_with_lines += f"{i+line_start:0=3d} {'=>' if i == lineno else ' |'} {l}\n"

            raise Exception(
                f"Error {err} line {lineno+line_start} while parsing :  \n{text_with_lines}\n")
        return r

    replacement = p.sub(replacer, text)
    return replacement


def pandocize(text: str):
    p = shortcode_pattern("pandoc")

    def replacer(match):
        s = match.group(1)
        orig = ""
        for l in s.split("\n"):
            orig += f"// {l}\n"

        s = transform(pypandoc.convert_text(
            s, 'html4', format='md', extra_args=['--self-contained'], filters=[f"{os.path.dirname(os.path.realpath(__file__))}/code2img.py"]))
        p = re.compile(r"<body>(.*)</body>",
                       re.MULTILINE | re.IGNORECASE | re.DOTALL)
        s = p.findall(s)[0]
        s = htmlmin.minify(s, remove_comments=True,
                           remove_all_empty_space=True, remove_empty_space=True, keep_pre=False)

        return orig+strip_entities(s)

    return p.sub(replacer, text)


def process(text: str):
    text = jinjize(text)
    text = pandocize(text)
    text = all_or_nothing(text)
    return f"""
// Moodle gift question bank (https://docs.moodle.org/38/en/GIFT_format)
// This file has been generated at {datetime.now()}
// Changes in this file will be overwritten if you restart the generator.
// Images and source codes have been included as base64. 
// To check the file you may switch to the html extension and use a browser.
// The original text has been preserved as comments.

{text}
    
    """


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage : {sys.argv[0]} <input gift> (<output generated file>)")
        print("You need to provide at least the file name")
        sys.exit()

    file = sys.argv[1]

    with open(file, 'r') as f:
        text = f.read()
        text = process(text)

        if len(sys.argv) == 2:
            print(text)
        else:
            output = sys.argv[2]
            with open(output, "w") as f:
                f.write(text)
