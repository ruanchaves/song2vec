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
		if target == '!fast':
			api_status = False
			target = [text[1]]
			home = text[2:129]
		else:
			api_status = True
		a = fill_author(MSD,home)
		b = fill_author(MSD,target, 1)[0]
	
	
		playlist = playlist_from_query(MSD,a,b)
		basis = next(playlist)
		msg = next(playlist)
	
		parse = re.sub('watch_videos?video_ids=','watch?v=',msg)
		parse = parse.split(",")
		bot.send_message(chat_id=update.message.chat_id, text=parse[0])
		for p in parse[1:]:
			s = "https://youtube.com/watch?v={0}".format(p)
			bot.send_message(chat_id=update.message.chat_id, text=s)
		msg = "PLAYLIST \n \n === \n \n A full playlist of the previous twenty videos follows below. \n \n  {0}".format(msg)
		bot.send_message(chat_id=update.message.chat_id, text=msg)
	
		new_links = get_more(WORD2VEC_MODEL,MSD,basis)
		for i,v in enumerate(new_links):
			bot.send_message(chat_id=update.message.chat_id, text=v)
			if i > 4:
				break
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
