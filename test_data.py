import numpy as np
from environment2D.generator import Generator

data = np.load("./data/train.npz", allow_pickle=True)
inputs = data['inputs']
outputs = data['outputs']
codes = data['codes']
code_lengths = data['code_lengths']


COLORS = ["red", "yellow"]
SHAPES = ["round", "square"]
generator = Generator(10, colors=COLORS, shapes=SHAPES)
#print(codes[:10])
for c in codes[:10]:
    print(generator.idx_to_code(c))
