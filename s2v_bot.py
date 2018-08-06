from song2vec.settings import TELEGRAM_API_KEY, YOUTUBE_API_KEY, TELEGRAM_START_MESSAGE
from song2vec.settings import WORD2VEC_MODEL, MSD,MODEL_SIZE, SEARCH_HISTORY
from telegram.ext import CommandHandler, Updater
from difflib import SequenceMatcher
import logging
import re
import yapi
import random
import json

def dct_test(filename):
	try:
		return json.load(open(filename,'r'))
	except:
		open(filename,'w+').close()
		return {}

def fill_author(MSD,name,size=20,initial_tolerance=0.9):
	keys = list(MSD.keys())
	lst = []
	random.shuffle(keys)
	for i,v in enumerate(keys):
		artist = MSD[keys[i]]['artist']
		for j,k in enumerate(name):
			try:
				if SequenceMatcher(None, k.lower().strip(), artist.lower().strip()).quick_ratio() >= initial_tolerance:
					lst.append(keys[i])
			except:
				pass
			if len(lst) >= size:
				break
	return lst

def start(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text=TELEGRAM_START_MESSAGE)

def rec(bot, update, args):
	try:
		history = dct_test(SEARCH_HISTORY)
		text = ' '.join(args).split(',')
		model = WORD2VEC_MODEL
		api = yapi.YoutubeAPI(YOUTUBE_API_KEY)			
		
		lst = fill_author(MSD,text)
		print(lst)
		if not lst:
			bot.send_message(chat_id=update.message.chat_id, text='Not found.')
			return
		similar_lst = model.most_similar(positive=lst, topn=20)

		query = []
		for sim in similar_lst:
			song_id = sim[0]
			title, artist = MSD[song_id]['title'], MSD[song_id]['artist']
			query.append('{0} {1}'.format(title,artist))

		urls = []
		for q in query:
			try:
				status = history.get( q, 0)
				if status:
					result = history[q]
				else:
					x = api.video_search(q,max_results=1)
					result = [ v['videoId'] for v in [ vars(z['id']) for z in [ vars(y) for y in vars(x)['items'] ] ] ][0]
				urls.append(result)
				history[q] = result
			except:
				pass
		msg = "https://youtube.com/watch_videos?video_ids={0}".format(",".join(urls))
		bot.send_message(chat_id=update.message.chat_id, text=msg)
		with open(SEARCH_HISTORY,'w') as f:
			json.dump(history,f)

	
	except Exception as e:
		msg = 'Your query was interrupted because of an error: {0}'.format(e)
		bot.send_message(chat_id=update.message.chat_id, text=msg)
	
if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
	updater = Updater(token=TELEGRAM_API_KEY)
	dispatcher = updater.dispatcher

	start_handler = CommandHandler('start',start)
	rec_handler = CommandHandler('rec',rec,pass_args=True)
	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(rec_handler)
	
	updater.start_polling()
