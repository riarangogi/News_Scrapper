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


def _extract_host(df):
	logger.info('Extracting host from urls')
	df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
	return df


def _fill_missing_titles(df):
	logger.info('Filling missing titles')
	missing_titles_mask = df['title'].isna()
	missing_titles = (df[missing_titles_mask]['url']
						.str.extract(r'(?P<missing_titles>[^/]+)$')
						.applymap(lambda title: title.split('-'))
						.applymap(lambda title_word_list: ' '.join(title_word_list))
						)
	df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']
	return df


def _generate_uids_for_rows(df):
	logger.info('Generating uids for each row')
	uids = (df
			.apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
			.apply(lambda hash_object: hash_object.hexdigest())
			)
	df['uid'] = uids
	return df.set_index('uid')
