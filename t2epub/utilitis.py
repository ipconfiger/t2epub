# coding=utf8
import os
import re
from jinja2 import Environment, BaseLoader


def filename_from_path(path):
    return path.split(os.sep)[-1]


def render_template (template, **data):
    template = Environment(loader=BaseLoader).from_string(template)
    _html = template.render(**data)
    return _html


def txt2lines(file_path):
    with open(file_path, 'r') as f:
        for l in f.readlines():
            yield l.strip().decode('utf8')


def is_chapter(line, re_exp, limit):
    if len(line) > limit:
        return False
    return True if re.match(re_exp.encode('utf8'), line.encode('utf8'), re.U) else False


def slice_chapter(file_path, reg_exp, limit):
    title = u'Foreword'
    chapter_lines = []
    for line in txt2lines(file_path):
        if line == u"":
            continue
        if not is_chapter(line.decode('utf8'), reg_exp, limit):
            chapter_lines.append(line.decode('utf8'))
        else:
            yield (title, chapter_lines)
            title = line.decode('utf8')
            chapter_lines = []
    yield (title.strip(), chapter_lines)

