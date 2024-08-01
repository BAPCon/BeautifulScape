import os
import pytest
from bookmark_parser import BookmarkParser, Folder

# ---------- Fixtures ----------
@pytest.fixture
def sample_bookmark_html():
    return """
        <!DOCTYPE NETSCAPE-Bookmark-file-1>
        <TITLE>Bookmarks</TITLE>
        <H1>Bookmarks</H1>
        <DL><p>
            <DT><H3 ADD_DATE="1691940657" LAST_MODIFIED="1706939041">Bookmarks Bar</H3>
            <DL><p>
                <DT><A HREF="www.jobsite.com">Bookmark #1</A>
                <DT><H3 ADD_DATE="1703242820" LAST_MODIFIED="0">Nested Folder #1</H3>
                <DL><p>
                    <DT><H3 ADD_DATE="1703242820" LAST_MODIFIED="0">Nested Folder #2</H3>
                    <DL><p>
                        <DT><A HREF="https://www.example.com">Nested Bookmark #1</A>
                        <DT><A HREF="https://www.example.com">Nested Bookmark #2</A>
                    </DL><p>
                </DL><p>
            </DL><p>
        </DL><p>
    """

@pytest.fixture
def bookmark_parser(sample_bookmark_html):
    return BookmarkParser(sample_bookmark_html)

# ---------- Unit Tests ----------
def test_folder_to_dict(bookmark_parser):
    folder = bookmark_parser.find_folder("Bookmarks Bar")
    folder_dict = folder.to_dict()

    assert folder_dict["name"] == "Bookmarks Bar"
    assert len(folder_dict["bookmarks"]) == 1
    assert len(folder_dict["folders"]) == 1

def test_all_bookmarks(bookmark_parser):
    all_bookmarks = bookmark_parser.all_bookmarks()
    assert len(all_bookmarks) == 3

# ---------- Integration Tests ----------
def test_bookmark_parser_end_to_end(sample_bookmark_html):
    parser = BookmarkParser(sample_bookmark_html)
    assert parser.title == "Bookmarks"
    assert isinstance(parser.root, Folder)
    assert len(parser.root.bookmarks) == 0
    assert len(parser.root.folders) == 1

# ---------- Functional Tests ----------
def test_chained_folder_search(bookmark_parser):
    """
    Tests the ability to chain folder searches.
    """
    parent_subfolder = bookmark_parser.find_folder("Nested Folder #1")
    subfolder = parent_subfolder.find_folder("Nested Folder #2")
    assert subfolder.name == "Nested Folder #2"
    assert len(subfolder.bookmarks) == 2

def test_parent_relationship(bookmark_parser):
    """
    Tests the parent relationship between folders.
    """

    pf = bookmark_parser.find_folder("Bookmarks Bar")
    ps = bookmark_parser.find_folder("Nested Folder #1")
    sf = ps.find_folder("Nested Folder #2")

    # Bookmarks > Bookmarks Bar > Nested Folder #1 > Nested Folder #2
    assert sf.parent == ps
    assert ps.parent == pf
    assert pf.parent is bookmark_parser.root
    assert bookmark_parser.root.parent is None