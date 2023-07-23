import argparse
import os
from pathlib import Path

import orjson
import pandas as pd


def view_results(result_file: str):
    with open(result_file, "rb") as f:
        eval_results = orjson.loads(f.read())

    report = {}
    for name in sorted(eval_results["accuracy"].keys()):
        name_split = name.split("___", 1)
        if len(name_split) == 2:
            config_set, task_filename = name_split
        else:
            config_set = "default"
            task_filename = name

        eval_set  = os.path.dirname(task_filename)
        eval_name = Path(task_filename).stem

        report.setdefault(config_set, {})
        report[config_set].setdefault(eval_set, {"name": [], "accuracy": [], "unmatched": []})
        
        report[config_set][eval_set]["name"].append(eval_name)
        report[config_set][eval_set]["accuracy"].append(eval_results["accuracy"][name])
        report[config_set][eval_set]["unmatched"].append(eval_results["unmatched"][name])

    for config_set, eval_sets_report in report.items():
        print(f"\n{config_set}\n==========")

        # eval set
        for eval_set, result_df in eval_sets_report.items():
            result_df = pd.DataFrame.from_dict(result_df)
            result_df.loc[len(result_df)] = {
                "name": "Average",
                "accuracy": result_df["accuracy"].mean(),
                "unmatched": result_df["unmatched"].mean()
            }

            print(f"\n## {eval_set}\n")
            print(result_df.to_markdown(index=False, floatfmt=".3f"))


def main():
    parser = argparse.ArgumentParser()

    # Input / output
    parser.add_argument("result_file", type=str, default="mcq_eval_result.json")

    args = parser.parse_args()

    view_results(**vars(args))

if __name__ == "__main__":
    main()
