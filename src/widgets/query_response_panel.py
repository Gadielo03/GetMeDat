import json
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import TabbedContent, TabPane, Pretty, Static
from textual.containers import VerticalScroll

class QueryResponsePanel(Widget):
    """Display the Query Response."""

    BINDINGS = [
        ("1", "show_tab('response-tab')", "Response"),
        ("2", "show_tab('response-headers-tab')", "Headers")
    ]
    
    DEFAULT_CLASSES = "query-response-panel"

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="response-tab"):
            with TabPane("Response", id="response-tab"):
                with VerticalScroll():
                    yield Static("No request made", id="status-info")
                    yield Pretty({}, id="response-body")
            with TabPane("Headers", id="response-headers-tab"):
                yield Pretty({}, id="response-headers")
    
    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab

    def on_mount(self) -> None:
        self.watch(self.app, "current_url", self.refresh_status_info)
        self.watch(self.app, "current_method", self.refresh_status_info)
        self.watch(self.app, "response_data", self.update_response_display)
        self.watch(self.app, "response_headers", self.refresh_headers_info)
        self.watch(self.app, "status_code", self.refresh_status_info)
        self.watch(self.app, "is_loading", self.refresh_status_info)
        self.watch(self.app, "error_message", self.update_error_display)
        
    def update_response_display(self, data: dict) -> None:
        response_body = self.query_one("#response-body", Pretty)
        response_body.update(data)
    
    def update_error_display(self, error: str) -> None:
        if error:
            response_body = self.query_one("#response-body", Pretty)
            response_body.update({"error": error})
    
    def refresh_status_info(self) -> None:
        status_info = self.query_one("#status-info", Static)
        
        if self.app.is_loading:
            status_info.update(f"Loading... | {self.app.current_method} {self.app.current_url}")
        elif self.app.status_code > 0:
            color = self.get_status_color(self.app.status_code)
            timestamp = ""
            if self.app.timestamp:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(self.app.timestamp)
                    timestamp = dt.strftime("%H:%M:%S")
                except:
                    pass
            
            status_text = f"[{color}]{self.app.status_code}[/] | {self.app.current_method} {self.app.current_url}"
            if timestamp:
                status_text += f" | {timestamp}"
            status_info.update(status_text)
        else:
            status_info.update("No request made")
    
    def refresh_headers_info(self) -> None:
        headers_info = {
            "status_code": self.app.status_code,
            "url": self.app.current_url,
            "method": self.app.current_method,
            "timestamp": self.app.timestamp,
            "response_headers": self.app.response_headers,
        }
        
        clean_headers = {k: v for k, v in headers_info.items() if v}
        response_headers = self.query_one("#response-headers", Pretty)
        response_headers.update(clean_headers)

    def get_status_color(self, status_code: int) -> str:
        if 200 <= status_code < 300:
            return "green"
        elif 300 <= status_code < 400:
            return "yellow"
        elif 400 <= status_code < 500:
            return "red"
        elif status_code >= 500:
            return "bright_red"
        else:
            return "white"
