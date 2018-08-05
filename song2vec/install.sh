wget http://labrosa.ee.columbia.edu/millionsong/sites/default/files/challenge/train_triplets.txt.zip
unzip train_triplets.txt.zip
wget https://labrosa.ee.columbia.edu/millionsong/sites/default/files/AdditionalFiles/unique_tracks.txt
python3.5 MSDtools.py
python3.5 train.py
