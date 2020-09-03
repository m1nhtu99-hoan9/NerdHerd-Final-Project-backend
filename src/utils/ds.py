""" 
  Data Structures customisation
"""

import json
from collections import namedtuple


def json_loads_to_named_tuple(jsonified_string: str, type_name: str):
    """Description: 
        convert `jsonified_string` into a list of named tuples
        or an named tuple having type of `type_name`
    """
    return json.loads(
        jsonified_string,
        object_hook=lambda d: namedtuple(type_name, d.keys())(*d.values()),
    )

