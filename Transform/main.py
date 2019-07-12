import argparse
import hashlib
import logging
import pandas as pd
from urllib.parse import urlparse

#configure message
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _read_data(filename):
	out_path = '../Data/Raw/'
	logger.info('Reading file {}'.format(filename))
	return pd.read_csv(out_path + filename)
