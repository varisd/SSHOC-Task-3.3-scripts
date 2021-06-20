#!/usr/bin/env python3
import argparse
import re

from utils import extract_count_vectors


def main(args):
    sentences = []
    with open(args.input_file, "r") as fh:
        for line in fh:
            line = line.strip()
            sentences.append(line)

    vocab = extract_count_vectors(
        {"default": sentences},
        ngrams=args.n_grams,
        language=args.language)["default"]

    with open("{}.{}_gram.voc".format(args.output_prefix, args.n_grams), "w") as fh:
        for k, v in vocab.items():
            print("{}\t{}".format(k, v), file=fh)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-file", type=str, required=True,
        help="Location of the input plaintext file.")
    parser.add_argument(
        "--n-grams", type=int, default=1,
        help="n-gram size of the extracted vocabulary.")
    parser.add_argument(
        "--language", type=str, default="english",
        help="Input language.")
    parser.add_argument(
        "--output-prefix", type=str, required=True,
        help="Prefix of the output files.")
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
