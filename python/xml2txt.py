#!/usr/bin/env python3
import argparse
import re
import xml.etree.ElementTree as ET
import xml


def main(args):
    root = ET.parse('{}.xml'.format(args.file_prefix)).getroot()

    ns = ''
    matched = re.match(r'{.*}', root.tag)
    if matched is not None:
        ns = matched.group(0)
    for p in root.iter('{}p'.format(ns)):
        line = ' '.join(
            [''.join(w.itertext()) for w in p.iter('{}w'.format(ns))
        ])
        print(line)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file-prefix", type=str, required=True,
        help="File prefix (in: .json, out: .xml).")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
