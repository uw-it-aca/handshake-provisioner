#!/usr/bin/python3

import argparse
import pandas as pd

EXAMPLE_CSV = 'example.csv'
MISSING_OUTPUT_CSV = 'missing.csv'
EXTRA_OUTPUT_CSV = 'extra.csv'
MATCHING_OUTPUT_CSV = 'matching.csv'


def validate_csv(filepath, example_path):
    example_df = pd.read_csv(example_path)
    generated_df = pd.read_csv(filepath)

    example_netids = example_df['username'].to_list()
    generated_netids = generated_df['username'].to_list()

    example_netids.sort()
    generated_netids.sort()

    missing = set(example_netids) - set(generated_netids)
    missing_str = 'missing: ' + str(len(missing))

    extra = set(generated_netids) - set(example_netids)
    extra_str = 'extra: ' + str(len(extra))

    matching = set(generated_netids) & set(example_netids)
    matching_str = 'matching: ' + str(len(matching))

    print(missing_str, extra_str, matching_str, sep=', ')

    missing_df = example_df[example_df['username'].isin(missing)]
    extra_df = generated_df[generated_df['username'].isin(extra)]
    matching_df = generated_df[generated_df['username'].isin(matching)]

    missing_df.to_csv(MISSING_OUTPUT_CSV, index=False)
    extra_df.to_csv(EXTRA_OUTPUT_CSV, index=False)
    matching_df.to_csv(MATCHING_OUTPUT_CSV, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='CSV file to validate')
    parser.add_argument('--example', '-e', help='Example file to compare to',
                        default=EXAMPLE_CSV)
    args = parser.parse_args()
    validate_csv(args.file, args.example)
