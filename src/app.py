from textual.app import App, ComposeResult
from textual.reactive import reactive
from widgets.save_config_modal import SaveConfigScreen
from widgets.tree_nav import TreeNav
from widgets.main_block import MainBlock
from widgets.search_area import SearchArea
from textual.widgets import Header, Footer
from typing import Dict, Any
from datetime import datetime
from services.file_service import *

class GetMeDatApp(App):
    CSS_PATH = "./styles/app.tcss"
    
    BINDINGS = [
        ("ctrl+r", "send_request", "Send Request"),
        ("ctrl+f", "focus_url", "Focus URL Input"),
        ("ctrl+d", "select_method", "Select HTTP Method"),
        ("ctrl+s", "show_save_config_modal", "Save Configuration"),
    ]

    config = load_config()

    current_url: reactive[str] = reactive(config.get("current_url", ""))
    current_method: reactive[str] = reactive(config.get("current_method", "GET"))
    request_headers: reactive[Dict[str, str]] = reactive(config.get("request_headers", {}))
    request_body: reactive[Dict[str, Any]] = reactive(config.get("request_body", {}))
    current_auth: reactive[str] = reactive(config.get("current_auth", ""))
    current_params: reactive[Dict[str, str]] = reactive(config.get("current_params", {}))

    response_data: reactive[Dict[Any, Any]] = reactive(config.get("response_data", {}))
    response_headers: reactive[Dict[str, str]] = reactive(config.get("response_headers", {}))
    status_code: reactive[int] = reactive(config.get("status_code", 0))
    error_message: reactive[str] = reactive(config.get("error_message", ""))
    is_loading: reactive[bool] = reactive(config.get("is_loading", False))
    timestamp: reactive[str] = reactive(config.get("timestamp", ""))

    show_timestamps: reactive[bool] = reactive(config.get("show_timestamps", True))
    auto_format_json: reactive[bool] = reactive(config.get("auto_format_json", True))

    def compose(self) -> ComposeResult:
        yield Header(id="app-header")  
        yield TreeNav(classes="box")
        yield MainBlock()
        yield Footer()
    
    def update_request(self, url: str = None, method: str = None, 
                      headers: Dict[str, str] = None, body: Dict[str, Any] = None,
                      auth: str = None, params: Dict[str, str] = None) -> None:
        if url is not None:
            self.current_url = url
        if method is not None:
            self.current_method = method
        if headers is not None:
            self.request_headers = headers
        if body is not None:
            self.request_body = body
        if auth is not None:
            self.current_auth = auth
        if params is not None:
            self.current_params = params
    
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
    
    def action_send_request(self) -> None:
        try:
            search_area = self.query_one("SearchArea")  
            button = search_area.query_one("#send-request-btn")
            button.action_press()
        except Exception as e:
            self.notify(f"Error sending request: {e}", severity="error")
    
    def action_focus_url(self) -> None:
        try:
            search_area = self.query_one("SearchArea")
            url_input = search_area.query_one("#url-input")
            url_input.focus()
        except Exception as e:
            self.notify(f"Error focusing URL input: {e}", severity="error")

    def action_select_method(self) -> None:
        try:
            search_area = self.query_one("SearchArea")
            method_select = search_area.query_one("#method-select")
            method_select.focus()
        except Exception as e:
            self.notify(f"Error focusing method select: {e}", severity="error")
    
    def action_show_save_config_modal(self) -> None:
        self.push_screen(SaveConfigScreen())

if __name__ == "__main__":
    initalize_storage()
    app = GetMeDatApp()
    app.run()