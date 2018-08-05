import multiprocessing
import json
from gensim.models import Word2Vec

CORPUS_FILE = '/home/ruan/train_triplets.txt'
MODEL_FILE = '/home/ruan/cloud2vec_data/word2vec.model'
METADATA_FILE = '/home/ruan/cloud2vec_data/metadata.json'
SEARCH_HISTORY = 'history.json'

MSD_FOLDER = '/home/ruan/MSD/'
MSD_CORPUS_FILENAME = 'unique_tracks.txt'
MSD_BUFFER_SIZE = 1024
MSD_METADATA_FILE = '/home/ruan/cloud2vec_data/msd_metadata.json'

CHUNK_SIZE = 1024 * 1024 * 10

MODEL_SIZE = 128
MODEL_WINDOW = 5
MODEL_MIN_COUNT = 1
MODEL_WORKERS = 4

MODEL_EPOCHS = 5

DEFAULT_DICT = {
		'read_counter' : 0,
		'MSD' : None
		}

YOUTUBE_API_KEY = 'AIzaSyBUSXXeNZMRP2fOE80jkLuF7ZB-TsDPcQE'
MAX_HEAP_SIZE = 1024
PROCESSOR_CORES = multiprocessing.cpu_count()

MSD = json.load(open(MSD_METADATA_FILE,'r'))

WORD2VEC_MODEL = Word2Vec.load(MODEL_FILE)

LOWER_BOUND = 0.95

TELEGRAM_API_KEY = '635288656:AAF_I6W2AAmY8hJzQMdC9tJ2nSsPuSd-vhg'
TELEGRAM_START_MESSAGE = """
	I'm the song2vec bot, and I'll recommend you two YouTube playlists according to your favorite artists.

	COMMAND SYNTAX:
		/rec followed by a comma-separated list of artists.
	
	EXAMPLE:
		/rec Bob Marley, Metallica, Nirvana, Alice In Chains, Iron Maiden

	Type /h for more.
"""

TELEGRAM_HELP_MESSAGE = """

	song2vec_bot

	COMMAND SYNTAX:
		/rec followed by a comma-separated list of artists.
	
	EXAMPLE:
		/rec Bob Marley, Metallica, Nirvana, Alice In Chains, Iron Maiden

	TIPS:
		Feel free to experiment but better results are expected if all artists after the first are 
		somewhat related between themselves and if the first artist is somewhat different from all others.

		You can submit up to 128 artists in a single command; all artists after the 128th will be ignored.

	SOURCE CODE:
		Pull requests are welcome. http://github.com/ruanchaves/song2vec
	
	CREDIT:
		This bot utilizes The Echo Nest Taste Profile Subset of the Million Song Dataset as its database.
		https://labrosa.ee.columbia.edu/millionsong/tasteprofile
"""
