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
target_word = sentences[20][4]

print(sample)
print(target_word)

basis, basis_to_target = pww.most_similar_with_base(model,sample,target_word)
word_vectors = model.wv.vectors

pww.plot_tsne(model,word_vectors,basis,target_word,'pww.png')

pww.plot_tsne(model,word_vectors,basis_to_target,target_word,'pww2.png')

sys.exit(0)


