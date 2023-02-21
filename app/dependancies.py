import random
from typing import List

class Classifier():
    classes = ['cs.ML', 'cs.AI', 'cs.LG']
    def predict(self, X: List[str]) -> List[str]:
        return [self.classes[random.randrange(0, 3)] for _ in X]

__model = Classifier()

def get_model():
    if __model:
        return __model
    return Classifier()