# coding=utf8
import os
import shutil
import uuid

import pypub
from utilitis import slice_chapter, render_template
from templates import CONTAINER_XML, CSS, CHAPTER_TEMPLATE, NAV_TEMPLATE, PACKAGE_OPF_TEMPLATE



class Chapter(object):
    def __init__(self,idx, title, contents):
        self.idx = idx
        self.title = title
        self.content_lines = contents
        self.file_name = "chapter_%05d.xhtml" % idx


class Processor(object):
    def __init__(self, filepath, exp, limit):
        self.filepath = filepath
        self.chapters = []
        idx = 1
        for title, content in slice_chapter(filepath, exp, limit):
            self.chapters.append(Chapter(idx, title, content))
            idx+=1

    def chapter_titles(self):
        return [chapter.title for chapter in self.chapters]


    def gen_container_xml(self, root):
        meta_inf_path = os.path.join(root, "META-INF")
        os.mkdir(meta_inf_path)
        with open(os.path.join(meta_inf_path, 'container.xml'), 'w') as f:
            f.write(CONTAINER_XML)

    def gen_static_files(self, root):
        os.mkdir(root)
        css_path = os.path.join(root, 'css')
        os.mkdir(css_path)
        with open(os.path.join(css_path, 'epub-spec.css'), 'w') as f:
            f.write(CSS)
        self.gen_xhtml_files(root)

    def gen_xhtml_files(self, root):
        html_path = os.path.join(root, 'xhtml')
        os.mkdir(html_path)
        for chapter in self.chapters:
            chapter_path = os.path.join(html_path, chapter.file_name)
            html = render_template(CHAPTER_TEMPLATE, chapter=chapter)
            with open(chapter_path, 'w') as f:
                f.write(html)
        nav_path = os.path.join(html_path, 'chapter_nav.xhtml')
        nav_html = render_template(NAV_TEMPLATE, chapters = self.chapters)
        with open(nav_path, 'w') as f:
            f.write(nav_html)


    def gen_opf_file(self, root, name, author):
        opf_path = os.path.join(root, 'package.opf')
        opf_xml = render_template(PACKAGE_OPF_TEMPLATE, chapters=self.chapters, name=name, author=author, uid=uuid.uuid4().hex)
        with open(opf_path, 'w') as f:
            f.write(opf_xml)

    def create_zip_archive(self, root_path, epub_name):
        epub_name = ''.join([c for c in epub_name if c != ' ']).rstrip()
        epub_name_with_path = os.path.join(root_path, epub_name)
        try:
            os.remove(os.path.join(epub_name_with_path, '.zip'))
        except OSError:
            pass
        shutil.make_archive(epub_name_with_path, 'zip', epub_name_with_path)
        zip_path = epub_name_with_path.rstrip('/') + '.zip' if epub_name_with_path.endswith('/') else epub_name_with_path + '.zip'
        return zip_path

    def turn_zip_into_epub(self, zip_archive):
        epub_full_name = zip_archive.strip('.zip') + '.epub'
        try:
            os.remove(epub_full_name)
        except OSError:
            pass
        os.rename(zip_archive, epub_full_name)
        return epub_full_name


    def gen(self, name, author):
        book_name = name if name else self.filepath.split(os.sep)[-1].split('.')[0]
        root_path = os.getcwd()
        root_dir_path = os.path.join(root_path, book_name)
        if os.path.exists(root_dir_path):
            shutil.rmtree(root_dir_path)
        os.mkdir(root_dir_path)
        mime_path = os.path.join(root_dir_path, 'mimetype')
        with open(mime_path, 'w') as f:
            f.write('application/epub+zip')
        epub_path = os.path.join(root_dir_path, "EPUB")
        self.gen_container_xml(root_dir_path)
        self.gen_static_files(epub_path)
        self.gen_opf_file(epub_path, book_name, author)
        zip_path = self.create_zip_archive(root_path, book_name)
        self.turn_zip_into_epub(zip_path)
        shutil.rmtree(root_dir_path)
        

            


