import pywordwalk as pww
from nltk.corpus import brown
from gensim.models import Word2Vec
import sys
import numpy as np
from nltk import FreqDist

sentences = brown.sents(categories=['news'])
vector_size = 10
sample_size = vector_size

model = Word2Vec(sentences,size=vector_size, window=5, min_count=1, workers=4)

sample = [x[0] for x in model.wv.most_similar(sentences[0][1])]
target_word = sentences[20][6]

target_word = 'Chicago'

print(sample)
print('TARGET',target_word)

basis, dist, basis_to_target = pww.most_similar(model,sample,target_word)

for i,v in enumerate(basis):
	suggest = [x[0] for x in model.wv.similar_by_vector(v,topn=10)]
	print(suggest)

print('\n === \n')

for i,v in enumerate(basis_to_target):
	suggest = [x[0] for x in model.wv.similar_by_vector(v,topn=10) ]
	print(suggest)


#im = pww.plot_walk(model,basis_to_target)

pww.walk_gif(model,basis_to_target,10,0.5,'black','red',target_word,'green')

#next(im).show()
#next(im).show()
