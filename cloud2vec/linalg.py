import numpy as np
import sympy
import random
import itertools
from functools import reduce

def vector_projection(a,b):
	"""
	Projects vector a onto vector b.
	:type a: numpy.ndarray
	:type b: numpy.ndarray
	:rtype: numpy.ndarray
	"""
	ab_dot_product = np.dot(a,b)
	b_magnitude = np.linalg.norm(b)
	projection = ab_dot_product / b_magnitude**2
	projection = projection * b
	return projection.real
		
def homogenous_solve(M):
	eigenvalues, eigenvectors = np.linalg.eig(np.dot(M.T,M))
	return eigenvectors[:, np.argmin(eigenvalues)]
		
def step(M):
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
		v2 = M[1] - vector_projection(M[1], M[0])
	solutions = np.array([v1,v2])
	for idx,v in enumerate(M[2:]):
		sum_projection = np.repeat(0.0,len(v))
		for p_idx,p in enumerate(M):
			normal_p = p / np.linalg.norm(p)
			sum_projection += vector_projection(v,p)
			if p_idx + 1 == idx + 2:
				break
		diff = np.array([v - sum_projection])
		solutions = np.vstack((solutions,diff))
	new_M = homogenous_solve(solutions)
	new_M = np.vstack((M,new_M))
	return new_M
	
def vec_dist(basis,vec):
	return np.linalg.lstsq(basis.T,vec)[0].T
	
def boil(corpus):
	echelon = np.array(sympy.Matrix(corpus).rref()[0]).real.astype('float')
	idx = [i for i,v in enumerate(echelon) if sum([abs(x) for x in echelon[i]]) != 0]
	return np.array([v for i,v in enumerate(corpus) if i in idx])
		
def corpus_to_base(corpus):
	M = boil(corpus)
	i = 0
	while not (lambda m: all(len(row) == len(m) for row in m))(M):
		M = step(M)
		i += 1
	return M, i

def base2vec(model,vec,check=True):
	end_base = model.wv[vec[0]]
	for w in vec[1:]:
		end_base = np.vstack((end_base, model.wv[w]))
	if check:
		return corpus_to_base(end_base)
	else:
		return end_base, None
	
def most_similar(model,base,target,N=1,threshold=False):
	base_vector, step = base2vec(model,base)
	if threshold:
		assert (step < threshold),"{0} steps to basis in base2vec >= {1} steps allowed".format(step,threshold)
	first_base_vector = np.array(base_vector)
	word_vector = model.wv[target]
	dist_vector = vec_dist(base_vector,word_vector)

	for i,v in enumerate(dist_vector):
		base_vector[i] *= v

	return first_base_vector, dist_vector, base_vector

def walk(base_vector):
	for i,v in enumerate(list(itertools.permutations(base_vector,len(base_vector)))):
		word_walk = []
		for j,w in enumerate(v):
			word_sum = reduce((lambda x,y: x+y), v[:j+1])
			word_walk.append(word_sum)
			yield word_walk
