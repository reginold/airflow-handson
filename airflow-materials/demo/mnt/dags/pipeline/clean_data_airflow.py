from pathlib import Path

import click
import pandas as pd

from module.read_yaml import read_yaml


def _save_datasets(train, test, outdir: Path):
    """save cleaned train and test datasets and write SUCCESS flag."""
    # csv paths and flag path
    out_train = outdir / "train_cleaned.csv/"
    out_test = outdir / "test_cleaned.csv/"

    # save as csv and create flag file
    train.to_csv(str(out_train), index=False)
    test.to_csv(str(out_test), index=False)


def CleanData(df, drop_columns, target_name):
    """clean data by dropping unnecessary columns, duplicate rows and empty rows of target.

    Parameters
    ----------
    df: dataframe
        dataframe object to be cleaned
    drop_columns: list of strings
        column names to be dropped
    target_name: string
        name of the target variable

    Returns
    -------
    cleaned dataframe
    """

    interim_df = df.drop(columns=drop_columns)

    interim_df_2 = interim_df.drop_duplicates(ignore_index=True)

    cleaned_df = interim_df_2.dropna(subset=[target_name], how="any").reset_index(
        drop=True
    )

    return cleaned_df


# @click.command()
# @click.option("--in-train-csv")
# @click.option("--in-test-csv")
# @click.option("--out-dir")
# @click.option("--flag")
def clean_datasets(in_train_csv, in_test_csv, out_dir, flag):
    # create directory
    out_dir = Path(out_dir)

    # load data
    train_df = pd.read_csv(in_train_csv)
    test_df = pd.read_csv(in_test_csv)

    # list of drop columns
    drop_columns = ["designation", "winery", "region_2", "taster_twitter_handle"]

    # clean data
    cleaned_train = CleanData(train_df, drop_columns, "points")
    cleaned_test = CleanData(test_df, drop_columns, "points")

    _save_datasets(cleaned_train, cleaned_test, out_dir)


if __name__ == "__main__":
    # load the config yaml
    config = read_yaml()

    clean_datasets(
        in_train_csv=config["clean_dataset"]["in_train_csv"],
        in_test_csv=config["clean_dataset"]["in_test_csv"],
        out_dir=config["clean_dataset"]["out_dir"],
        flag=config["clean_dataset"]["flag"],
    )
