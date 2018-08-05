from .settings import YOUTUBE_API_KEY, TELEGRAM_API_KEY
from .settings import TELEGRAM_START_MESSAGE
from .settings import CORPUS_FILE, METADATA_FILE, SEARCH_HISTORY, MSD_CORPUS_FILENAME, MSD_METADATA_FILE
from .settings import MSD_BUFFER_SIZE, MAX_HEAP_SIZE, CHUNK_SIZE, PROCESSOR_CORES, LOAD_FACTOR
from .settings import MODEL_FILE, MODEL_SIZE, MODEL_WINDOW, MODEL_WORKERS, MODEL_EPOCHS, MODEL_SUBSAMPLE

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

from .MSDtools import MSD_builder, MSD_preprocess
