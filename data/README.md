# ListOfDictsDataLoader README

## Overview
`ListOfDictsDataLoader` is a class designed to handle a list of dictionaries, primarily loaded from a JSON file or directly from JSON data. It provides various utility functions to access and manipulate the data in meaningful ways.
It assumes all the data entries (dictionaries) have the same structure, i.e. the same set of keys.

## Initialization
There are two static methods to create an instance of the class:

1. `from_file(path)`: Loads data from a JSON file given its path.
2. `from_json(json_data)`: Directly initializes the object from JSON data.

## Methods

### Basic Access and Modification

1. `keys()`: Returns the keys from the inner dictionaries in the list, i.e. fields.
2. `key_values(key)`: Given a key, it will return all unique values associated with that key from the list.
3. `filter_by(exact=True, **kwargs)`: Returns a new `ListOfDictsDataLoader` instance filtered by the specified key-value pairs. If `exact` is set to `True`, the filter would search for exact matches; otherwise, the match can be inclusive (substring).
4. `random()`: Returns a random dictionary from the list.
5. `drop_duplicates()`: Removes duplicate dictionaries from the list.

### Magic Methods

1. `__len__()`: Returns the number of dictionaries in the list.
2. `__getitem__(key)`: Fetches the dictionary at the specified index or dictionaries by specified keys (when a string or a list of strings is provided).
3. `__iter__()`: Returns an iterator over the list of dictionaries.

### Grouping and Combining

1. `group_by(keys)`: Groups the list by the given keys and returns a list of new `ListOfDictsDataLoader` objects for each unique combination of key values.
2. `get_tuples(same, size=2)`: Provides an iterator that yields combinations of dictionaries where specified keys have the same values. The `size` parameter determines the size of the combination.

### Internal Classes

1. `ComparisonTuplesIterator`: This is an internal iterator class used by `get_tuples` to produce combinations of dictionaries.

## Usage Example

```python
# Load data from a JSON file
loader = ListOfDictsDataLoader.from_file("data.json")

# Get all unique values for the key 'category'
categories = loader.key_values("category")

# Get a filtered loader for specific key-value pairs
filtered_loader = loader.filter_by(name=["John"], age=[23, 24, 25])

# Just keep "category," "type," and "name" columns
filtered_loader = filtered_loader[["category","type","name"]].drop_duplicates()

# Fetch a random dictionary from the list
random_dict = loader.random()

# Group by 'category' and 'type' keys
grouped_data = loader.group_by(["category", "type"])

# Get combinations of dictionaries where 'category' is the same
for tuple_data in loader.get_tuples(same=["category"]):
    print(tuple_data)
```
