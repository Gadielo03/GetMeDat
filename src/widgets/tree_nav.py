from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Tree

class TreeNav(Widget):
    """Display a tree navigation."""

    def compose(self) -> ComposeResult:
        tree: Tree[str] = Tree("Tree Navigation")
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")
        yield tree