#!/usr/bin/env python3
import argparse
import json
import xml


THRESHOLD = 1901


def main(args):
    with open('{}.json'.format(args.file_prefix), 'r') as f_in:
        data = json.load(f_in)

    filters = {}
    with open(args.filter, 'r') as f_in:
        for line in f_in:
            # Workaround for CRLF files
            if line == "\n":
                continue

            line = line.rstrip().split("\t")

            # Skipt the CSV header
            try:
                year = int(line[7])
            except ValueError:
                continue

            if year < THRESHOLD:
                key = line[11].split("=")[1]
                filters[key] = 1

    data_out = { 'data': [] }
    print('\t'.join(['Discipline', 'Name of Journal', 'Year/Number Of Issue/Vol.', 'Year', 'Language', 'Publisher', 'Number of pages', 'Unknown tag', 'Identifier']))
    for i, entry in enumerate(data['data']):
        PID = entry[8].split('_')[0]
        if PID not in filters:
            continue

        print('\t'.join(entry))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file-prefix", type=str, required=True,
        help="File prefix (in: .json, out: .xml).")
    parser.add_argument(
        "--filter", type=str, required=True,
        help="CSV File containing the list allowed entries.")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
