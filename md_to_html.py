"""
This module is a standalone script to convert Markdown into HTML.
It reads Markdown from stdin and writes HTML to stdout.
"""


import re


def paragraphs(corpus):
    r"""
    Inserts <p> and </p> tags appropriately into corpus.

    Parameters
    ----------
    corpus : str
        The raw or partially converted Markdown text.

    Returns
    -------
    all_paras_added : str
        The corpus after paragraph tags are inserted.

    >>> text = 'P1\n\nP2\nP2\n    \t   \n\n\n  \t\nP3'
    >>> paragraphs(text)
    '<p>P1</p>\n<p>P2\nP2</p>\n<p>P3</p>'
    """
    inner_paras_added = re.sub(r'\n\s*\n', '</p>\n<p>', corpus)
    all_paras_added = f'<p>{inner_paras_added}</p>'
    return all_paras_added


def lists(corpus):
    r"""
    Inserts list tags appropriately into corpus.

    Parameters
    ----------
    corpus : str
        The raw or partially converted Markdown text.

    Returns
    -------
    ol_ul_finished : str
        The corpus after list tags are inserted.

    >>> ul_test = '- i1\n+ i2\n* i3'
    >>> lists(ul_test)
    '<ul><li>i1</li>\n<li>i2</li>\n<li>i3</li></ul>'
    >>> ul_test = '2. i1\n69. i2\n1337. i3'
    >>> lists(ul_test)
    '<ol><li>i1</li>\n<li>i2</li>\n<li>i3</li></ol>'
    """
# wrap each unordered item in its own list
    ul_wrapped = re.sub(r'(-|\+|\*) (.*)', '<ul><li>\g<2></li></ul>', corpus)
# remove back-to-back </ul><ul>
    ul_finished = re.sub(r'</ul>\n(.*)<ul>', '\n', ul_wrapped)
# wrap each ordered item in its own list
    ol_wrapped = re.sub(r'(\d+\.) (.*)', '<ol><li>\g<2></li></ol>', ul_finished)
# remove back-to-back </ul><ul>
    ol_ul_finished = re.sub(r'</ol>\n(.*)<ol>', '\n', ol_wrapped)
    return ol_ul_finished


def italics(corpus):
    r"""
    Italicizes words in the markdown that are surrounded by
    single asterisks.

    Parameters
    ----------
    corpus : str
        The raw or partially converted Markdown text.

    Returns
    -------
    str
        The `corpus` with <em> tags inserted.

    >>> text = '*italic*'
    >>> italics(text)
    '<em>italic</em>'
    """
    return re.sub(r'\*([^\n]+)\*', '<em>\g<1></em>', corpus)


def bold(corpus):
    r"""
    Bolds words in the markdown that are surrounded by
    double asterisks.

    Parameters
    ----------
    corpus : str
        The raw or partially converted Markdown text.

    Returns
    -------
    str
        The `corpus` with <strong> tags inserted.

    >>> text = '**bold**'
    >>> bold(text)
    '<strong>bold</strong>'
    """
    return re.sub(r'\*\*([^\n]+)\*\*', '<strong>\g<1></strong>', corpus)


def headers(corpus):
    r"""
    Places headers up to h6 into the corpus.

    Parameters
    ----------
    corpus : str
        Markdown string to convert.

    Returns
    -------
        A string of HTML converted from the `corpus`.

    >>> headers('#hello')
    '#hello'
    >>> headers('# hello')
    '<h1>hello</h1>'
    >>> headers('## hello')
    '<h2>hello</h2>'
    >>> headers('###  \t hello')
    '<h3>hello</h3>'
    >>> headers('####\thello')
    '<h4>hello</h4>'
    >>> headers('#####\t   hello')
    '<h5>hello</h5>'
    >>> headers('######    hello')
    '<h6>hello</h6>'
    >>> headers('#######\t hello')
    '#######\t hello'
    """
    for i in range(6, 0, -1):
        corpus = re.sub(r'(^|\n)'+f'({"#"*i})'+'[ \t]+([^\n]+)',
                        f'\g<1><h{i}>\g<3></h{i}>', corpus)
    return corpus


def html(corpus):
    r"""
    Converts raw Markdown into HTML.

    Parameters
    ----------
    corpus : str
        The raw Markdown.

    Returns
    -------
    converted_text : str
        Resulting HTML from converting `corpus`.

    >>> text = 'P1\n\nP2\n- 1\n- 2\nP2\n\nP3'
    >>> html(text)
    '<article><p>P1</p>\n<p>P2\n<ul><li>1</li>\n<li>2</li></ul>\nP2</p>\n<p>P3</p></article>'
    >>> bolditalic = '***hello***'
    >>> html(bolditalic)
    '<article><p><strong><em>hello</em></strong></p></article>'
    """
    text = paragraphs(lists(italics(bold(headers(corpus)))))
    return f'<article>{text}</article>'


if __name__ == '__main__':
    import doctest
    doctest.testmod()
