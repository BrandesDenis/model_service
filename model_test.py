from typing import List

import joblib
from sklearn.linear_model import LinearRegression

X = [[1], [2], [3], [4], [5], [6]]
y = [[x[0] ** 2] for x in X]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, 'model2.joblib')


class Test:
    pass


def test(a: int, b: str, c: Test) -> List[Test]:
    """

    Args:
        a ():
        b ():
        c ():

    Returns:

    """
    return []
