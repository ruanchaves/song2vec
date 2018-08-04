from wordcloud import (WordCloud, get_single_color_func)
from PIL import Image
from linalg import *
from moviepy.editor import ImageSequenceClip
import matplotlib.pyplot as plt
import multidict
import io
import numpy as np

class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)

def color_map(word_map,old_color='black',new_color='red', target_word='target_word', target_color='green'):
	words = []
	for i,v in enumerate(word_map):
		for j,w in enumerate(v):
			words.append(w[0])
	words = list(set(words))
	try:
		words.remove(target_word)
	except:
		pass
	return ({ old_color : words, target_color : [target_word] }, new_color)
	

def plot_words(model,word_map,basis,colors=None,old_color='black',new_color='red',target_word='target_word',target_color='green'):
	tmp_dict = {}
	full_dict = multidict.MultiDict()

	for artist in word_map.keys():
		tmp_dict[artist] = len(word_map[artist])
	
	for key in tmp_dict:
		full_dict.add(key, tmp_dict[key])

	wc = WordCloud(background_color="white", max_words=100)
	wc.generate_from_frequencies(full_dict)

	print('ok')
	
	if colors:
		cm = color_map(colors,old_color,new_color,target_word,target_color)
	else:
		cm = color_map([],old_color,new_color,target_word,target_color)
		
	grouped_color_func = SimpleGroupedColorFunc(cm[0],cm[1])

	wc.recolor(color_func=grouped_color_func)

	plt.imshow(wc, interpolation="bilinear")
	plt.axis("off")
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)
	im = Image.open(buf)
	plt.clf()
	return im, word_map

def plot_walk(model,basis,old_color='black',new_color='red',target_word='target_word',target_color='green'):
	w = walk(basis)
	im, word_map = plot_words(model,next(w))
	yield im
	while 1:
		try:
			im, word_map = plot_words(model, next(w),word_map,old_color,new_color,target_word,target_color)
			yield im
		except StopIteration:
			break

def walk_gif(model,basis,length=10,fps=0.25,old_color='black',new_color='red',target_word='target_word',target_color='green'):
	im = plot_walk(model,basis,old_color,new_color,target_word,target_color)
	images = [np.array(next(im))]
	i = 1
	while 1:
		try:
			current_im = next(im)
			i += 1
			if i == length:
				break
			images.append(np.array(current_im))
		except StopIteration:
			break

	clip = ImageSequenceClip(images,fps=fps)
	clip.write_gif('test.gif')

if __name__ == '__main__':
	
