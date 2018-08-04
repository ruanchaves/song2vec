from gensim.models import Word2Vec
from multiprocessing import Process, Manager, Pool
from settings import MODEL_FILE, MSD_METADATA_FILE, MODEL_SIZE, YOUTUBE_API_KEY
import json
import linalg
import numpy as np
import random
import sys
import heapq
import yapi
import re

def get_url(api,args,N=1,order=None):
	x = api.video_search(args,max_results=N,order=order)
	return [ v['videoId'] for v in [ vars(z['id']) for z in [ vars(y) for y in vars(x)['items'] ] ] ]

def get_playlist(lst_gen,size=20):	
	for lst in lst_gen:
		yield "https://www.youtube.com/watch_videos?video_ids={0}".format(','.join(lst[i:i+size]))

def get_walk(model,api,basis,size=20):
	vectors = linalg.walk(basis,n=2)
	for v in vectors:
		i = 0
		lst = []
		while i < size:
			song_id = model.wv.similar_by_vector(v,topn=1)[0]
			lst.append(get_url(api,song_id))
			i += 1
		yield lst	

def query(MSD,lst,target,api=None):
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
		h = []
		check = []

		yield b

		for vector in b:
			similar = model.wv.similar_by_vector(vector,topn=10)
			for sim in similar:
				song_id = sim[0]
				song_score = sim[1]		
			
				title = MSD[song_id]['title']
				artist = MSD[song_id]['artist']
				status = end.get( artist, 0)
				tup = (song_score,title,song_id)
				if status:
					end[artist] += [tup]
				else:
					end[artist] = [tup]
		end_map = {}
		for idx,key in enumerate(end):
			sum_lst = [ 1 - tup[0] for tup in end[key] ]
			if sum_lst:
				proximity_sum = sum(sum_lst) / len(sum_lst)
			else:
				proximity_sum = 1
			titles = [ tup[1] for tup in end[key] ]
			song_ids = [ tup[2] for tup in end[key] ]
			artist = key
			end_map[idx] = {"artist" : artist, "titles" : titles, "song_ids" : song_ids }
			heapq.heappush(h, (proximity_sum, idx) )
		
		while h:	
			tup = heapq.heappop(h)
			idx = tup[1]
			dct = end_map[idx]
			if api:
				for i,v in enumerate(dct['titles']):
					search_string = '{0} {1}'.format(dct['artist'],v)
					try:
						url = get_url(api,search_string)[0]
					except:
						url = None
				yield tup, url
			else:
				yield tup, None
		
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

	a = fill_author(MSD,['Nirvana','Foo Fighters', 'Marigold', 'Sappy'])

	b = fill_author(MSD,['Pink Floyd'], 1)[0]
	
	api = yapi.YoutubeAPI(YOUTUBE_API_KEY)
	
	h = query(MSD,a,b,api)
	basis = next(h)
#	lst = []
#	i = 0
#	for tup,url in h:
#		i += 1
#		if url:
#			lst.append(url)
#			if not i % 20:
#				links = get_playlist(lst)
#				for link in links:
#					print(link)

	
	more = get_playlist(get_walk(model,api,basis))
	for link in more:
		print('more',more)
