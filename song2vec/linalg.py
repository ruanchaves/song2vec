from functools import reduce
import itertools
import numpy as np
import random
import sympy

def vector_projection(a,b):
	"""
	Projects vector a onto vector b.
	
	Parameters
	----------
	a : numpy.ndarray
	
	b : numpy.ndarray

	Returns
	-------
	numpy.ndarray

	"""

	ab_dot_product = np.dot(a,b)
	b_magnitude = np.linalg.norm(b)
	projection = ab_dot_product / b_magnitude**2
	projection = projection * b
	return projection.real
		
def homogenous_solve(M):
	"""
	Solve homogeneous linear system by finding the eigenvector associated with the smallest eigenvalue.


	Parameters
	----------
	
	M: (M,M) numpy.ndarray

	Returns
	-------
	numpy.ndarray
	
	"""
	eigenvalues, eigenvectors = np.linalg.eig(np.dot(M.T,M))
	return eigenvectors[:, np.argmin(eigenvalues)]
		
def step(M):
	"""
	Add a new linearly independent row to matrix M.
	
	This is done by finding the normalized basis of given real, (n-1)-dimensional linear subspace and then 
	complementing it to a full basis of n by solving a homogeneous linear system. 

	Parameters
	----------
	
	M: (M,M-1) numpy.ndarray


	Returns
	-------
	numpy.ndarray

	"""
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
	"""
	Find the least-squares solution of basis*x = vec and transpose it.

	Parameters
	----------

	basis: numpy.ndarray
	
	vec: numpy.ndarray
	
	Returns
	-------
	numpy.ndarray
	
	"""

	return np.linalg.lstsq(basis.T,vec)[0].T
	
def boil(corpus):
	"""
	Eliminate lines in 'corpus' matrix that are not linearly independent.


	Parameters
	----------

	corpus: numpy.ndarray
	
	Returns
	-------
	numpy.ndarray
	
	"""

	echelon = np.array(sympy.Matrix(corpus).rref()[0]).real.astype('float')
	idx = [i for i,v in enumerate(echelon) if sum([abs(x) for x in echelon[i]]) != 0]
	return np.array([v for i,v in enumerate(corpus) if i in idx])
		
def corpus_to_base(corpus):
	"""
	Given a 'corpus' matrix, find a basis and how many lines are not linearly independent.
	

	Parameters
	----------
	
	corpus: numpy.ndarray
	

	Returns
	-------
	(numpy.ndarray, int)

	"""

	M = boil(corpus)
	i = 0
	while not (lambda m: all(len(row) == len(m) for row in m))(M):
		M = step(M)
		i += 1
	return M, i

	
def most_similar(base,target,threshold=False):
	"""
	Given a 'target' word, try to replace each word in the word list 'base' by a similar word
	that is in the same context as 'target'.
	
	Vectors in 'base' that are not linearly independent will be automatically replaced.
	
	Parameters
	----------
	
	base: np.array
		Word list represented as a matrix of word embeddings.

	target: nd.array
		Target word represented as a vector.
	
	threshold: int, bool
		Raise an error if the number of linearly dependent lines in 'base' after conversion is more than or equal to threshold.
		Therefore threshold means the maximum amount of words in 'base' that will be allowed to be replaced by random words.
		If threshold is False, this function won't check for linearly dependent lines.
		
	
	Returns
	-------
	(numpy.ndarray, numpy.ndarray, numpy.ndarray)

	The first array is the result of converting the word list into a matrix of word embeddings.

	The third array is a matrix of word embeddings that stand for the target word list.
	
	The dot product of the first and the second array will be the third array.
	
	"""

	base_vector, step = corpus_to_base(base)
	if threshold:
		assert (step < threshold),"{0} steps to basis in base2vec >= {1} steps allowed".format(step,threshold)
	first_base_vector = np.array(base_vector)
	dist_vector = vec_dist(base_vector,target)

	for i,v in enumerate(dist_vector):
		base_vector[i] *= v

	return first_base_vector, dist_vector, base_vector

def walk(base_vector,n=2):
	"""
	Yield all possible subseries for all possible row permutations of base_vector.
	

	Parameters
	----------

	base_vector: numpy.ndarray 


	Yields
	------
	numpy.ndarray

	"""
	generator = itertools.permutations(base_vector, len(base_vector))
	for g in generator:
		word_sum = reduce((lambda x,y: x+y), g[0:n])
		yield word_sum
