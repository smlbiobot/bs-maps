import csv
import os

import yaml
from box import Box


class Config():
    _cfg = None

    def __init__(self, src):
        self.src = src

    @property
    def config(self):
        if self._cfg is None:
            with open(self.src) as f:
                self._cfg = Box(yaml.load(f))
        return self._cfg

    def get_csv_path(self, name):
        return self.config.csv[name]


def parse_maps(config=None):
    csv_path = config.get_csv_path('maps')
    maps = []

    # read blocks
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        map = None
        for index, row in enumerate(reader):
            if index < 1:
                continue

            if row.get('Group'):
                if map is not None:
                    maps.append(map)

                map = dict(
                    name=row.get('Group'),
                    blocks=[]
                )

            map['blocks'].append(row.get('Data'))

    # save blocks as individual txt files
    for map in maps:
        path = os.path.join(config.config.maps_output, map.get('name') + '.txt')
        with open(path, 'w') as f:
            blocks = '\n'.join(map.get('blocks'))
            f.write(blocks)


def main(config=None):
    parse_maps(config=config)


if __name__ == '__main__':
    cfg = Config('./config.yml')
    main(config=cfg)
