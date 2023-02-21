""""Shared module"""
import random

class Classifier():
    """Dummy class

    Returns:
        Classifier: class that contains the dummy model
    """
    classes = ['cs.ML', 'cs.AI', 'cs.LG']
    def predict(self, X: list[str]) -> list[str]:
        """Return dummy 

        Args:
            X (List[str]): List of abstracts to classify

        Returns:
            List[str]: List of categories as strings, same length as input array
        """
        return [self.classes[random.randrange(0, 3)] for _ in X]

__model = Classifier()

def get_model():
    """Returns an instance of a classifier model

    Returns:
        Classifier:  the model
    """
    if __model:
        return __model
    return Classifier()
