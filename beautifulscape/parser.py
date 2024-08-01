# bookmark_parser/parser.py

from .utils import netscape
from typing import List, Union, Optional
from bs4 import Tag
import datetime
import json


class BookmarkParser:
    """
    A class to parse and describe bookmarks from a Netscape bookmark file (ie: Chrome export).

    Attributes:
        soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.
        bookmarks (List[dict]): The list of parsed bookmarks.
        title (str): The title of the bookmark file.
        root (Folder): The root folder of the bookmarks.

    Methods:
        validate_html(): Validates the structure of the HTML soup.
        find_folder(folder_name: str): Finds a folder by name in the parser.
        to_json(indent=4): Converts the parsed bookmarks to a JSON string.
        all_bookmarks(): Returns a list of all bookmarks in the parser.
    """


    def __init__(self, html_content: Union[str, bytes]):
        self.soup = netscape(html_content)
        self.bookmarks = []
        
        self.title = self.soup.find('title').text
        self.root = Folder(self.title, self.soup.find('dl'))
        self.validate_html()
        self.root.parse()


    def validate_html(self) -> None:
        """
        Validates the structure of the HTML soup.
        """

        # Check if the root folder contains all bookmarks
        num_root_bookmarks = len(self.root.root_element.find_all('a'))
        if num_root_bookmarks != len(self.soup.find_all('a')):
            raise ValueError("Invalid bookmark structure")
        
        # Unwrap DL titles and add as attributes
        for dl in self.root.root_element.find_all('dl'):
            title_child = dl.find_previous('h3')
            dl.attrs['title'] = title_child.text
            if not title_child.parent:
                raise ValueError("Invalid bookmark structure")
            title_child.parent.decompose()


    def find_folder(self, folder_name: str) -> Optional['Folder']:
        """
        Finds a folder by name in the parser.
        """
            
        return self.root.find_folder(folder_name)


    def to_json(self, indent=4) -> str:
        """
        Converts the parsed bookmarks to a JSON string.
        """

        return json.dumps(self.root.to_dict(), indent=indent)


    def __str__(self) -> str:
        """
        Describes the bookmarks and folders in the parser.
        """

        lines = [f"Root folder: {self.root} ({len(self.root.bookmarks)} bookmarks)"]

        def describe_folder(folder, depth=0):
            """
            Recursively describes the folder and its contents.
            """
            lines.append(
                f"{'  ' * (depth+1)}Folder: {folder.name} ({len(folder.bookmarks)} bookmarks)"
            )
            for subfolder in folder.folders:
                describe_folder(subfolder, depth + 1)

        for folder in self.root.folders:
            describe_folder(folder)

        return '\n'.join(lines)
    

    def all_bookmarks(self) -> List[dict]:
        """
        Returns a list of all bookmarks in the parser.
        """
        return self.root.all_bookmarks(recursive=True)
            

class Folder:
    """
    A class to represent a folder of bookmarks.

    Attributes:
        name (str): The name of the folder.
        parent (Optional[Folder]): The parent folder.
        root_element (Tag): The root element of the folder.
        bookmarks (List[dict]): The list of bookmarks in the folder.
        folders (List[Folder]): The list of subfolders.

    Methods:
        parse(): Parses the bookmarks and subfolders of the folder.
        describe(from_raw: bool = True): Describes the folder and its contents.
        to_dict(): Converts the folder and its contents to a dictionary.
    """


    def __init__(self, name: str, root_element: Tag, parent: Optional['Folder'] = None):
        self.name = name
        self.parent = parent
        self.root_element = root_element
        self.bookmarks = []
        self.folders = []


    def parse(self) -> None:
        """
        Parses the bookmarks and subfolders of the folder.
        """

        child_links = self.root_element.find_all('dt', recursive=False)
        child_links = [link.a for link in child_links if link.a]

        for link in child_links:
            bookmark = {
                'title': link.text,
                'url': link['href'],
                'date_added': datetime.datetime.now().isoformat()
            }
            self.bookmarks.append(bookmark)

        for _folder in self.root_element.find_all('dl', recursive=False):
            _folder: Tag
            folder = Folder(
                _folder.attrs['title'], 
                _folder, 
                parent=self
            )
            folder.parse()
            self.folders.append(folder)


    def find_folder(self, folder_name: str) -> Optional['Folder']:
        """
        Finds a subfolder by name in the folder.
        """

        def find_folder_recursive(folder, name):
            """
            Recursively finds the subfolder by name.
            """
            if folder.name == name:
                return folder
            for subfolder in folder.folders:
                result = find_folder_recursive(subfolder, name)
                if result:
                    return result
            return None

        return find_folder_recursive(self, folder_name)
    

    def all_bookmarks(self, recursive: bool = True) -> List[dict]:
        """
        Returns a list of all bookmarks in the folder.

        Args:
            recursive (bool): Returns only first level subfolder bookmarks if False.
        """

        bookmarks = []
        
        def collect_bookmarks(folder):
            """
            Recursively collects bookmarks from the folder and its subfolders.
            """
            bookmarks.extend(folder.bookmarks)
            if recursive or folder.parent == self:
                for subfolder in folder.folders:
                    collect_bookmarks(subfolder)

        collect_bookmarks(self)

        return bookmarks


    def __str__(self) -> str:
        return self.name


    def describe(self) -> dict:
        """
        Describes the folder and its contents.
        """

        num_bookmarks = len(self.bookmarks)
        num_folders   = len(self.folders)

        depth = 0
        parent = self.parent
        while parent:
            depth += 1
            parent = parent.parent

        return {
            'name': self.name,
            'depth': depth,
            'num_bookmarks': num_bookmarks,
            'num_folders': num_folders
        }
    

    def to_dict(self) -> dict:
        """
        Converts the folder and its contents to a dictionary.
        """

        return {
            'name': self.name,
            'bookmarks': self.bookmarks,
            'folders': [folder.to_dict() for folder in self.folders]
        }