from gensim.models import Word2Vec
from multiprocessing import Process, Manager, Pool
from settings import MODEL_FILE, MSD_METADATA_FILE, MODEL_SIZE
import json
import linalg
import numpy as np
import random
import sys
import heapq

def query(MSD,lst,target):
	start = {}
	end = {}
	for idx,item in enumerate(lst):
		vector = MSD[item]['wv']
		if not idx:
			basis = np.array([vector])
		else:
			basis = np.vstack((basis,vector))
		status = start.get( MSD[item]['artist'], 0)
		if status:
			start[ MSD[item]['artist'] ] += [MSD[item]['title']]
		else:
			start[ MSD[item]['artist'] ] = [MSD[item]['title']]

		target_word = MSD[target]['wv']

		f, d, b = linalg.most_similar(basis,target_word)
		heap = []

		for vector in b:
			similar = model.wv.similar_by_vector(vector,topn=10)
			for sim in similar:
				song_id = sim[0]
				song_score = sim[1]		
			
				title = MSD[song_id]['title']
				artist = MSD[song_id]['artist']
				status = end.get( artist, 0)
				if status:
					end[artist] += [(song_score,title,song_id)]
				else:
					end[artist] = [(song_score,title,song_id)]
		for key in end:
			sum_lst = [ 1 - tup[0] for tup in end[key] ]
			proximity_sum = sum(sum_lst) / len(sum_lst)
			titles = [ tup[1] for tup in end[key] ]
			artist = key
			heapq.heappush(heap, (proximity_sum, artist, titles) )
		
		return heap
		
def fill_author(MSD,name,size=MODEL_SIZE):
	keys = list(MSD.keys())
	lst = []
	for i,v in enumerate(keys):
		artist = MSD[keys[i]]['artist']
		for j,k in enumerate(name):
			if k.lower() in artist.lower():
				lst.append(keys[i])
		if len(lst) >= size:
			break
	return lst
			
if __name__ == '__main__':

	with open(MSD_METADATA_FILE,'r') as f:
		MSD = json.load(f)

	MSD_keys = list(MSD.keys())
	model = Word2Vec.load(MODEL_FILE)
	model_words = list(model.wv.index2word)
	model_vectors = [tuple(x) for x in list(model.wv.syn0)]

	model_dct = dict(zip(model_vectors,model_words))

	a = fill_author(MSD,['Arctic Monkeys','The Last Shadow Puppets', 'Mongrel', 'Reverend and the Makers', 'The Dodgems', 'The Rascals'])
	print(a)

	b = fill_author(MSD,['50 Cent'], 1)[0]
	print(b)
	
	h = query(MSD,a,b)

	while h:
		print(heapq.heappop(h))
