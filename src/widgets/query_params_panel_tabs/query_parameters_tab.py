from textual.app import ComposeResult
from textual.widget import Widget
from ..crud_table import CrudTable

class QueryParametersTab(Widget):
    """Display the Query Parameters Tab using CrudTable."""
    
    DEFAULT_CLASSES = "tab-content"
    
    def compose(self) -> ComposeResult:
        yield CrudTable(
            title="Query Parameters",
            key_placeholder="Parameter Name",
            value_placeholder="Parameter Value",
            table_id="params-table"
        )
    
    def get_parameters(self) -> dict:
        crud_table = self.query_one(CrudTable)
        return crud_table.get_data()
