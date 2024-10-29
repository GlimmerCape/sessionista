import json
import re
import sys
import random
from textual.app import App, ComposeResult
from textual.widgets import Tree, Input
from textual.reactive import reactive
from textual.binding import Binding
from textual.events import Key

class JsonTreeView(Tree):
    def __init__(self, json_path):
        super().__init__("JSON Viewer")
        self.json_path = json_path
        self.search_term = ""
        self.search_results = []
        self.current_search_index = 0
        self.load_json_tree()

    def compose(self) -> ComposeResult:
        self.search_input = Input(placeholder="Search for: ")
        self.search_input.visible = False
        yield self.search_input

    def load_json_tree(self):
        with open(self.json_path) as json_file:
            data = json.load(json_file)
        self.display_tree(self, data)

    def display_tree(self, tree, data, parent=None):
        if isinstance(data, dict):
            for key, value in data.items():
                node = tree.root.add(key) if parent is None else parent.add(key)
                self.display_tree(tree, value, node)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                node = tree.root.add(f"[{index}]") if parent is None else parent.add(f"[{index}]")
                self.display_tree(tree, item, node)
        else:
            tree.root.add(f"{data}") if parent is None else parent.add(f"{data}")

    # Search actions
    def focus_on_search_input(self):
        if self.search_input.visible:
            self.search_input.visible = False
            self.focus()
        else:
            self.search_input.visible = True
            self.search_input.focus()

    def run_search(self):
        self.search_results = self.search_nodes(self.root, self.search_term)
        self.current_search_index = 0
        self.search_input.visible = False
        self.focus()
        self.move_to_search_result()

    def next_match(self):
        if self.search_results:
            self.current_search_index = (self.current_search_index + 1) % len(self.search_results)
            self.move_to_search_result()

    def previous_match(self):
        if self.search_results:
            self.current_search_index = (self.current_search_index - 1) % len(self.search_results)
            self.move_to_search_result()

    def search_nodes(self, node, term):
        results = []
        if re.search(term, node.label, re.IGNORECASE):
            results.append(node)
        for child in node.children:
            results.extend(self.search_nodes(child, term))
        return results

    def move_to_search_result(self):
        if self.search_results:
            self.select_node(self.search_results[self.current_search_index])

    def on_key(self, event: Key) -> None:
        """Change color on every key press."""
        # random_color = f"#{random.randint(0, 0xFFFFFF):06x}"
        # self.styles.scrollbar_color = random_color
        pass

class JsonTreeApp(App):
    JSON_PATH = reactive("")

    BINDINGS = [
        Binding("x", "quit", "Quit"),
        Binding("l", "expand_current_node", "Expand Node"),
        Binding("h", "collapse_current_node", "Collapse Node"),
        Binding("/,s", "focus_on_search_input", "Search Input"),
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
