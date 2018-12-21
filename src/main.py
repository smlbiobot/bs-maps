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



def parse_locations():
    csv_path = config.get_csv_path('locations')
    global locations
    locations = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader):
            if index < 1:
                continue
            location = row
            location['key'] = 1500000 + index -1

            locations.append(location)

    import json
    print(json.dumps(locations))

def get_location(name=None):
    global locations
    for loc in locations:
        if loc.get('Name') == name:
            return loc

    return None


def parse_maps():
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

                name = row.get('Group').replace('_', '')
                if 'bank' in name.lower():
                    name = name[4:].title()
                loc = get_location(name=name) or {}
                key = loc.get('key')

                map = dict(
                    name=name,
                    blocks=[],
                    key=key
                )

            map['blocks'].append(row.get('Data'))


    # save blocks as individual txt files
    for map in maps:
        name = map.get('name')
        key = map.get('key') or ''
        path = os.path.join(
            config.config.maps_output,
            f"{key}-{name}.txt"
        )
        with open(path, 'w') as f:
            blocks = '\n'.join(map.get('blocks'))
            f.write(blocks)


def main():
    parse_locations()
    parse_maps()


if __name__ == '__main__':
    locations = None
    config = Config('./config.yml')
    main()
