from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label, TabbedContent, TabPane
from .query_params_panel_tabs.query_parameters_tab import QueryParametersTab
from .query_params_panel_tabs.query_headers_tab import QueryHeadersTab
from .query_params_panel_tabs.query_body_tab import QueryBodyTab
from .query_params_panel_tabs.query_auth_tab import QueryAuthTab

class QueryParametersPanel(Widget):
    """Display the Query Parameters."""

    BINDINGS = [
        ("1", "show_tab('parameters-tab')", "Parameters"),
        ("2", "show_tab('headers-tab')", "Headers"),
        ("3", "show_tab('body-tab')", "Body"),
        ("4", "show_tab('auth-tab')", "Auth"),
    ]
    
    DEFAULT_CLASSES = "query-params-panel"

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="parameters-tab"):
            with TabPane("Parameters", id="parameters-tab"):
                yield QueryParametersTab()
            with TabPane("Headers", id="headers-tab"):
                yield QueryHeadersTab()
            with TabPane("Body", id="body-tab"):
                yield QueryBodyTab()
            with TabPane("Auth", id="auth-tab"):
                yield QueryAuthTab()
    
    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab