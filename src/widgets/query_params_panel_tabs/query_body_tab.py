import json
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import TextArea, Static, Button
from textual.containers import Vertical, Horizontal


class QueryBodyTab(Widget):
    """Display the Query Body Tab with JSON validation."""

    DEFAULT_CLASSES = "tab-content"
    
    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(classes="header-section"):
                yield Static("Request Body", id="body-header")
                yield Button("Save Body", variant="success", id="save-body-btn", classes="save-btn")
            
            yield TextArea(
                placeholder="Enter request body here (JSON format)...", 
                id="body-textarea",
                language="json"
            )
            yield Static("Valid JSON", id="json-status", classes="json-valid")
    
    def on_mount(self) -> None:
        self.update_json_status()
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        if event.text_area.id == "body-textarea":
            self.update_json_status()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-body-btn":
            self.save_body()
    
    def save_body(self) -> None:
        if not self.is_valid_json():
            self.notify("Cannot save: Invalid JSON", severity="error", timeout=3)
            return
        
        body = self.get_body()
        if not body.strip():
            self.notify("Cannot save: Empty body", severity="warning", timeout=3)
            return
    
        self.notify("Body saved successfully!", severity="information", timeout=3)
    
    def update_json_status(self) -> None:
        textarea = self.query_one("#body-textarea", TextArea)
        status = self.query_one("#json-status", Static)
        
        text = textarea.text.strip()
        
        if not text:
            status.update("Empty (Valid)")
            status.remove_class("json-invalid")
            status.add_class("json-valid")
            return
        
        try:
            json.loads(text)
            status.update("Valid JSON")
            status.remove_class("json-invalid")
            status.add_class("json-valid")
        except json.JSONDecodeError as e:
            status.update(f"Invalid JSON: {e.msg} at line {e.lineno}")
            status.remove_class("json-valid")
            status.add_class("json-invalid")
    
    def get_body(self) -> str:
        textarea = self.query_one("#body-textarea", TextArea)
        return textarea.text
    
    def is_valid_json(self) -> bool:
        text = self.get_body().strip()
        if not text:
            return True
        try:
            json.loads(text)
            return True
        except json.JSONDecodeError:
            return False
    
    def get_json(self) -> dict | list | None:
        text = self.get_body().strip()
        if not text:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None