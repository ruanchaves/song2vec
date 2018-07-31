import numpy as np
import sympy
import random
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE

class LinAlg(object):

	def vector_projection(self,a,b):
		ab_dot_product = np.dot(a,b)
		b_magnitude = np.linalg.norm(b)
		projection = ab_dot_product / b_magnitude**2
		projection = projection * b
		return projection.real
		
	def homogenous_solve(self,M):
		eigenvalues, eigenvectors = np.linalg.eig(np.dot(M.T,M))
		return eigenvectors[:, np.argmin(eigenvalues)]
		
	def step(self,M):
		v1 = M[0] / np.linalg.norm(M[0])
		if len(M) == 1:
			v2 = np.random.rand(1,len(M[0]))[0]
			prod = np.dot(v1,v2)
			v1_null = np.array(v1)
			v2_null = np.array(v2)
			v1_null[-1] = 0.0
			v2_null[-1] = 0.0
			prod -= np.dot(v1_null,v2_null)
			v2[-1] = prod / v1[-1]
		else:
			v2 = M[1] - self.vector_projection(M[1], M[0])
		solutions = np.array([v1,v2])
		for idx,v in enumerate(M[2:]):
			sum_projection = np.repeat(0.0,len(v))
			for p_idx,p in enumerate(M):
				normal_p = p / np.linalg.norm(p)
				sum_projection += self.vector_projection(v,p)
				if p_idx + 1 == idx + 2:
					break
			diff = np.array([v - sum_projection])
			solutions = np.vstack((solutions,diff))
		new_M = self.homogenous_solve(solutions)
		new_M = np.vstack((M,new_M))
		return new_M
	
	def vec_dist(self,basis,vec):
		return np.linalg.lstsq(basis.T,vec)[0].T
	
	def boil(self,corpus):
		echelon = np.array(sympy.Matrix(corpus).rref()[0]).real.astype('float')
		idx = [i for i,v in enumerate(echelon) if sum([abs(x) for x in echelon[i]]) != 0]
		return np.array([v for i,v in enumerate(corpus) if i in idx])
		
	def corpus_to_base(self,corpus):
		M = self.boil(corpus)
		while not (lambda m: all(len(row) == len(m) for row in m))(M):
			M = self.step(M)
		return M

def most_similar_with_base(model,base,target,N=1,check=True):
	la = LinAlg()
	base_vector = model.wv[base[0]]
	for w in base[1:]:
		base_vector = np.vstack((base_vector, model.wv[w]))
	if check:
		base_vector = la.corpus_to_base(base_vector)
	first_base_vector = np.array(base_vector)
	word_vector = model.wv[target]
	dist_vector = la.vec_dist(base_vector,word_vector)

	for i,v in enumerate(dist_vector):
		base_vector[i] *= v

	return first_base_vector, base_vector

#	origin_words = [model.wv.similar_by_vector(v,topn=N) for v in first_base_vector]
#	target_words = [model.wv.similar_by_vector(v,topn=N) for v in base_vector]
#	return origin_words, target_words,base_vector

def random_word_sample(sentences,size=10):
	sample = random.sample(list(sentences), size)
	return [random.choice(v) for i,v in enumerate(sample)]

def vec2word(model,vec,N=1):
	return model.wv.similar_by_vector(vec,topn=N)[0][0]

def plot_tsne(model, word_vectors, basis, word, filename):

	wordlist = []
	print(word_vectors)
	print('\n',vec2word(model,word))
	datapoints = np.vstack(( word_vectors, np.array([model.wv[word]]) ))
	datapoints = np.vstack(( datapoints, basis ))
	for i,v in enumerate(datapoints):
		wordlist += str(vec2word(model,v))
		if i == len(word_vectors):
			break
	wordlist += word
	
	fit = TSNE(random_state=20150101).fit_transform(datapoints)
	x,y = tuple(zip(*fit))
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	plt.plot(x[0],y[0],'go')

	
	# word_vectors are red
	k = len(word_vectors)
	for i in range(k):
		plt.plot(x[i],y[i],'ro')

	# target word is blue
	plt.plot(x[k],y[k],'bo')
	
	#basis points are green
	for i in range(k,len(x)):
		plt.plot(x[i],y[i],'go')
		
	for idx,xy in enumerate(zip(x,y)):
		ax.annotate(wordlist[idx], xy=xy, textcoords='data')
		if idx == len(word_vectors) + 1:
			break
	plt.grid()
	plt.savefig(filename)
