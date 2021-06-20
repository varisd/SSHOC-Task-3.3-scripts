#!/usr/bin/env python3
import argparse
import json
import xml


def main(args):
    with open("{}.json".format(args.file_prefix), 'r') as f_in:
        data = json.load(f_in)

    filters = {}
    with open(args.filter_file, 'r') as f_in:
        for line in f_in:
            line = line.strip()
            filters[line] = 1

    data_out = { "data": [] }
    with open("{}.xml".format(args.file_prefix), 'w') as f_out:
        print('<?xml version="1.0" encoding="UTF-8"?>', file=f_out)
        print('<listBibl>', file=f_out)

        for i, entry in enumerate(data["data"]):
            PID = entry[8].split("_")[0]
            if PID not in filters:
                continue

            print('<entry n="{}">'.format(i), file=f_out)
            for j, item in enumerate(entry):
                print('\t<field n="{}">{}</field>'.format(j, item), file=f_out)

            print('</entry>', file=f_out)

        print('\n</listBibl>', file=f_out)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file-prefix", type=str, required=True,
        help="File prefix (in: .json, out: .xml).")
    parser.add_argument("--filter", type=str, required=True,
        help="File containing the list of allowed entries (their PPN numbers).")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
