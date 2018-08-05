from gensim.models import Word2Vec
import json
import multiprocessing

# Put below your Youtube and Telegram API keys.
YOUTUBE_API_KEY = ''
TELEGRAM_API_KEY = ''

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
CHUNK_SIZE = 1024 * 1024 * 1024
## You may want to experiment with values on the 1024 * 1024 * 16 ~~ 1024 * 1024 * 1024 range.

# How many processor cores you have and/or want this program to utilize.
PROCESSOR_CORES = multiprocessing.cpu_count()


# The parameters below will be utilized while training the word2vec model.
MODEL_FILE = 'word2vec.model'
MODEL_SIZE = 128
MODEL_WINDOW = 5
MODEL_MIN_COUNT = 1
MODEL_WORKERS = 4
MODEL_EPOCHS = 5

#You can play around with this parameter to improve recommendations. Accepted values are on the (0,1] interval.
LOWER_BOUND = 0.95

DEFAULT_DICT = {
		'read_counter' : 0,
		'MSD' : None
		}
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
