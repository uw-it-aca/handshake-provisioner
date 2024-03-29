#!/usr/bin/python3

import argparse
import pandas as pd

EXAMPLE_CSV = 'example.csv'
MISSING_OUTPUT_CSV = 'missing.csv'
EXTRA_OUTPUT_CSV = 'extra.csv'


def validate_csv(column, filepath, example_path, remove_cols):
    example_df = pd.read_csv(example_path)
    generated_df = pd.read_csv(filepath)

    example_df['card_id'] = example_df['card_id'].astype(str)
    generated_df['card_id'] = generated_df['card_id'].astype(str)

    example_netids = example_df[column].to_list()
    generated_netids = generated_df[column].to_list()

    example_netids.sort()
    generated_netids.sort()

    missing = set(example_netids) - set(generated_netids)
    missing_str = 'missing: ' + str(len(missing))

    extra = set(generated_netids) - set(example_netids)
    extra_str = 'extra: ' + str(len(extra))

    matching = set(generated_netids) & set(example_netids)
    matching_str = 'matching: ' + str(len(matching))

    all_list = set(example_netids) | set(generated_netids)
    all_str = 'uniques: ' + str(len(all_list))

    ex_str = 'example length: ' + str(len(example_netids))
    gen_str = 'generated length: ' + str(len(generated_netids))

    print(missing_str, extra_str, matching_str, all_str, ex_str, gen_str,
          sep=', ')

    missing_df = example_df[example_df[column].isin(missing)]
    extra_df = generated_df[generated_df[column].isin(extra)]
    matching_df = generated_df[generated_df[column].isin(matching)]
    matching_df2 = example_df[example_df[column].isin(matching)]

    matching_df.sort_values(by=column, inplace=True, ignore_index=True)
    matching_df2.sort_values(by=column, inplace=True, ignore_index=True)

    missing_df.to_csv(MISSING_OUTPUT_CSV, index=False)
    extra_df.to_csv(EXTRA_OUTPUT_CSV, index=False)

    pared_df = matching_df.drop(labels=remove_cols, axis=1)
    pared_df2 = matching_df2.drop(labels=remove_cols, axis=1)

    compare_df = pared_df.compare(pared_df2, align_axis=0)

    compare_df_copy = pared_df.compare(pared_df2, align_axis=0,
                                       keep_equal=True, keep_shape=True)
    compare_df_copy.drop_duplicates(inplace=True, keep=False)
    netid_col = compare_df_copy['username']
    compare_df.insert(0, 'username', netid_col)

    compare_df.insert(0, 'from',
                      ['example' if x % 2 else 'generated'
                       for x in range(len(compare_df))])

    compare_df.to_csv('comparison.csv', index=False)

    print('row differences: ', round(len(compare_df) / 2))
    print('cell differences: ', compare_df.count().drop(
            labels=['from', 'username']).sum())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='CSV file to validate')
    parser.add_argument('--example', '-e', help='Example file to compare to',
                        default=EXAMPLE_CSV)
    parser.add_argument('--column', '-c', help='Column to validate',
                        default='username')
    parser.add_argument('--remove-cols', '-r', nargs='*',
                        help='Columns to remove from comparison',
                        default=[])
    args = parser.parse_args()
    validate_csv(args.column, args.file, args.example, args.remove_cols)
