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


def _extract_newspaper_uid(filename):
	logger.info('Extracting newspaper uid')
	newspaper_uid = filename.split('_')[0]
	logger.info('Newspaper uid detected: {}'.format(newspaper_uid))
	return newspaper_uid
