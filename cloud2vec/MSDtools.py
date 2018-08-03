import random
from settings import MODEL_SIZE, MSD_CORPUS_FILENAME, METADATA_FILE, DEFAULT_DICT
import json
import difflib

def attempt(lst,var_id):
	try:
		return lst[var_id]
	except:
		return ''

def words_to_id(MSD,lst):
	id_collection = []
	pairs = list(zip(*list(MSD.items())))
	keys = pairs[0]
	values = pairs[1]
	for i,v in enumerate(lst):
		for j,k in enumerate(values):
			if v.lower() in k.lower():
				id_collection.append(keys[j])
		if len(lst) > 1:
			try:
				return random.sample(id_collection,MODEL_SIZE)
			except:
				random.shuffle(id_collection)
				return id_collection
		else:
			return random.sample(id_collection,1)

def similarity_query(model,MSD,word,sep='-'):
	values = MSD[word].split(sep)
	with open('debug.txt','a') as f:
		print(values,file=f)
	for i,v in enumerate(values):
		recommendation = words_to_id(MSD,[v])
		if recommendation:
			for rec in recommendation:
				yield rec

	for i,v in enumerate(values):
		recommendation = difflib.get_close_matches(word, list(MSD.keys()))
		if recommendation:
			for rec in recommendation:	
				yield rec
	
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
			MSD_dct[song_id] = '{0} - {1}'.format(title,artist)

	try:
		with open(METADATA_FILE,'r') as handle:
			D = json.load(handle)
	except:
		open(METADATA_FILE,'w+').close()
		D = DEFAULT_DICT
	
	pairs = list(zip(*list(MSD_dct.items())))
	keys = pairs[0]
	values = pairs[1]

	final_dct = {}
	for j,k in enumerate(keys):
		try:
			word_vector = model.wv[k]
		except KeyError:
			options = similarity_query(model,MSD_dct,k)
			for o in options:
				try:
					word_vector = model.wv[o]
					break
				except:
					continue
		word_vector = { 'wv' : word_vector }
		with open('debug.txt','a') as f:
			print('1',file=f)
		final_dct[k] = [values[j], word_vector]
			
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
