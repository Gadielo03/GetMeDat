from textual.app import ComposeResult
from textual.widget import Widget
from ..crud_table import CrudTable
from services.request_client import http_client

class QueryParametersTab(Widget):
    """Display the Query Parameters Tab using CrudTable."""
    
    DEFAULT_CLASSES = "tab-content"
    
    def compose(self) -> ComposeResult:
        yield CrudTable(
            initial_data=self.app.current_params,
            title="Query Parameters",
            key_placeholder="Parameter Name",
            value_placeholder="Parameter Value",
            table_id="params-table"
        )
    
    def on_crud_table_data_changed(self, event: CrudTable.DataChanged) -> None:
        table_data = event.data
        self.app.update_request(params=table_data)
        self.app.notify(f"Query parameters updated: {table_data}", severity="information", timeout=2)
        http_client.set_params(params=table_data)