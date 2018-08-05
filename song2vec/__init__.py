from .settings import YOUTUBE_API_KEY, TELEGRAM_API_KEY
from .settings import TELEGRAM_START_MESSAGE, TELEGRAM_HELP_MESSAGE
from .settings import CORPUS_FILE, METADATA_FILE, SEARCH_HISTORY, MSD_CORPUS_FILENAME, MSD_METADATA_FILE
from .settings import MSD_BUFFER_SIZE, MAX_HEAP_SIZE, CHUNK_SIZE, PROCESSOR_CORES
from .settings import MODEL_FILE, MODEL_SIZE, MODEL_WINDOW, MODEL_WORKERS, MODEL_EPOCHS
from .settings import LOWER_BOUND, DEFAULT_DICT

try:
	open(MSD_METADATA_FILE,'r').close()
	from .settings import MSD
except:
	pass

try:
	open(MODEL_FILE,'r').close()
	from .settings import WORD2VEC_MODEL
except:
	pass

from .linalg import vector_projection, homogenous_solve, step, vec_dist, boil, corpus_to_base, most_similar, walk
from .MSDtools import MSD_builder, MSD_preprocess
from .query import get_url, get_playlist, get_walk, query, fill_author, get_more, playlist_from_query  
