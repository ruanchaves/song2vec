from telegram.ext import CommandHandler, Updater
from settings import WORD2VEC_MODEL, MSD
from settings import TELEGRAM_API_KEY, TELEGRAM_START_MESSAGE, TELEGRAM_HELP_MESSAGE
import logging
from query import fill_author, playlist_from_query, get_more
import re

def start(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text=TELEGRAM_START_MESSAGE)

def h(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text=TELEGRAM_HELP_MESSAGE)

def rec(bot, update, args):
	try:

		text = ' '.join(args).split(',')
		target = [text[0]]
		home = text[1:128]
		a = fill_author(MSD,home)
		b = fill_author(MSD,target, 1)[0]
	
		playlist = playlist_from_query(MSD,a,b)
		basis = next(playlist)
		msg = next(playlist)
		bot.send_message(chat_id=update.message.chat_id, text=msg)
	
		new_links = get_more(WORD2VEC_MODEL,MSD,basis)
		links_lst = []
		for i,v in enumerate(new_links):
			try:
				msg = v.split('=')[1]
				links_lst.append(msg)
			except:
				pass
			if len(links_lst) >= 20:
				break
		links_lst = list(set(links_lst))
		dct = {}
		for w in links_lst:
			dct[w] = 0
		for w in links_lst:
			dct[w] += 1
		links_lst = [ x[0] for x in sorted(list(dct.items()), key=lambda tup: tup[1]) ][::-1]
		msg = "https://youtube.com/watch_videos?video_ids={0}".format(",".join(links_lst))
		bot.send_message(chat_id=update.message.chat_id, text=msg)

	
	except Exception as e:
		msg = 'Your query was interrupted because of an error: {0}'.format(e)
		bot.send_message(chat_id=update.message.chat_id, text=msg)
	
if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
	updater = Updater(token=TELEGRAM_API_KEY)
	dispatcher = updater.dispatcher

	start_handler = CommandHandler('start',start)
	h_handler = CommandHandler('h',h)
	rec_handler = CommandHandler('rec',rec,pass_args=True)
	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(h_handler)
	dispatcher.add_handler(rec_handler)
	
	updater.start_polling()
