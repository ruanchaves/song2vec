import random
from settings import MODEL_SIZE, MSD_CORPUS_FILENAME, MSD_BUFFER_SIZE, METADATA_FILE, DEFAULT_DICT, MAX_HEAP_SIZE
import json
from difflib import SequenceMatcher
import datetime
import numpy as np
import heapq
import time
import multiprocessing as mp

def attempt(lst,var_id):
	try:
		return lst[var_id]
	except:
		return ''

def words_to_id(keys,values,iterator,lst):
	id_collection = []
	fields = ['artist','title']
	for i,v in enumerate(lst):	
		for f in fields:
			np.random.shuffle(iterator)
			for j in iterator:
				if v.lower() in values[j][f].lower():
					yield keys[j]
	yield None

		
def similarity_query(model,MSD,word,sep='-'):
	fields = ['artist', 'title']
	values = []

	keys = list(MSD.keys())
	heap = []
	for j,k in enumerate(keys):
		for i,v in enumerate(fields):
			try:
				ratio = 1 - SequenceMatcher(MSD[word][v],MSD[k][v]).ratio()
			except:
				break
			heapq.heappush(heap,(ratio,k))
			if len(heap) == MAX_HEAP_SIZE:
				while heap:
					rec = heapq.heappop(heap)
					yield rec[1]

	while 1:
		recommendation = list(model.wv.vocab.keys())	
		random_rec = random.choice(recommendation)
		yield random_rec

def build_MSD(model):
	MSD_dct = {}
	with open(MSD_CORPUS_FILENAME,'r') as f:
		MSD_lst = f.read().split('\n')
		for line in MSD_lst:
			s = line.split('<SEP>')
			song_id = attempt(s,1)
			title = attempt(s,2)
			artist = attempt(s,3)
			MSD_dct[song_id] = {'title' : title, 'artist' : artist}

	try:
		with open(METADATA_FILE,'r') as handle:
			D = json.load(handle)
	except:
		open(METADATA_FILE,'w+').close()
		D = DEFAULT_DICT
	
	pairs = list(zip(*list(MSD_dct.items())))
	keys = pairs[0]
	values = pairs[1]


	model_words = list(model.wv.index2word)
	model_vectors = list(model.wv.syn0)
	model_dct = dict(zip(model_words,model_vectors))

	final_dct = {}
	for j,k in enumerate(keys):
		try:
			word_vector = model_dct[k]
		except:
			options = similarity_query(model,MSD_dct,k)
			for o in options:
				try:
					word_vector = model_dct[o]
					break
				except:
					continue
		with open('debug.txt','a') as f:
			print('1',file=f)
		final_dct[k] = MSD_dct[k]
		final_dct[k]['wv'] = word_vector.tolist()
		final_dct_size = len(final_dct)
		if not final_dct_size % MSD_BUFFER_SIZE:
			now = str(datetime.datetime.now())
			print('Word vectors calculated for {0} songs. Saved to {1} at {2}'.format(final_dct_size,METADATA_FILE,now))
			D['MSD'] = final_dct
			with open(METADATA_FILE,'w') as handle:
				json.dump(D,handle)
	D['MSD'] = final_dct
	with open(METADATA_FILE,'w') as handle:
		json.dump(D,handle)
	return final_dct

def check_MSD(model):
	try:
		with open(METADATA_FILE,'r') as handle:
			D = json.load(handle)
		if D['MSD'] == None:
			return build_MSD(model)
		else:
			return D['MSD']
	except:
		return build_MSD(model)
