from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Button, Input, DataTable
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.message import Message

class CrudTable(Widget):
    """A CRUD Table widget for managing key-value pairs."""

    DEFAULT_CLASSES = "crud-table"
    
    class DataChanged(Message):
        def __init__(self, data: dict) -> None:
            self.data = data.copy()
            super().__init__()
    
    data = reactive({})
    selected_row = None  
    original_key = None  
    original_value = None 
    button_mode = "add"
    
    def __init__(
        self, 
        title: str = "CRUD Table",
        key_placeholder: str = "Key",
        value_placeholder: str = "Value",
        table_id: str = "crud-table",
        initial_data: dict = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.key_placeholder = key_placeholder
        self.value_placeholder = value_placeholder
        self.table_id = table_id
        self.key_input_id = f"{table_id}-key-input"
        self.value_input_id = f"{table_id}-value-input"
        self.add_btn_id = f"{table_id}-add-btn"
        self.initial_data = initial_data or {}
    
    def compose(self) -> ComposeResult:
        yield Static(self.title, classes="crud-header")
        yield DataTable(id=self.table_id, cursor_type="row", zebra_stripes=True)
        
        with Horizontal(classes="crud-input-section"):
            yield Input(placeholder=self.key_placeholder, id=self.key_input_id, classes="crud-input")
            yield Input(placeholder=self.value_placeholder, id=self.value_input_id, classes="crud-input")
            yield Button("Add", variant="primary", id=self.add_btn_id, classes="crud-btn")
    
    def on_mount(self) -> None:
        table = self.query_one(f"#{self.table_id}", DataTable)
        table.add_columns("Key", "Value")        
        
        if self.initial_data:
            self.set_data(self.initial_data)
        else:
            self.data = {}
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == self.add_btn_id:
            if self.button_mode == "add":
                self.add_item()
            elif self.button_mode == "delete":
                self.delete_selected_row()
            elif self.button_mode == "modify":
                self.modify_item()
    
    def add_item(self) -> None:
        key_input = self.query_one(f"#{self.key_input_id}", Input)
        value_input = self.query_one(f"#{self.value_input_id}", Input)
        
        key = key_input.value.strip()
        value = value_input.value
        
        if key:
            self.data[key] = value
            table = self.query_one(f"#{self.table_id}", DataTable)
            table.add_row(key, value)
            key_input.value = ""
            value_input.value = ""
            key_input.focus()
            
            self.post_message(self.DataChanged(self.data))
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id in [self.key_input_id, self.value_input_id]:
            if self.button_mode == "add":
                self.add_item()
            elif self.button_mode == "modify":
                self.modify_item()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id in [self.key_input_id, self.value_input_id]:
            if self.selected_row is not None:
                key_input = self.query_one(f"#{self.key_input_id}", Input)
                value_input = self.query_one(f"#{self.value_input_id}", Input)
                
                if (key_input.value != self.original_key or 
                    value_input.value != self.original_value):
                    self.set_button_mode("modify")
                else:
                    self.set_button_mode("delete")
    
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id != self.table_id:
            return
            
        self.selected_row = event.row_key
        table = self.query_one(f"#{self.table_id}", DataTable)
        
        row_data = table.get_row(event.row_key)
        self.original_key = str(row_data[0])
        self.original_value = str(row_data[1])
        
        key_input = self.query_one(f"#{self.key_input_id}", Input)
        value_input = self.query_one(f"#{self.value_input_id}", Input)
        key_input.value = self.original_key
        value_input.value = self.original_value
        
        self.set_button_mode("delete")
    
    def delete_selected_row(self) -> None:
        if self.selected_row is None:
            return
        
        table = self.query_one(f"#{self.table_id}", DataTable)
        row_data = table.get_row(self.selected_row)
        key = str(row_data[0])
        
        table.remove_row(self.selected_row)
        
        if key in self.data:
            del self.data[key]
        
        self.selected_row = None
        self.original_key = None
        self.original_value = None
        self.clear_inputs()
        self.set_button_mode("add")
        
        self.post_message(self.DataChanged(self.data))
    
    def modify_item(self) -> None:
        if self.selected_row is None:
            return
        
        key_input = self.query_one(f"#{self.key_input_id}", Input)
        value_input = self.query_one(f"#{self.value_input_id}", Input)
        
        new_key = key_input.value.strip()
        new_value = value_input.value
        
        if not new_key:
            return
        
        table = self.query_one(f"#{self.table_id}", DataTable)
        
        if self.original_key != new_key and self.original_key in self.data:
            del self.data[self.original_key]
        
        self.data[new_key] = new_value
        
        table.remove_row(self.selected_row)
        table.add_row(new_key, new_value)
        
        self.selected_row = None
        self.original_key = None
        self.original_value = None
        self.clear_inputs()
        self.set_button_mode("add")
        
        self.post_message(self.DataChanged(self.data))
    
    def set_button_mode(self, mode: str) -> None:
        self.button_mode = mode
        button = self.query_one(f"#{self.add_btn_id}", Button)
        
        button.remove_class("delete-mode")
        button.remove_class("modify-mode")
        
        if mode == "add":
            button.label = "Add"
            button.variant = "primary"
        elif mode == "delete":
            button.label = "Delete"
            button.variant = "error"
            button.add_class("delete-mode")
        elif mode == "modify":
            button.label = "Modify"
            button.variant = "warning"
            button.add_class("modify-mode")
    
    def clear_inputs(self) -> None:
        key_input = self.query_one(f"#{self.key_input_id}", Input)
        value_input = self.query_one(f"#{self.value_input_id}", Input)
        key_input.value = ""
        value_input.value = ""
    
    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.data_table.id != self.table_id:
            return
            
        if event.row_key is None:
            self.selected_row = None
            self.original_key = None
            self.original_value = None
            self.clear_inputs()
            self.set_button_mode("add")
    
    def get_data(self) -> dict:
        return dict(self.data)
    
    def set_data(self, data: dict) -> None:
        self.data = dict(data)
        table = self.query_one(f"#{self.table_id}", DataTable)
        table.clear()
        for key, value in data.items():
            table.add_row(key, value)
        
        self.post_message(self.DataChanged(self.data))
