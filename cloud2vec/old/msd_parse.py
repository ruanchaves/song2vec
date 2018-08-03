import os
from settings import MSD_FOLDER, MSD_CORPUS_FILENAME
import json

initial_dir_path = os.getcwd()

def parser(fname, dct):
	return '{0}\t{1}\t{2}\n'.format(fname[:-5], dct['response']['songs'][0]['title'],dct['response']['songs'][0]['artist_name'])

file_buffer = ''
os.chdir(MSD_FOLDER)
for dirpath, dirs, files in os.walk('.'):
	for filename in files:
		if '.json' in filename:
			fname = os.path.join(dirpath,filename)
			song_id = filename.rstrip('.json')
		else:
			continue
		with open(fname,'r') as myfile:
			content = myfile.read()
		dct = json.loads(content)
		try:
			current_string = parser(song_id,dct)
			file_buffer += current_string
		except:
			continue

os.chdir(initial_dir_path)
open(MSD_CORPUS_FILENAME,'w+').close()
with open(MSD_CORPUS_FILENAME,'w') as f:
	print(file_buffer,file=f)
