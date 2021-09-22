from pathlib import Path

import click
import numpy as np
import pandas as pd

from module.read_yaml import read_yaml


def _save_datasets(train, test, outdir: Path):
    """Save data sets into nice directory structure and write SUCCESS flag."""
    # csv paths and flag path
    out_train = outdir / "train.csv/"
    out_test = outdir / "test.csv/"

    # save as csv and create flag file
    train.to_csv(str(out_train), index=False)
    test.to_csv(str(out_test), index=False)


# @click.command()
# @click.option('--in-csv')
# @click.option('--out-dir')
# @click.option('--flag')
def make_datasets(in_csv, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # create pandas dataframe
    ddf = pd.read_csv(in_csv, index_col="Unnamed: 0")

    # trigger computation
    n_samples = len(ddf)

    # TODO: implement proper dataset creation here
    # http://docs.dask.org/en/latest/dataframe-api.html

    # split dataset into train test feel free to adjust test percentage
    idx = np.arange(n_samples)

    # separate first 1000 rows as test set
    test_idx = idx[: n_samples // 10]
    test = ddf.loc[test_idx]

    # separate last 9000 rows as training set
    train_idx = idx[n_samples // 10 :]
    train = ddf.loc[train_idx]

    _save_datasets(train, test, out_dir)


if __name__ == "__main__":
    config = read_yaml()
    make_datasets(
        in_csv=config["make_dataset"]["in_csv"],
        out_dir=config["make_dataset"]["out_dir"],
    )
