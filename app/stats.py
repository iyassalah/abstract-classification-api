import os
import datetime

import numpy as np

from .database import stats_col
from .classifier import get_classes, get_model


def remove_sub_cat(cats: list[str]):
    return list(set([cat.split(".")[0] for cat in cats]))


dropped_cats = set(get_classes())


def select_cats(cats: str):
    return np.array(
        [cat for cat in remove_sub_cat(cats.split(" ")) if cat in dropped_cats]
    )


async def evalutate_classifier():
    current_path = os.path.abspath(__file__)
    parent_directory = os.path.dirname(current_path)
    df: np.ndarray = np.load(
        os.path.join(parent_directory, "../test.npy"), allow_pickle=True
    )
    X = df[:, 3]
    y = np.vectorize(select_cats, otypes=[np.ndarray])(df[:, 2])
    model = get_model()
    tn, fp, fn, tp = model.confusion_mat(X, y)
    # print(model.model.get_params())
    stats_col.insert_one(
        {
            "fp": fp,
            "tp": tp,
            "fn": fn,
            "tn": tn,
            "created": datetime.datetime.now(),
            "params": {},
        }
    )
    return
