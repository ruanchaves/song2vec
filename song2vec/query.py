from time import sleep
import yapi

def get_url(MSD,api_key, history, similar_lst):
	api = yapi.YoutubeAPI(api_key)
	query = []
	for sim in similar_lst:
		song_id = sim[0]
		title, artist = MSD[song_id]['title'], MSD[song_id]['artist']
		query.append('{0} {1}'.format(title,artist))

	urls = []
	for q in query:
		status = history.get( q, 0)
		if status:
			result = history[q]
		else:
			while 1:
				i = 0
				try:
					x = api.video_search(q,max_results=1)
					break
				except Exception as e:
					print('Error : {0} . Sleeping for {1} seconds'.format(e,2**i))
					i += 1
					sleep(2**i)
			result = [ v['videoId'] for v in [ vars(z['id']) for z in [ vars(y) for y in vars(x)['items'] ] ] ][0]
		urls.append(result)
		history[q] = result
	return history, urls
