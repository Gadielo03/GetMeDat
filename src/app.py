from textual.app import App, ComposeResult
from textual.reactive import reactive
from widgets.tree_nav import TreeNav
from widgets.main_block import MainBlock
from textual.widgets import Header, Footer
from typing import Optional, Dict, Any
from datetime import datetime
import copy

class GetMeDatApp(App):
    CSS_PATH = "./styles/app.tcss"
    
    current_url: reactive[str] = reactive("")
    current_method: reactive[str] = reactive("GET")
    request_headers: reactive[Dict[str, str]] = reactive({})
    request_body: reactive[str] = reactive("")
    
    response_data: reactive[Dict[Any, Any]] = reactive({})
    response_headers: reactive[Dict[str, str]] = reactive({})
    status_code: reactive[int] = reactive(0)
    error_message: reactive[str] = reactive("")
    is_loading: reactive[bool] = reactive(False)
    timestamp: reactive[str] = reactive("")
    
    show_timestamps: reactive[bool] = reactive(True)
    auto_format_json: reactive[bool] = reactive(True)
    
    def compose(self) -> ComposeResult:
        yield Header()  
        yield TreeNav(classes="box")
        yield MainBlock()
        yield Footer()
    
    def update_request(self, url: str = None, method: str = None, 
                      headers: Dict[str, str] = None, body: str = None) -> None:
        if url is not None:
            self.current_url = url
        if method is not None:
            self.current_method = method
        if headers is not None:
            self.request_headers = headers
        if body is not None:
            self.request_body = body
    
    def update_response(self, data: Dict[Any, Any] = None, headers: Dict[str, str] = None,
                       status: int = None, error: str = None, loading: bool = None) -> None:
        if data is not None:
            self.response_data = data
        if headers is not None:
            self.response_headers = headers
        if status is not None:
            self.status_code = status
        if error is not None:
            self.error_message = error
        if loading is not None:
            self.is_loading = loading
        
        if any(x is not None for x in [data, status, error, loading]):
            self.timestamp = datetime.now().isoformat()
    
    def set_loading(self, loading: bool) -> None:
        self.is_loading = loading
        if loading:
            self.timestamp = datetime.now().isoformat()
    
    def clear_response(self) -> None:
        self.response_data = {}
        self.response_headers = {}
        self.status_code = 0
        self.error_message = ""
        self.is_loading = False
        self.timestamp = ""

if __name__ == "__main__":
    app = GetMeDatApp()
    app.run()