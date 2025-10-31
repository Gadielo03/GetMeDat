from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import TextArea, Static, Button
from textual.containers import Vertical, Horizontal
from services.request_client import http_client


class QueryAuthTab(Widget):
    """Display the Query Auth Tab with save functionality."""

    DEFAULT_CLASSES = "tab-content"
    
    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(classes="header-section"):
                yield Static("Request Auth", id="auth-header")
                yield Button("Save Auth", variant="success", id="save-auth-btn", classes="save-btn")
            
            yield TextArea(
                placeholder="Enter Bearer token or other auth info here...",
                id="auth-textarea"
            )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-auth-btn":
            self.save_auth()
    
    def save_auth(self) -> None:
        auth = self.get_auth()
        if not auth.strip():
            self.notify("Cannot save: Empty auth data", severity="warning", timeout=3)
            return
        
        token = self.get_auth()
        http_client.set_header("Authorization", f"Bearer {token}")
        self.notify("Auth data saved successfully!", severity="information", timeout=3)
    
    def get_auth(self) -> str:
        textarea = self.query_one("#auth-textarea", TextArea)
        return textarea.text