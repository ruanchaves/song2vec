# song2vec


song2vec_bot is a Telegram bot that lives at [http://t.me/song2vec_bot](http://t.me/song2vec_bot).

 > ![](https://i.imgur.com/VJbm80p.jpg)
 
 
 Justin Bieber + Backstreet Boys + Ice Cube + Lil Jon = Justin Bieber with rappers.


Feature requests and bug reports are welcome, please open an issue.
 
# Usage

	COMMAND SYNTAX:
		Simply type /rec followed by a comma-separated list of artists.
	
	EXAMPLE:
		/rec Metallica, Nirvana, Pink Floyd, Iron Maiden, Ice Cube, Bob Marley, Rolling Stones, U2

# Installation

You can run song2vec from your own computer.
	
	sudo apt-get install virtualenv
	virtualenv song2vec_env -p `which python3.5`
	cd ./song2vec_env/bin
	source activate
	./pip3.5 install datetime gensim numpy python-telegram-bot sympy yapi
	cd ..
	git clone https://github.com/ruanchaves/song2vec.git
	cd ./song2vec/song2vec
	bash install.sh
	
After that you just have to edit **settings.py** with your Youtube and Telegram API keys. If you don't have them yet:

* [Get API Key for Youtube](https://www.slickremix.com/docs/get-api-key-for-youtube/)

* [Get API Key for Telegram](https://www.sohamkamani.com/blog/2016/09/21/making-a-telegram-bot/) - Simply follow the "Set up your bot" section until you get the API Key ( you won't have to manually set up a bot server ).

Then you can turn on the bot with:

	python3.5 s2v_bot.py
	
# Details

Currently the bot takes recommendations from a gensim word2vec model and that's all there's to it.

It's been trained on [The Echo Nest Taste Profile Subset](https://labrosa.ee.columbia.edu/millionsong/tasteprofile) taken from the Million Song Database. The Song IDs were matched to author and title according to [this file](https://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_tracks.txt).

Some tricks I learned along the way:

* This is not NLP, so we shouldn't use gensim's default parameters. Otherwise [recommendations will get twice as bad](https://arxiv.org/pdf/1804.04212.pdf).

* Calling `model.wv[word]` for every word is painfully slow. It's much faster to do...

		model_words = list(model.wv.index2word
		model_vectors = list(model.wv.syn0)
		model_dct = dict(zip(model_words,model_vectors))
	
...and call model_dct[word]. It's there [on the source code](https://github.com/RaRe-Technologies/gensim/blob/3b9bb59dac0d55a1cd6ca8f984cead38b9cb0860/gensim/models/word2vec.py#L441).

# Donate

**BTC address:** 32tQxrFSkA8kkyEgq7PSh8AANghn3tfmX9
