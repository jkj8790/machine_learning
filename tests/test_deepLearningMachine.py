from unittest import TestCase
from types import FunctionType
import numpy as np
import os

from hw import DeepLearningMachine
from hw import Perceptrons

TEST_FILE = os.path.join(os.path.dirname(__file__), 'test_trn.txt')

class TestDeepLearningMachine(TestCase):

    def setUp(self):
        fake_perceptrons = Perceptrons([13, 2, 2, 1])
        self.machine = DeepLearningMachine(fake_perceptrons)
        self.fake_data = [1] * 14

    def test_initialize(self):
        assert isinstance(self.machine, DeepLearningMachine)
        assert self.machine.epoch == 0
        assert self.machine.layers == []
        assert self.machine.weights == []
        assert self.machine.training_data == []
        assert isinstance(self.machine.perceptrons, Perceptrons)

    def test_predict_positive_discriminant_class1(self):
        self.machine.discriminant = lambda data : 1
        assert self.machine.predict(self.fake_data) == 1
        self.machine.discriminant = lambda data : 0.7
        assert self.machine.predict(self.fake_data) == 1
        self.machine.discriminant = lambda data : 0.55
        assert self.machine.predict(self.fake_data) == 1

    def test_predict_negative_discriminant_class0(self):
        self.machine.discriminant = lambda data : 0
        assert self.machine.predict(self.fake_data) == 0
        self.machine.discriminant = lambda data : 0.3
        assert self.machine.predict(self.fake_data) == 0
        self.machine.discriminant = lambda data : 0.4
        assert self.machine.predict(self.fake_data) == 0

    def test_learn_file_make_discriminant_function(self):
        with open(TEST_FILE) as file:
            self.machine.learn_file(file)

        assert isinstance(self.machine.discriminant, FunctionType)

    def test_learn_file_bring_variety_to_weight(self):
        initial_weights = []
        for step in range(len(self.machine.perceptrons.weights)):
            initial_weights.append(np.copy(self.machine.perceptrons.weights[step]))
        with open(TEST_FILE) as file:
            self.machine.learn_file(file)
        for initial_weight in initial_weights:
            assert not np.array_equal(initial_weight, self.machine.perceptrons.weights[step])

    def test_raw_str_to_data(self):
        fake_data = ["1.5"] * 13
        fake_data.insert(0, "0")

        data = self.machine.raw_str_to_data(fake_data)

        assert data['cls'] == 0
        assert data['data'].shape == (13, 1)

    def test_read_file(self):
        with open(TEST_FILE) as file:
            self.machine.read_file(file)

        cls_positive = sum(x['cls'] == 1 for x in self.machine.training_data)
        cls_negative = sum(x['cls'] == 0 for x in self.machine.training_data)
        cls_invalid = sum(x['cls'] != 0 and x['cls'] != 1 for x in self.machine.training_data)

        assert len(self.machine.training_data) == 4
        assert cls_positive == 2
        assert cls_negative == 2
        assert cls_invalid == 0

'''
    def test_converge_epoch_nine_false(self):
        for _ in range(8):
            self.machine.converge()

        assert not self.machine.converge()

    def test_converge_epoch_ten_true(self):
        for _ in range(9):
            self.machine.converge()

        assert self.machine.converge()
'''
