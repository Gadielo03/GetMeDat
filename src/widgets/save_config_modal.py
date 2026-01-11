from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Input
from services.file_service import save_config

class SaveConfigScreen(ModalScreen):
    """Screen with a dialog to save configuration."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Enter filename to save configuration:", classes="modal-title"),
            Input(placeholder="Enter filename", id="filename-input"),
            Button("Save", variant="primary", id="save", classes="dialog-button"),
            Button("Cancel", variant="error", id="cancel", classes="dialog-button"),
            classes="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            filename_input = self.query_one("#filename-input", Input)
            filename = filename_input.value.strip()
            if filename:
                if not filename.endswith('.json'):
                    filename += '.json'
                self.save_current_config(filename)
                self.app.pop_screen()
            else:
                self.notify("Please enter a filename", severity="warning", timeout=3)
        else:
            self.app.pop_screen()
            
    def save_current_config(self, filename) -> None:
        current_config = {
            "current_url": self.app.current_url,
            "current_method": self.app.current_method,
            "request_headers": self.app.request_headers,
            "request_body": self.app.request_body,
            "current_auth": self.app.current_auth,
            "current_params": self.app.current_params,
            "response_data": self.app.response_data,
            "response_headers": self.app.response_headers,
            "status_code": self.app.status_code,
            "error_message": self.app.error_message,
            "is_loading": self.app.is_loading,
            "timestamp": self.app.timestamp,
            "show_timestamps": self.app.show_timestamps,
            "auto_format_json": self.app.auto_format_json
        }
        save_config(current_config, filename)
        self.app.config
        self.notify(f"Configuration saved to {filename}", severity="information", timeout=3)