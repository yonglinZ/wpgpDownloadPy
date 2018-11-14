from typing import List
from collections import namedtuple
import warnings
import platform
import sys
import gzip
import csv

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

BASE_ROOT = Path(__file__).parent
CSV_FILE = BASE_ROOT / '..' / 'data' / 'wpgpDatasets.csv.gz'
_Product = namedtuple('Product', 'idx numeric alpha3 country_name dataset_name description path')
_records = []

if platform.system() == 'Windows':
    if sys.version_info.major == 3 and sys.version_info.minor >= 6:
        encoding = 'oem'
    else:
        encoding = 'utf-8'
else:
    encoding = 'utf-8'

with gzip.open(CSV_FILE, 'rt', encoding=encoding, errors='replace') as csvfile:
    reader = csv.DictReader(csvfile)
    for idx, row in enumerate(reader, 1):
        # add each row to the records list
        _records.append(
            # idx numeric alpha3 country_name dataset_name description path
            _Product(int(row['ID']), row['ISO'], row['ISO3'], row['CountryName'], row['DataSetName'], row['Description'],
                     Path(row['PathToRaster']))
        )

def _build_index(iso):
    if iso is None:
        raise TypeError('ISO should not be None')
    res = dict((r.idx, r) for r in _records if r.alpha3 == iso)
    if len(res) == 0:
        warnings.warn('Found 0 products')

    return res


NOT_FOUND = object()


class _Products(object):

    def __init__(self, iso):
        self.products = _build_index(iso)

    def get(self, idx, default=NOT_FOUND):
        res = self.products.get(idx, default)
        if res == NOT_FOUND:
            raise KeyError
        return res

    def __getitem__(self, item):
        return self.get(item)

    def iter_download_urls(self):
        for p in self.products.values():
            yield p.Path

    def __iter__(self):
        for k, v in self.products.items():
            yield k, v

    def __len__(self):
        return len(self.products)

    def filter(self, filter=str):
        for k, v in self.products.items():
            if filter.lower() in v.description.lower():
                yield k, v


Product = _Products
