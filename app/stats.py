import os

import numpy as np

from .database import stats_col
from .classifier import get_classes


def remove_sub_cat(cats: list[str]):
    return list(set([cat.split(".")[0] for cat in cats]))


dropped_cats = set(get_classes())


def select_cats(cats: list[str]):
    return [cat for cat in remove_sub_cat(cats) if cat in dropped_cats]


async def evalutate_classifier():
    current_path = os.path.abspath(__file__)
    parent_directory = os.path.dirname(current_path)
    df: np.ndarray = np.load(
        os.path.join(parent_directory, "../test.npy"), allow_pickle=True
    )
    # print(df.ndim)
    # np.info(df)
    # print(df[0][2].split(" "))
    # print(select_cats(df[0][2].split(" ")))
    X = df[:, 3]
    y = np.apply_along_axis(select_cats, 0, df[:, 2])
    print(X[0])
    print(y[0])
    # stats_col.insert_one({"fp"})
    return
