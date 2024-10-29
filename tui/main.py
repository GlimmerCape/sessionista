import json
import re
import sys
from textual.app import App, ComposeResult
from textual.widgets import Tree
from textual.reactive import reactive

class JsonTreeView(Tree):
    def __init__(self, json_path):
        super().__init__("JSON Viewer")
        self.json_path = json_path
        self.search_term = ""
        self.search_results = []
        self.current_search_index = 0
        self.load_json_tree()

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
    def search(self):
        self.search_term = input("Enter search term: ")
        self.search_results = self.search_nodes(self.root, self.search_term)
        self.current_search_index = 0
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

class JsonTreeApp(App):
    JSON_PATH = reactive("")

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("zc", "fold_node", "Collapse Node"),
        ("zo", "unfold_node", "Expand Node"),
        ("/", "search", "Search"),
        ("n", "next_match", "Next Match"),
        ("N", "previous_match", "Previous Match"),
        ("j", "move_down", "Move Down"),
    ]

    def __init__(self, json_path):
        super().__init__()
        self.JSON_PATH = json_path

    def compose(self) -> ComposeResult:
        self.tree_view = JsonTreeView(self.JSON_PATH)
        yield self.tree_view

    def action_fold_node(self) -> None:
        self.notify('zc', title='key pressed')
        self.tree_view.action_toggle_node()

    def action_unfold_node(self) -> None:
        self.tree_view.action_toggle_node()

    def action_search(self) -> None:
        self.tree_view.search()

    def action_next_match(self) -> None:
        self.tree_view.next_match()

    def action_previous_match(self) -> None:
        self.tree_view.previous_match()

    def action_move_down(self) -> None:
        self.notify('j', title='key-pressed')
        self.tree_view.action_toggle_node()
        self.tree_view.action_cursor_down()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_json>")
        sys.exit(1)

    json_path = sys.argv[1]
    app = JsonTreeApp(json_path)
    app.run()
