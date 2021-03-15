#!/usr/bin/env python
import os
import argparse
import numpy as np

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
    data_arg.add_argument('--num_train', type=int, default=10000)
    data_arg.add_argument('--num_test', type=int, default=1000)
    data_arg.add_argument('--num_val', type=int, default=1000)
    data_arg.add_argument('--num_in_out', type=int, default=10)
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
        errors = {}
        inputs, outputs, codes, codes_str, code_lengths = [], [], [], [], []
        for _ in trange(data_num):
            code = generator.random_program(stmt_max_depth=config.max_depth,
                                            template="sort_template")
            # print(code)
            code_ins = []
            code_outs = []
            same_in_out = 0
            for i in range(config.num_in_out):
                env = generator.random_env()
                start = env.to_tensor(colors=COLORS, shapes=SHAPES)
                # print(start)
                try:
                    execute(code, env, colors=COLORS, shapes=SHAPES)
                    output = env.to_tensor(colors=COLORS, shapes=SHAPES)
                    # print(output)
                except RuntimeError as e:
                    # print("runtime error: ", e)
                    if e in errors.keys():
                        errors[e] += 1
                    else:
                        errors[e] = 1
                    break
                except Exception as e:
                    # print("Exception: ", e)
                    if e in errors.keys():
                        errors[e] += 1
                    else:
                        errors[e] = 1
                    break
                if (start == output).all():
                    same_in_out += 1
                code_ins.append(start)
                code_outs.append(output)

            if same_in_out == config.num_in_out:
                print("no action done by program")
                continue
            if len(code_ins) == config.num_in_out \
                    or len(code_outs) != config.num_in_out:
                continue

            token_idxes = generator.code_to_idx(code)
            codes.append(token_idxes)
            code_lengths.append(len(token_idxes))
            codes_str.append(code)

            inputs.append(code_ins)
            outputs.append(code_outs)

        print(errors)
        npz_path = os.path.join(config.data_dir, name)
        np.savez(npz_path,
                 inputs=inputs,
                 outputs=outputs,
                 codes=codes,
                 codes_str=codes_str,
                 code_lengths=code_lengths)
