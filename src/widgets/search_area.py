from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Input, Select, Button
from services.request_client import http_client

class SearchArea(Widget):
    """Display a search area."""

    def __init__(self):
        super().__init__()
        self.http_method = "GET"

    def compose(self) -> ComposeResult:
        yield Select(
            options=[
                ("GET", "GET"),
                ("POST", "POST"),
                ("PUT", "PUT"),
                ("DELETE", "DELETE"),
                ("PATCH", "PATCH"),
                ("HEAD", "HEAD")
            ],
            value="GET",
            classes="http-method-select",
            id="method-select"
        )
        yield Input(placeholder="Enter URL", classes="search-bar-input", id="url-input")
        yield Button("→", variant="primary", id="send-request-btn", classes="send-btn")

    def normalize_url(self, url: str) -> str:
        url = url.strip()
        if not url:
            return url
        
        if url.startswith(('http://', 'https://')):
            return url
        
        return f'https://{url}'

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "url-input":
            self.log(f"URL changed to: {event.input.value}")
            self.app.update_request(url=event.input.value)
            http_client.set_url(event.input.value)

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "method-select":
            self.http_method = event.value
            self.log(f"Method changed to: {event.value}")
            self.app.update_request(method=event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send-request-btn":
            input_url = self.query_one("#url-input", Input).value
            
            if not input_url:
                self.notify("Please enter a URL", severity="warning", timeout=3)
                return
                
            normalized_url = self.normalize_url(input_url)
            
            self.app.update_request(url=normalized_url, method=self.http_method)
            self.app.set_loading(True)
            
            http_client.set_url(normalized_url)
            self.notify(f"Sending {self.http_method} request to {normalized_url}", timeout=2)
            self.make_request(normalized_url)
    
    def make_request(self, url: str) -> None:
        try:
            method_map = {
                "GET": http_client.get_request,
                "POST": http_client.post_request,
                "PUT": http_client.put_request,
                "DELETE": http_client.delete_request,
                "PATCH": http_client.patch_request,
                "HEAD": http_client.head_request
            }
            
            method_map[self.http_method]()
            response = http_client.get_response()

            if response:
                try:
                    response_data = response.json()
                except:
                    response_data = {"text": response.text}
                
                self.app.update_response(
                    data=response_data,
                    headers=dict(response.headers),
                    status=response.status_code,
                    error="",
                    loading=False
                )
                
                self.notify(f"Response: {response.status_code}", severity="information", timeout=3)
            else:
                # No hay respuesta
                self.app.update_response(
                    data={"error": "No response received"},
                    headers={},
                    status=0,
                    error="No response received",
                    loading=False
                )
                self.notify("No response received", severity="warning", timeout=3)
            
        except Exception as e:
            # Error en la petición
            self.app.update_response(
                data={"error": str(e)},
                headers={},
                status=0,
                error=str(e),
                loading=False
            )
            self.notify(f"Error: {str(e)}", severity="error", timeout=5)
        