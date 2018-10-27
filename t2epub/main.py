# coding=utf8

import click
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from processor import Processor

EXP = u"\s*?第(.{1,5})(章|节|集|卷|部|篇|回)"

def get_file_name(file_path):
    import ntpath
    fn = ntpath.basename(file_path)
    return fn.split('.')[0]

@click.group()
def cmd():
    pass

@cmd.command()
@click.argument('file_path', type=click.Path())
@click.option('--exp', default=EXP)
@click.option('--limit', default=40)
@click.option('--name', default='', help='the book name')
@click.option('--author', default='Unknown', help='the book name')
def process(file_path, exp, limit, name, author):
    """
    Actualy process txt file to epub
    :param file_path: input txt file path
    :type file_path: String
    :param exp: Regular expression for detect chapter
    :type exp: String
    :param limit: Chapter line max length
    :type limit: Int
    :param name: Specify the name of this book
    :type name: String
    :param author: Specify the author of this book
    :type author: String
    :return:
    :rtype:
    """
    processor = Processor(file_path, exp, limit)
    processor.gen(name, author)
    click.echo("Process complete!")
    
    


@cmd.command()
@click.argument('file_path', type=click.Path())
@click.option('--exp', default=EXP)
@click.option('--limit', default=40)
def test(file_path, exp, limit):
    """
    Show chapter title to check if Regular expression is OK
    :param file_path: input txt file path
    :type file_path: String
    :param exp: Regular expression for detect chapter
    :type exp: String
    :param limit: Chapter line max length
    :type limit: Int
    :return:
    :rtype:
    """

    processor = Processor(file_path, exp, limit)
    for title in processor.chapter_titles():
        click.echo(title)
        click.echo("---------------------")


cli = click.CommandCollection(sources=[cmd,])

def main():
    cli()

if __name__ == '__main__':
    main()



