import numpy as np
import math


class DataLoader:
    def __init__(self, file_name_training, file_name_test='', fill_missing=0.0, ignore_fields=None, class_field=-1, separator=','):
        if ignore_fields is None:
            ignore_fields = []
        self.has_test_set = False
        self.x_training = None
        self.y_training = None
        self.x_tests = None
        self.y_tests = None
        self.class_field = class_field
        self.xt = []
        self.yt = []
        self.class_values_training = []
        self.class_values_test = []
        self.first_iteration = True
        with open(file_name_training, 'r') as f:
            lines = f.readlines()
            self.xt = []
            self.yt = []
            j = 0
            for line in lines:
                separated = line.split(separator)
                '''if self.class_field == -1 and self.first_iteration:
                    self.class_field = len(separated) - 1'''
                if self.first_iteration:
                    self.first_iteration = False
                values = []
                for i in range(0, len(separated)):
                    if i not in ignore_fields and i != self.class_field:
                        try:
                            values.append(float(separated[i]))
                        except ValueError:
                            values.append(float(fill_missing))
                self.xt.append(values)
                self.yt.append(float(separated[self.class_field]))
                if float(separated[self.class_field]) not in self.class_values_training:
                    self.class_values_training.append(float(separated[self.class_field]))
                j += 1
            self.x_training = self.xt
            self.y_training = self.yt
        if file_name_test != '':
            self.has_test_set = True
            with open(file_name_test, 'r') as f:
                lines = f.readlines()
                self.xt = []
                self.yt = []
                j = 0
                for line in lines:
                    separated = line.split(separator)
                    values = []
                    for i in range(0, len(separated)):
                        if i not in ignore_fields and i != self.class_field:
                            try:
                                values.append(float(separated[i]))
                            except ValueError:
                                values.append(float(fill_missing))
                    self.xt.append(values)
                    self.yt.append(float(separated[self.class_field]))
                    if float(separated[self.class_field]) not in self.class_values_test:
                        self.class_values_test.append(float(separated[self.class_field]))
                    j += 1
                self.x_tests = self.xt
                self.y_tests = self.yt

    @staticmethod
    def normalize(vector):
        min_class_value = min(vector)
        if min_class_value < 0.0:
            for i in range(0, len(vector)):
                vector[i] += min_class_value
        max_class_value = max(vector)
        if max_class_value > 1.0:
            for i in range(0, len(vector)):
                vector[i] /= max_class_value

    @staticmethod
    def normalize2(vector):
        min_class_value = float('inf')
        for i in range(len(vector)):
            for j in range(len(vector[0])):
                if vector[i][j] < min_class_value:
                    min_class_value = vector[i][j]
        if min_class_value < 0.0:
            for i in range(0, len(vector)):
                for j in range(0, len(vector[0])):
                    vector[i][j] += math.fabs(min_class_value)
        max_class_value = float('-inf')
        for i in range(len(vector)):
            for j in range(len(vector[0])):
                if vector[i][j] > max_class_value:
                    max_class_value = vector[i][j]
        if max_class_value > 1.0:
            for i in range(0, len(vector)):
                for j in range(0, len(vector[0])):
                    vector[i][j] /= math.fabs(max_class_value)

    def __add_product(self):
        for i in range(0, len(self.x_training)):
            product = 1
            for j in range(0, len(self.x_training[i])):
                product *= self.x_training[i][j]
            self.x_training[i].append(product)
        if self.has_test_set:
            for i in range(0, len(self.x_tests)):
                product = 1
                for j in range(0, len(self.x_tests[i])):
                    product += self.x_tests[i][j]
                self.x_tests[i].append(product)

    def get_data(self, classification=False, normalize_outputs=False, normalize_inputs=False, add_product=False):
        if add_product:
            self.__add_product()
        if classification:
            self.class_values_training.sort()
            space_training = np.linspace(0.0, 1.0, len(self.class_values_training))
            space_test = []
            if self.has_test_set:
                self.class_values_test.sort()
                space_test = np.linspace(0.0, 1.0, len(self.class_values_test))
            for i in range(0, len(self.y_training)):
                for j in range(0, len(self.class_values_training)):
                    if self.y_training[i] == self.class_values_training[j]:
                        self.y_training[i] = space_training[j]
                        continue
            if self.has_test_set:
                for i in range(0, len(self.y_tests)):
                    for j in range(0, len(self.class_values_test)):
                        if self.y_tests[i] == self.class_values_test[j]:
                            self.y_tests[i] = space_test[j]
                            continue
        if normalize_outputs:
            self.normalize(self.y_training)
            if self.has_test_set:
                self.normalize(self.y_tests)
        if normalize_inputs:
            self.normalize2(self.x_training)
            if self.has_test_set:
                self.normalize2(self.x_tests)
        if self.has_test_set:
            return self.x_training, self.y_training, self.x_tests, self.y_tests
        else:
            return self.x_training, self.y_training
