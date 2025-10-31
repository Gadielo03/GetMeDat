from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Tree
from services.file_service import *

class TreeNav(Widget):
    """Display a tree navigation."""

    def compose(self) -> ComposeResult:
        tree: Tree[str] = Tree("GetMeDat Configurations", id="tree-nav")
        tree.root.expand()
        config_node = None
        for config in list_configs():
            if config == "default_config.json":
                config_node = tree.root.add_leaf(config)
                config_node.expand()
            else:
                tree.root.add_leaf(config)

        if config_node:
            tree.select_node(config_node)        

        yield tree
        
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        selected_node = event.node.label
        if str(selected_node).endswith('.json'):
            self.app.title = f"GetMeDat - {selected_node}"
            self.notify(f"Selected node: {selected_node}", severity="information", timeout=2)