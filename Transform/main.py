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
	try:
		missing_titles = (df[missing_titles_mask]['url']
						.str.extract(r'(?P<missing_titles>[^/]+)$')
						.applymap(lambda title: title.split('-'))
						.applymap(lambda title_word_list: ' '.join(title_word_list))
						)
		df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']
	except:
		next
	return df


def _generate_uids_for_rows(df):
	logger.info('Generating uids for each row')
	uids = (df
			.apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
			.apply(lambda hash_object: hash_object.hexdigest())
			)
	df['uid'] = uids
	return df.set_index('uid')


def _remove_new_lines_from_body(df):
	logger.info('Remove new lines from body')
	stripped_body = (df
					 .apply(lambda row: row['body'], axis=1)
					 .apply(lambda body: list(body))
					 .apply(lambda letters: list(map(lambda letter: letter.replace('\n', ' '), letters)))
					 .apply(lambda letters: ''.join(letters))
					 )
	df['body'] = stripped_body
	return df


def _remove_duplicate_entries(df, column_name):
	logger.info('Removing duplicate entries')
	df.drop_duplicates(subset=[column_name], keep='first', inplace=True)
	return df


def _drop_rows_with_missing_values(df):
	logger.info('Dropping rows with missing values')
	return df.dropna()


def _save_data(df, filename):
	in_path = '../Data/Tidy/'
	tidy_filename = 'tidy_{}'.format(filename)
	logger.info('Saving data at location: {}'.format(in_path + tidy_filename))
	df.to_csv(in_path + tidy_filename, index=False)


def main(filename):
	logger.info('Starting cleaning process')
	df = _read_data(filename)
	newspaper_uid = _extract_newspaper_uid(filename)
	df = _add_newspaper_uid_column(df, newspaper_uid)
	df = _extract_host(df)
	df = _fill_missing_titles(df)
	df = _generate_uids_for_rows(df)
	df = _remove_new_lines_from_body(df)
	df = _remove_duplicate_entries(df, 'title')
	df = _drop_rows_with_missing_values(df)
	_save_data(df, filename)
	return df


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('filename',
						help='The path to the dirty data',
						type=str)
	args = parser.parse_args()
	df = main(args.filename)

