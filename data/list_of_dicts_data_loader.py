import json
import random
from itertools import combinations, product

class ListOfDictsDataLoader:
  @staticmethod
  def from_file(path):
    this = ListOfDictsDataLoader()
    with open(path) as f:
      this._data = json.load(f)
    return this

  @staticmethod
  def from_json(json_data):
    this = ListOfDictsDataLoader()
    this._data = json_data
    return this

  def keys(self):
    return self._data[0].keys()

  def key_values(self, key):
    return set([d[key] for d in self._data])

  def filter_by(self, exact=True, **kwargs):
    return ListOfDictsDataLoader.from_json(list(filter(
      lambda d: \
        all(d[k] in w for k,w in kwargs.items()) \
        if exact else \
        all(any(option in d[k] for option in w) for k,w in kwargs.items()),
      self._data
    )))

  def __len__(self):
    return len(self._data)

  def __getitem__(self, key):
    if type(key) is str:
      return [d[key] for d in self._data]
    elif type(key) is int:
      return self._data[key]
    else:
      return ListOfDictsDataLoader.from_json([{k: d[k] for k in key} for d in self._data])

  def random(self):
    return self._data[random.randint(0, len(self)-1)]

  def __iter__(self):
    return iter(self._data)

  def group_by(self, keys):
    return [self.filter_by(**{key: [k] for key,k in zip(keys, ks[:-1])}) for ks in product(*[self.key_values(key) for key in keys], [None])]

  def drop_duplicates(self):
    return ListOfDictsDataLoader.from_json([dict(t) for t in {tuple(d.items()) for d in self._data}])

  class ComparisonTuplesIterator:
    def __init__(self, data, same, size):
      self.data = data
      self.size = size
      self.same = same
      self.other_groups = product(*[data.key_values(s) for s in same], [None])
      self.next_group()

    def __iter__(self):
      return self

    def next_group(self):
      self.this_group = []
      while len(self.this_group) < self.size:
        try:
          self.this_group = self.data.filter_by(**{field: [value] for field,value in zip(self.same, next(self.other_groups)[:-1])})
        except StopIteration:
          self.this_group = None
          return False
      self.indices = combinations(range(len(self.this_group)), self.size)
      return True

    def __next__(self):
      try:
        return ListOfDictsDataLoader.from_json([self.this_group[i] for i in next(self.indices)])
      except StopIteration:
        if self.next_group():
          return next(self)
        else:
          raise StopIteration

  def get_tuples(self, same, size=2):
    return ListOfDictsDataLoader.ComparisonTuplesIterator(self, same, size)
