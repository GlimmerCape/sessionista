from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Input

class CenteredInputBar(Widget):
    """A widget that displays a centered input bar."""
    
    DEFAULT_CSS = """
    CenteredInputBar {
        align: center middle;
        display: none;
        width: 50%;
        height: 10%;
    }
    CenteredInputBar.visible {
        display: block;
    }
    """
    BINDINGS = [
        Binding('enter', 'run_command', 'Run Command'),
        Binding('escape', 'close_input', 'Return to Normal Mode')
    ]

    def compose(self) -> ComposeResult:
        self.input = Input(placeholder="Enter command", id="input-bar")
        yield self.input

    def open_input(self) -> None:
        """Toggles the visibility of the input bar."""
        self.notify('try to call open input')
        if self.has_class("visible"):
            return
        self.notify('open input called')
        self.input.clear()
        self.toggle_class("visible")
        self.input.focus()

    def action_close_input(self) -> None:
        if not self.has_class("visible"):
            return
        self.toggle_class("visible")
        self.input.blur()

    def action_run_command(self) -> None:
        # running command?
        if self.input.value.startswith('f'):
            pass # filter
        self.action_close_input()
