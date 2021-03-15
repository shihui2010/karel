from utils import prepare, set_random_seed

import os
import sys
import numpy as np
import tensorflow as tf

from trainer import Trainer
from config import get_config

config = None
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_VISIBLE_DEVICES"]="-1"  
#os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def main(_):
    prepare(config)
    rng = set_random_seed(config.seed)

    sess_config = tf.ConfigProto(
            log_device_placement=False,
            allow_soft_placement=False)
    sess_config.gpu_options.allow_growth=False

    trainer = Trainer(config, rng)

    with tf.Session(config=sess_config) as sess:
        if config.train:
            trainer.train(sess)
        else:
            if not config.map:
                raise Exception("[!] You should specify `map` to synthesize a program")
            trainer.synthesize(sess, config.map)

if __name__ == "__main__":
    config, unparsed = get_config()
    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
