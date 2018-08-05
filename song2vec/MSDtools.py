from gensim.models import Word2Vec
from multiprocessing import Process, Manager, Pool
from settings import MODEL_FILE, MSD_CORPUS_FILENAME, MSD_METADATA_FILE, PROCESSOR_CORES
import json
import numpy

def MSD_builder(MSD_dct, model_dct, manager_dct, k):
	manager_dct[k] = { 'artist' : MSD_dct[k]['artist'] , 'title': MSD_dct[k]['title'], 'wv' : model_dct[k].tolist() }

def MSD_preprocess(manager_dct, line):
	def attempt(lst,var_id):
		try:
			return lst[var_id]
		except:
			return ''
	s = line.split('<SEP>')
	song_id = attempt(s,1)
	artist = attempt(s,2)
	title = attempt(s,3)
	if song_id:
		manager_dct[song_id] = {'title' : title, 'artist' : artist}
	

if __name__ == '__main__':
	model = Word2Vec.load(MODEL_FILE)
	model_words = list(model.wv.index2word)
	model_vectors = list(model.wv.syn0)
	model_dct = dict(zip(model_words,model_vectors))

	with open(MSD_CORPUS_FILENAME,'r') as f:
		MSD_lst = f.read().split('\n')
	
	manager = Manager()

	manager_dct = manager.dict()
	with Pool(processes=PROCESSOR_CORES) as pool:
		pool.starmap(MSD_preprocess, [(manager_dct, line) for line in MSD_lst] )	
	pool.close()
	pool.join()

	MSD_dct = manager_dct

	manager_dct = manager.dict()
	with Pool(processes=PROCESSOR_CORES) as pool:
		pool.starmap(MSD_builder, [(MSD_dct, model_dct, manager_dct, k) for k in model_words] )
	pool.close()
	pool.join()
	
	open(MSD_METADATA_FILE,'w+').close()
	
	with open(MSD_METADATA_FILE,'w') as f:
		json.dump(manager_dct.copy(),f)
