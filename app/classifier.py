""""Shared module"""

from typing import Iterable

import joblib
from numpy import ndarray
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer

from .config import settings
from .models import Probabilities


class __classifier:
    """Wrapper for the classifier model

    Returns:
        Classifier: the classifier wrapped in a helper class.
    """

    def __init__(self):
        model_name = settings.MODEL
        mlb_name = settings.MLB
        self.model: Pipeline = joblib.load(model_name)
        self.__mlb: MultiLabelBinarizer = joblib.load(mlb_name)
        print(self.model)  # TODO: replace with logger
        print(self.__mlb)

    def predict_one(self, X: str) -> list[str]:
        """Classify an abstract

        Args:
            X (str): Abstract to classify

        Returns:
            List[str]: List of categories as strings
        """
        prediction = self.model.predict([X])
        return self.__mlb.inverse_transform(prediction)[0]

    def predict_proba_one(self, X: str) -> Probabilities:
        """Classify an abstract

        Args:
            X (str): Abstract to classify

        Returns:
            dict[str, Annotated[list[float], 2]]: List label probabilities
        """
        pred: ndarray = self.model.predict_proba([X])
        return {
            label: proba.tolist() for proba, label in zip(pred[0], self.__mlb.classes_)
        }

    def get_classes(self) -> list[str]:
        """Return the list of classes that the classifier is trained to predict

        Returns:
            List[str]: The list of classes
        """
        return self.__mlb.classes_

    def confusion_mat(
        self, X: Iterable[str], y: Iterable[Iterable[str]]
    ) -> tuple[int, int, int, int]:
        """Return the confusion matrix of the model as evaluated by the provided X, y

        Returns:
            tuple[int, int, int, int]: True negatives, False positives, False negatives, True positives in that order
        """
        y_test = self.__mlb.transform(y)
        pred = self.model.predict(X)
        mat = multilabel_confusion_matrix(y_test, pred)
        flattened = sum(mat)
        (tn, fp), (fn, tp) = flattened
        return int(tn), int(fp), int(fn), int(tp)


__model = __classifier()


def get_model():
    """Returns an instance of a classifier model

    Returns:
        Classifier:  the model
    """
    if __model:
        return __model
    return __classifier()


def get_classes() -> list[str]:
    """
    Return the list of classes that the classifier is trained to predict

    Returns:
        List[str]: The list of classes
    """
    return get_model().get_classes()
