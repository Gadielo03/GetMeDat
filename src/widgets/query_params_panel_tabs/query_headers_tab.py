from textual.app import ComposeResult
from textual.widget import Widget
from ..crud_table import CrudTable

class QueryHeadersTab(Widget):
    """Display the Query Headers Tab using CrudTable."""
    
    DEFAULT_CLASSES = "tab-content"
    
    def compose(self) -> ComposeResult:
        yield CrudTable(
            title="Headers",
            key_placeholder="Header Name",
            value_placeholder="Header Value",
            table_id="headers-table"
        )
    
    def get_headers(self) -> dict:
        crud_table = self.query_one(CrudTable)
        return crud_table.get_data()
