from gensim.models import Word2Vec
import json
import multiprocessing

# Put below your Youtube and Telegram API keys.
YOUTUBE_API_KEY = ''
TELEGRAM_API_KEY = ''

TELEGRAM_START_MESSAGE = """
	I'm the song2vec bot, and I'll recommend you a YouTube playlist according to your favorite artists.

	COMMAND SYNTAX:
		Simply type /rec followed by a comma-separated list of artists.
	
	EXAMPLE:
		/rec Metallica, Nirvana, Pink Floyd, Iron Maiden, Ice Cube, Bob Marley, Rolling Stones, U2

	SOURCE CODE:
		Pull requests are welcome. http://github.com/ruanchaves/song2vec
	
	CREDIT:
		This bot utilizes The Echo Nest Taste Profile Subset of the Million Song Dataset as its database.
		https://labrosa.ee.columbia.edu/millionsong/tasteprofile

	DONATE:
		BTC address: 32tQxrFSkA8kkyEgq7PSh8AANghn3tfmX9
"""

# File locations
CORPUS_FILE = 'train_triplets.txt'
METADATA_FILE = 'metadata.json'
SEARCH_HISTORY = 'history.json'
MSD_CORPUS_FILENAME = 'unique_tracks.txt'
MSD_METADATA_FILE = 'msd_metadata.json'

# Block sizes for file I/O
MSD_BUFFER_SIZE = 1024
MAX_HEAP_SIZE = 1024
## The model will be retrained every CHUNK_SIZE bytes in your input data.
CHUNK_SIZE = 1024 * 1024 * 100 

# How many processor cores you have and/or want this program to utilize.
PROCESSOR_CORES = multiprocessing.cpu_count()


# The parameters below will be utilized while training the word2vec model.
MODEL_FILE = 'word2vec.model'

LOAD_FACTOR = 4
MODEL_WORKERS = PROCESSOR_CORES * LOAD_FACTOR
MODEL_SIZE = 100
MODEL_WINDOW = 3
MODEL_EPOCHS = 130

MODEL_SUBSAMPLE = 1 / (10 ** 5 )

try:
	MSD = json.load(open(MSD_METADATA_FILE,'r'))
except Exception as e:
	MSD = None
	print('settings Exception : ',e)
try:
	WORD2VEC_MODEL = Word2Vec.load(MODEL_FILE)
except Exception as e:
	WORD2VEC_MODEL = None
	print('settings Exception : ',e)
