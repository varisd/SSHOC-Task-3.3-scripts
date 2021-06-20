#!/usr/bin/env python3
import argparse
import json
import sys
import xml


def main(args):
    with open("{}.json".format(args.file_prefix), 'r') as f_in:
        data = json.load(f_in)

    counts = {
        1800 : 0,
        1849 : 0,
        1859 : 0,
        1869 : 0,
        1879 : 0,
        1889 : 0,
        1899 : 0,
        # 1909 : 0,
        # 1919 : 0,
        # 1925 : 0,
    }

    for entry in data["data"]:
        # Handling of "irregularities"
        try:
            year = entry[3].strip("[").strip("]")
            year = year.split("/")[0].split(".")[0].split("-")[0].split(" ")[0].split("[")[0]
            year = int(year)
        except:
            print("Warning: entry '{}' does not have a valid format.".format(entry[3]), sys.stderr)
            continue
        for max_year in sorted(counts, key=lambda x: x):
            if year <= max_year:
                counts[max_year] += 1
                continue

    with open("{}.xml".format(args.file_prefix), 'w') as f_out:
        print('<?xml version="1.0" encoding="UTF-8"?>\n<table>', file=f_out)

        print('<row>', file=f_out)
        print('<cell role="label">', file=f_out)
        print('<hi rend="color(#f00)">Time span</hi>', file=f_out)
        print('</cell>', file=f_out)
        print('<cell role="label">', file=f_out)
        print('<hi rend="color(#f00)">Number of issues</hi>', file=f_out)
        print('</cell>\n</row>', file=f_out)

        min_year = 1770
        for max_year in sorted(counts, key=lambda x: x):
            print('<row>', file=f_out)
            print('<cell>{}--{}</cell>'.format(min_year, max_year), file=f_out)
            print('<cell>{}</cell>'.format(counts[max_year]), file=f_out)
            print('</row>', file=f_out)
            min_year = max_year + 1
           
        print('</table>', file=f_out)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file-prefix", type=str, required=True,
        help="File prefix (in: .json, out: .xml).")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
