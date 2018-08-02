from cloud2vec_settings import *
import sys
import json
from gensim.test.utils import get_tmpfile
from gensim.models import Word2Vec
import datetime

def main():
	try:
		open(METADATA_FILE,'r').close()
	except:
		open(METADATA_FILE,'w+').close()
		with open(METADATA_FILE,'w') as handle:
			D = { 'read_counter' : 0 , 'previous_listener' : None }
			json.dump(D,handle)
	
	with open(METADATA_FILE,'r') as handle:
		D = json.load(handle)
	
	with open(CORPUS_FILE,'r') as f, open(METADATA_FILE,'r+') as handle:
		print('Preprocessing the next chunk of data... Press CTRL+C if you think this step is taking too long.')
		try:
			print('hi')
			session_counter = 0
			chunk_counter = 0
			word_counter = 0
			start_position = D['read_counter']
			corpus = []
			phrase = []
			previous_listener = D['previous_listener']
			for line in f:
				if session_counter >= start_position:
					line_text = line.split('\t')
					song = line_text[1]
					listener = line_text[0]
					
					if start_position == 0:
						previous_listener = listener	
						phrase.append(song)
					else:
						if previous_listener == listener:
							phrase.append(song)
						else:
							if len(phrase) > 1:
								corpus.append(phrase)
								word_counter += len(phrase)
							phrase = [song]
						previous_listener = listener
					
					if chunk_counter == CHUNK_SIZE:
						break
				
					chunk_counter += 1
					start_position += 1
					D['read_counter'] = start_position
					D['previous_listener'] = previous_listener
					handle.seek(0)
					json.dump(D,handle)
					handle.truncate()
				session_counter += 1
		except KeyboardInterrupt:
			pass
	
	print('Preprocessing is done. Now training word2vec... Press CTRL+C at any moment to end the program.')
	
	try:	
		try:
			open(MODEL_FILE,'r').close()
			model = Word2Vec.load(MODEL_FILE)
			model.train(corpus,total_examples=len(corpus),total_words=word_counter, epochs=MODEL_EPOCHS)
		except FileNotFoundError:
			path = get_tmpfile(MODEL_FILE)
			model = Word2Vec(corpus,MODEL_SIZE,MODEL_WINDOW,MODEL_MIN_COUNT,MODEL_WORKERS)
	except KeyboardInterrupt:
		return 1
	model.save(MODEL_FILE)
	print('Your model was saved. {0}'.format(str(datetime.datetime.now()))
	return 0

if __name__ == '__main__':
	while 1:
		status == main()
		if status:
			break
