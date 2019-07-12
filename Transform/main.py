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


def _add_newspaper_uid_column(df, newspaper_uid):
	logger.info('Filling newspaper_uid column with {}'.format(newspaper_uid))
	df['newspaper_uid'] = newspaper_uid
	return df
