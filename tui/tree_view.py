import json
import re
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

    # Folding/Unfolding actions
    def fold_node(self):
        selected_node = self.selected
        if selected_node:
            selected_node.collapse()

    def unfold_node(self):
        selected_node = self.selected
        if selected_node:
            selected_node.expand()

    # Search actions
    def search(self, term):
        """Initialize a search for a term."""
        self.search_term = term
        self.search_results = self.search_nodes(self.root, term)
        self.current_search_index = 0
        self.move_to_search_result()

    def next_match(self):
        """Move to the next search result."""
        if self.search_results:
            self.current_search_index = (self.current_search_index + 1) % len(self.search_results)
            self.move_to_search_result()

    def previous_match(self):
        """Move to the previous search result."""
        if self.search_results:
            self.current_search_index = (self.current_search_index - 1) % len(self.search_results)
            self.move_to_search_result()

    def search_nodes(self, node, term):
        """Recursively search for nodes containing the search term."""
        results = []
        if re.search(term, node.label, re.IGNORECASE):
            results.append(node)
        for child in node.children:
            results.extend(self.search_nodes(child, term))
        return results

    def move_to_search_result(self):
        """Move selection to the current search result."""
        if self.search_results:
            self.select_node(self.search_results[self.current_search_index])
