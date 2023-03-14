""""Shared module"""
import os
import joblib


class __classifier:
    """Wrapper for the classifier model

    Returns:
        Classifier: the classifier wrapped in a helper class.
    """

    classes = ["cs.ML", "cs.AI", "cs.LG"]

    def __init__(self):
        model_name = os.getenv("MODEL") if os.getenv("MODEL") else "model.joblib"
        mlb_name = os.getenv("MLB") if os.getenv("MLB") else "mlb.joblib"
        self.__model = joblib.load(model_name)
        self.__mlb = joblib.load(mlb_name)
        print(self.__model)  # TODO: replace with logger
        print(self.__mlb)

    def predict_one(self, X: str) -> list[str]:
        """Classify an abstracts

        Args:
            X (List[str]): List of abstracts to classify

        Returns:
            List[str]: List of categories as strings
        """
        prediction = self.__model.predict([X])
        return self.__mlb.inverse_transform(prediction)[0]


__model = __classifier()

def get_model():
    """Returns an instance of a classifier model

    Returns:
        Classifier:  the model
    """
    if __model:
        return __model
    return __classifier()
