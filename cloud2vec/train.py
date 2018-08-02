from cloud2vec_settings import *
import sys
import json
from gensim.test.utils import get_tmpfile
from gensim.models import Word2Vec
import datetime
import sys

default_dict = {
		'read_counter' : 0, 
		}

def main():

	try:
		open(METADATA_FILE,'r').close()
	except:
		open(METADATA_FILE,'w+').close()
		with open(METADATA_FILE,'w') as handle:
			D = default_dict
			json.dump(D,handle)
	
	with open(METADATA_FILE,'r') as handle:
		D = json.load(handle)

	
	with open(CORPUS_FILE,'rb') as f, open(METADATA_FILE,'r+') as handle:

		print('Preprocessing the next chunk of data...')

		corpus = []
		word_buffer = {}
		i = D['read_counter']
		pos = CHUNK_SIZE * i
		f.seek(pos)
		chunk = f.read(CHUNK_SIZE)
		if bool(chunk):
			chunk = chunk.decode('utf-8').split('\n')
			chunk = chunk[1:-1]
			word_counter = len(chunk)
			for index,item in enumerate(chunk):
				line = item.split('\t')
				isentry = word_buffer.get(line[0], 0)
				if isentry:
					word_buffer[line[0]] += [line[1]] * int(line[2])
				else:
					word_buffer[line[0]] = [line[1]] * int(line[2])
			corpus += word_buffer.values()
			word_buffer = {}
			i += 1
			D['read_counter'] = i
		else:
			print('Reached end of file.')
			D['read_counter'] = 0
			handle.seek(0)
			json.dump(D,handle)
			handle.truncate()
			return 1
			
		handle.seek(0)
		json.dump(D,handle)
		handle.truncate()

		
	print('Preprocessing is done. Now training word2vec...')

	try:
		open(MODEL_FILE,'r').close()
		model = Word2Vec.load(MODEL_FILE)
		model.train(corpus,total_examples=len(corpus),total_words=word_counter, epochs=MODEL_EPOCHS)
	except Exception as e:
		print(e)
		print('Creating {0}...'.format(MODEL_FILE))
		path = get_tmpfile(MODEL_FILE)
		model = Word2Vec(corpus,MODEL_SIZE,MODEL_WINDOW,MODEL_MIN_COUNT,MODEL_WORKERS)
	model.save(MODEL_FILE)
	print('Your model was saved. {0}'.format(str(datetime.datetime.now())))

	return 0

if __name__ == '__main__':
	while 1:
		status = main()
		if status:
			break
