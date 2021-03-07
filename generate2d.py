#!/usr/bin/env python
import os
import argparse
import numpy as np

from environment2D.environment import Grid2D
from environment2D.generator import Generator
from environment2D.executor import execute

try:
    from tqdm import trange
except:
    trange = range

COLORS = ["red", "yellow"]
SHAPES = ["round", "square"]

def makedirs(path):
    if not os.path.exists(path):
        print(" [*] Make directories : {}".format(path))
        os.makedirs(path)

if __name__ == '__main__':
    data_arg = argparse.ArgumentParser()
    data_arg.add_argument('--num_train', type=int, default=10)
    data_arg.add_argument('--num_test', type=int, default=5)
    data_arg.add_argument('--num_val', type=int, default=5)
    data_arg.add_argument('--num_examples', type=int, default=2)
    data_arg.add_argument('--data_dir', type=str, default='data')
    data_arg.add_argument('--max_depth', type=int, default=6)
    data_arg.add_argument('--mode', type=str, default='token', choices=['text', 'token'])
    data_arg.add_argument('--world_width', type=int, default=10, help='Width of square grid world')
    config = data_arg.parse_args()

    # Make directories
    makedirs(config.data_dir)
    datasets = ['train', 'test', 'val']

    # Generate datasets
    generator = Generator(config.world_width, colors=COLORS, shapes=SHAPES)

    for name in datasets:
        data_num = getattr(config, "num_{}".format(name))

        inputs, outputs, codes, code_lengths = [], [], [], []
        for _ in trange(data_num):
            while True:
                env = generator.random_env()
                start = env.state
                code = generator.random_program(stmt_max_depth=config.max_depth,
                                                template="sort_template")
                # print(code)
                # print(start)
                try:
                    execute(code, env, colors=COLORS, shapes=SHAPES)
                    output = env.state
                    # print(output)
                except RuntimeError as e:
                    print("runtime error: ", e)
                    continue
                if start == output:
                    print("no difference")
                    continue

                inputs.append(start)
                outputs.append(output)

                #token_idxes = generator.lex_to_idx(code, details=True)
                #codes.append(token_idxes)
                #code_lengths.append(len(token_idxes))
                break

        npz_path = os.path.join(config.data_dir, name)
        np.savez(npz_path,
                 inputs=inputs,
                 outputs=outputs,
                 codes=codes,
                 code_lengths=code_lengths)
