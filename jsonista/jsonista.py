import re
import json
from typing import Any, Dict, List, Mapping, Union

class JsonDataManager:
    def __init__(self, json_data: Mapping | str):
        if isinstance(json_data, Mapping):
            self.data = json_data
        else:
            with open(json_data) as json_file:
                self.data = json.load(json_file)

    def get_all_data(self) -> Mapping:
        return self.data

    def get_filtered_data(self, text_filter: str) -> Dict[Any, Any] | List[Any] | None:
        return filter_mapping_by_regex(self.data, text_filter)


def filter_mapping_by_regex(
    data: Mapping[Any, Any], pattern: str
) -> Dict[Any, Any] | List[Any] | None:
    regex = re.compile(pattern)

    def recursive_filter(element: Any) -> Union[Dict[Any, Any], List[Any], Any, None]:
        if isinstance(element, Mapping):
            filtered_dict = {}
            for key, value in element.items():
                filtered_value = recursive_filter(value)
                if filtered_value is not None:
                    filtered_dict[key] = filtered_value
            return element if filtered_dict else None

        elif isinstance(element, list):
            filtered_list = []
            for item in element:
                filtered_item = recursive_filter(item)
                if filtered_item is not None:
                    filtered_list.append(filtered_item)
            return filtered_list if filtered_list else None

        else:
            # Convert the leaf to string for regex matching
            if regex.search(str(element)):
                return element
            else:
                return None

    return recursive_filter(data)
