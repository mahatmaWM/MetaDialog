import logging

import argparse, time
import collections
import logging
import json
import math
import os
import random
from tqdm import tqdm, trange
import sys

parser = argparse.ArgumentParser()

# define path
parser.add_argument('--hello', required=False, help='the path to the training file.')
args = parser.parse_args()
logging.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
logging.info("{}".format(args.hello))
print(vars(args))

for ind in trange(int(10), desc="Epoch"):
    logging.info("procedding:{}".format(ind))
    time.sleep(0.5)
