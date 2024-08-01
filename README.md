
# BeautifulScape
<div style="text-align:center;margin-left:5%;margin-right:5%;padding:15px;font-size:1.2em;border-radius:8px;border-style:solid;margin-bottom:20px;margin-top:10px;"> Netscape Bookmark Parser (Chrome, Firefox, IE)</div>

[![PyPI Version](https://img.shields.io/pypi/v/bookmark_explorer.svg)](https://pypi.org/project/bookmark_explorer/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/YOUR_USERNAME/bookmark_explorer/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR_USERNAME/bookmark_explorer/actions/workflows/tests.yml)

Bookmark Explorer is a Python package designed to effortlessly extract, analyze, and navigate through your browser bookmarks. Whether you're dealing with a massive collection of bookmarks or just want to quickly find that one elusive link, Bookmark Explorer has you covered.

## Features

* **Parse Netscape Bookmark Files:**  Effortlessly extract bookmarks from HTML bookmark files exported from Chrome, Firefox, and other browsers.
* **Structured Representation:**  Organize bookmarks into a clear hierarchy, making it easy to traverse and search.
* **JSON Conversion:** Convert parsed bookmarks into JSON for easy integration with other tools and applications.

## Installation

<div>
<code style='text-decoration:line-through;'>pip install bookmark_explorer</code>
</div>

## Usage

```python
from bookmark_explorer import BookmarkParser

with open('bookmarks.html', 'r') as f:
    parser = BookmarkParser(f)

# Get all bookmarks
all_bookmarks = parser.all_bookmarks()

# Find a specific folder
folder = parser.find_folder("Recipes")

# Convert to JSON
json_data = parser.to_json()
```