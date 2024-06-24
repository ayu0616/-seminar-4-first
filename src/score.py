from pydantic import BaseModel


class CaseScore(BaseModel):
    true_positive: int = 0
    false_positive: int = 0
    false_negative: int = 0
    true_negative: int = 0

    @property
    def precision(self):
        if self.true_positive + self.false_positive == 0:
            return 0
        return self.true_positive / (self.true_positive + self.false_positive)

    @property
    def recall(self):
        if self.true_positive + self.false_negative == 0:
            return 0
        return self.true_positive / (self.true_positive + self.false_negative)

    @property
    def f1(self):
        if self.precision + self.recall == 0:
            return 0
        return 2 * self.precision * self.recall / (self.precision + self.recall)

    @property
    def accuracy(self):
        return (self.true_positive + self.true_negative) / (self.true_positive + self.false_positive + self.false_negative + self.true_negative)
