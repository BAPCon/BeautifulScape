# bookmark_parser/utils.py

from io import TextIOWrapper
from typing import Union
from bs4 import BeautifulSoup
import os


def netscape(html: Union[str, TextIOWrapper], custom_validator: callable = None) -> BeautifulSoup:
    """
    ### Description
    Parses Netscape bookmark HTML content into a BeautifulSoup object.
    Corrects missing closing </DT> tags and optionally removes \<p> tags in HTML.

    ### Parameters
    - html (Union[str, TextIOWrapper]): The HTML content to parse.
    - remove_paragraphs (bool): Whether to remove \<p> tags from the HTML.
    - custom_validator (function): A custom validator function to apply to the HTML, should take a string and return a string.

    ### Returns
    - BeautifulSoup: The parsed HTML content as a BeautifulSoup object.
    """

    # Input validation and loading
    if isinstance(html, TextIOWrapper):
        html = html.read()

    elif os.path.exists(html):  # Read directly from file
        with open(html, 'r', encoding='utf-8') as f:
            html = f.read()
    
    # Quick check for empty HTML (no tags)
    if not any(char in html for char in '<'):
        raise ValueError("Input contains no HTML tags")

    html = html.replace('<p>', '')
    html = html.replace('</p>', '')

    is_dt = lambda line: line.startswith('<DT>')

    # Correct missing closing tags
    html = '\n'.join([
            line + '</DT>' if is_dt(line.strip()) 
            else line
        for line in html.split('\n')
    ])

    if custom_validator:
        html = custom_validator(html)

    return BeautifulSoup(html, 'html.parser')