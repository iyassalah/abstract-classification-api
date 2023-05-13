""""Shared module"""

import joblib
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
        self.__model: Pipeline = joblib.load(model_name)
        self.__mlb: MultiLabelBinarizer = joblib.load(mlb_name)
        print(self.__model)  # TODO: replace with logger
        print(self.__mlb)

    def predict_one(self, X: str) -> list[str]:
        """Classify an abstract

        Args:
            X (str): Abstract to classify

        Returns:
            List[str]: List of categories as strings
        """
        prediction = self.__model.predict([X])
        return self.__mlb.inverse_transform(prediction)[0]

    def predict_proba_one(self, X: str) -> Probabilities:
        """Classify an abstract

        Args:
            X (str): Abstract to classify

        Returns:
            dict[str, Annotated[list[float], 2]]: List label probabilities
        """
        return {
            label: proba.tolist()[0]
            for proba, label in zip(
                self.__model.predict_proba([X]), self.__mlb.classes_
            )
        }


__model = __classifier()


def get_model():
    """Returns an instance of a classifier model

    Returns:
        Classifier:  the model
    """
    if __model:
        return __model
    return __classifier()
