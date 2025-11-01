from textual.app import ComposeResult
from textual.widget import Widget
from ..crud_table import CrudTable
from services.request_client import http_client

class QueryHeadersTab(Widget):
    """Display the Query Headers Tab using CrudTable."""
    
    DEFAULT_CLASSES = "tab-content"
    
    def compose(self) -> ComposeResult:
        yield CrudTable(
            initial_data=self.app.request_headers,
            title="Headers",
            key_placeholder="Header Name",
            value_placeholder="Header Value",
            table_id="headers-table"
        )
    
    def get_headers(self) -> dict:
        crud_table = self.query_one(CrudTable)
        return crud_table.get_data()
    
    def on_crud_table_data_changed(self, event: CrudTable.DataChanged) -> None:
        headers_data = event.data
        http_client.set_headers(headers_data)
        self.app.update_request(headers=headers_data)
        self.app.notify(f"Headers updated: {headers_data}", severity="information", timeout=2)
