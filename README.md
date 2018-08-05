# song2vec


song2vec_bot is a Telegram bot that lives at [http://t.me/song2vec_bot](http://t.me/song2vec_bot).

 ![](https://i.imgur.com/VJbm80p.jpg)
 
 Justin Bieber + Backstreet Boys + Ice Cube + Lil Jon = Justin Bieber with rappers.
 
 Table of Contents
=================
   * [Usage]()
   * [Installation]()
   * [Donate]()

 
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
	
# Donate

**BTC address:** 32tQxrFSkA8kkyEgq7PSh8AANghn3tfmX9
