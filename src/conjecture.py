import ast
from fractions import Fraction


class Conjecture:
    def __init__(self, row):
        self.id = row["Conjecture ID"]
        self.text = row["Conjecture"]
        self.subgroup = row["Subgroup"]
        self.x_name = row["X"]
        self.y_name = row["Y"]
        self.sign = row["Sign"]
        self.coefficients = self._parse_coefficients(row["Coefficients"])
        self.intercept = self._parse_number(row["Intercept"])

    def _parse_coefficients(self, value):
        """
        Exemple dans Excel : ['-1/6', '0', '1/6']
        On transforme ça en nombres Python.
        """
        if isinstance(value, str):
            items = ast.literal_eval(value)
        else:
            items = value

        return [self._parse_number(x) for x in items]

    def _parse_number(self, value):
        """
        Transforme '1/6', '-3', 0, etc. en float.
        """
        if isinstance(value, str):
            return float(Fraction(value))
        return float(value)

    def f(self, x):
        """
        Calcule f(x) = intercept + c1*x + c2*x² + c3*x³ ...
        """
        total = self.intercept

        for power, coef in enumerate(self.coefficients, start=1):
            total += coef * (x ** power)

        return total

    def violation(self, invariants):
        """
        Calcule le score de violation.

        Si conjecture : Y <= f(X)
        violation = Y - f(X)

        Si conjecture : Y >= f(X)
        violation = f(X) - Y

        Un contre-exemple est trouvé si violation > 0.
        """
        x = invariants[self.x_name]
        y = invariants[self.y_name]
        fx = self.f(x)

        if self.sign == "<=":
            return y - fx

        if self.sign == ">=":
            return fx - y

        raise ValueError(f"Signe inconnu : {self.sign}")

    def is_counterexample(self, invariants):
        return self.violation(invariants) > 0

    def __str__(self):
        return f"Conjecture {self.id}: {self.text}"