from pydantic import BaseModel

from type.features import crf_label, CrfLabelSequence


class CaseScore(BaseModel):
    true_positive: int = 0
    false_positive: int = 0
    false_negative: int = 0
    true_negative: int = 0

    @classmethod
    def from_test_pred(cls, y_test: CrfLabelSequence, y_pred: CrfLabelSequence):
        true_positive = 0
        false_positive = 0
        false_negative = 0
        true_negative = 0
        for t, p in zip(y_test, y_pred):
            if t == p:
                if p == crf_label.NG:
                    true_negative += 1
                else:
                    true_positive += 1
            else:
                if p == crf_label.NG:
                    false_positive += 1
                else:
                    false_negative += 1
        return cls(true_positive=true_positive, false_positive=false_positive, false_negative=false_negative, true_negative=true_negative)

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
