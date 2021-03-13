import os
import numpy as np
import tensorflow as tf
from environment2D.generator import Generator

class Dataset(object):
    tokens = []
    idx_to_token = {}

    def __init__(self, config, load=True):
        self.config = config

        self.inputs, self.outputs, self.codes, self.code_lengths = {}, {}, {}, {}
        self.input_strings, self.output_strings = {}, {}
        self.with_input_string = False

        self.iterator = {}
        self._inputs, self._outputs, self._codes, self._code_lengths = {}, {}, {}, {}
        self._input_strings, self._output_strings = {}, {}

        self.data_names = ['train', 'test', 'val']
        self.data_paths = {
            key: os.path.join(config.data_dir, '{}.{}'.format(key, config.data_ext)) \
            for key in self.data_names
        }

        if load:
            self.load_data()
            for name in self.data_names:
                self.build_tf_data(name)

        self.generator = Generator(config.world_width, colors=config.colors, shapes=config.shapes)

    def build_tf_data(self, name):
        if self.config.train:
            batch_size = self.config.batch_size
        else:
            batch_size = 1

        # inputs, outputs
        data = [
            self._inputs[name], self._outputs[name], self._code_lengths[name]
        ]

        in_out = tf.data.Dataset.from_tensor_slices(tuple(data)).repeat()
        batched_in_out = in_out.batch(batch_size)

        # codes
        code = tf.data.Dataset.from_generator(lambda: self._codes[name], tf.int32).repeat()
        batched_code = code.padded_batch(batch_size, padded_shapes=[None])

        batched_data = tf.data.Dataset.zip((batched_in_out, batched_code))
        iterator = batched_data.make_initializable_iterator()

        (inputs, outputs, code_lengths), codes = iterator.get_next()

        inputs = tf.cast(inputs, tf.float32)
        outputs = tf.cast(outputs, tf.float32)
        code_lengths = tf.cast(code_lengths, tf.int32)

        self.inputs[name] = inputs
        self.outputs[name] = outputs
        self.codes[name] = codes
        self.code_lengths[name] = code_lengths
        self.iterator[name] = iterator

    def get_data(self, name):
        data = {
            'inputs': self.inputs[name],
            'outputs': self.outputs[name],
            'codes': self.codes[name],
            'code_lengths': self.code_lengths[name],
            'iterator': self.iterator[name]
        }
        if self.with_input_string:
            data.update({
                'input_strings': self.input_strings[name],
                'output_strings': self.output_strings[name],
            })
        return data

    def count(self, name):
        return len(self._inputs[name])

    def shuffle(self):
        raise NotImplementedError

    def load_data(self):
        raise NotImplementedError

    def idx_to_text(self, idxes):
        if hasattr(idxes[0], '__len__'):
            strings = [self.generator.idx_to_code(idx) for idx in idxes]
        else:
            strings = self.generator.idx_to_code(idxes)
        return np.array(strings)

    def load_data(self):
        self.data = {}
        for name in self.data_names:
            data = np.load(self.data_paths[name])
            self._inputs[name] = data['inputs']
            self._outputs[name] = data['outputs']
            self._codes[name] = data['codes']
            self._code_lengths[name] = data['code_lengths']
