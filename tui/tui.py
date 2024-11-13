import sys

from textual.app import App, ComposeResult
from textual.binding import Binding

from .json_tree_view import JsonTreeView


class JsonTreeApp(App):
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("l", "expand_current_node", "Expand Node"),
        Binding("h", "collapse_current_node", "Collapse Node"),
        Binding("/", "focus_on_search_input", "Search Input"),
        Binding("enter", 'search', "Search"),
        Binding("n", "next_match", "Next Match"),
        Binding("N", "previous_match", "Previous Match"),
        Binding("k", "move_up", "Move Down"),
        Binding("j", "move_down", "Move Down"),
    ]

    def __init__(self, json_path):
        super().__init__()
        self.JSON_PATH = json_path

    def compose(self) -> ComposeResult:
        self.tree_view = JsonTreeView(self.JSON_PATH)
        yield self.tree_view

    def action_expand_current_node(self) -> None:
        if not self.tree_view.cursor_node: return
        self.tree_view.cursor_node.expand()

    def action_collapse_current_node(self) -> None:
        curr_node = self.tree_view.cursor_node 
        if not curr_node: return
        if not curr_node.parent: 
            curr_node.collapse()
            return
        if curr_node.is_expanded:
            curr_node.collapse()
        else:
            curr_node.parent.collapse()
            self.tree_view.select_node(curr_node.parent)

    def action_search(self) -> None:
        self.tree_view.run_search()

    def action_focus_on_search_input(self) -> None:
        self.tree_view.focus_on_search_input()

    def action_next_match(self) -> None:
        self.tree_view.next_match()

    def action_previous_match(self) -> None:
        self.tree_view.previous_match()

    def action_move_down(self) -> None:
        self.tree_view.action_cursor_down()

    def action_move_up(self) -> None:
        self.tree_view.action_cursor_up()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    app = JsonTreeApp(json_path)
    app.run()

