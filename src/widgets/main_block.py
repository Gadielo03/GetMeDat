from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal
from widgets.query_paramters_panel import QueryParametersPanel
from widgets.query_response_panel import QueryResponsePanel
from .search_area import SearchArea

class MainBlock(Widget):
    """Display a main block."""
    
    DEFAULT_CLASSES = "main-block"

    def compose(self) -> ComposeResult:
        with Horizontal(classes="search-bar-section"):
            yield SearchArea()
        with Horizontal(classes="content-area"):
            yield QueryParametersPanel()
            yield QueryResponsePanel()