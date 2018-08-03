import linalg
from gensim.models import Word2Vec
from settings import MSD_CORPUS_FILENAME, MODEL_FILE, MODEL_SIZE
import sys
import numpy as np
import difflib
import random
import MSDtools

class Query(object):

	def __init__(self,keywords,target):

		self.model = Word2Vec.load(MODEL_FILE)
		self.MSD = MSDtools.check_MSD(self.model)
		self.keywords = keywords
		self.target = target
		
	def basis_parse(self,basis,N=1):
		basis_words = []
		for i,v in enumerate(basis):
			suggest = [x[0] for x in self.model.wv.similar_by_vector(v,topn=N)]
			if N == 1:
				suggest = suggest[0]
			basis_words.append(suggest)
		return basis_words
	
	def __call__(self,preference):
		kwd = MSDtools.words_to_id(self.MSD, self.keywords)
		tgt = MSDtools.words_to_id(self.MSD, self.target)[0]
		basis, dist, basis_to_target = linalg.most_similar(self.model,kwd,tgt)
		if preference == 'id':
			basis_words = self.basis_parse(basis)
			new_words = self.basis_parse(basis_to_target)
			return basis_words, new_words
			
n = Query(['Avril Lavigne','Miley Cyrus'],['Snoop Dogg'])
