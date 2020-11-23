import lyricsgenius
import re
from collections import Counter
import spacy
from spacy.gold import docs_to_json
from spacy.vocab import Vocab

nlp = spacy.load("en_core_web_sm")
vocab = Vocab(strings=["hello", "world"])
special_cases = [{"ORTH": "Takyon", "NORM": "takyon", "LEMMA": "takyon"}]
nlp.tokenizer.add_special_case("Tak-kyon", special_cases)
nlp.tokenizer.add_special_case("Takyon", special_cases)

### remove stop words
# nlp.Defaults.stop_words.remove('bread')
# nlp.vocab['bread'].is_stop = False
### add stop words
# nlp.Defaults.stop_words.add('bread')
# nlp.vocab['bread'].is_stop = True

# stop_words = (lex for lex in nlp.vocab if lex.is_stop)
# print(stop_words.strings())

# STOP_WORDS = set("""
# a about above across after afterwards again against all almost alone along
# already also although always am among amongst amount an and another any anyhow
# anyone anything anyway anywhere are around as at

# back be became because become becomes becoming been before beforehand behind
# being below beside besides between beyond both bottom but by
# """.split())

tfile = open('textgrips/token.txt', 'r')  # genius API token is stored in token.txt
gtoken = tfile.read()

genius = lyricsgenius.Genius(gtoken)


def save_lyrics():
    '''a function to save lyrics localy
    '''
    path = 'textgrips/lyrics-txt/'
    album = genius.search_album("Exmilitary", "Death Grips")
    for song in album.songs:
        print(song.title+' is being processed')
        song_file = open(path+song.title+'.txt', 'w')
        song_file.write(song.lyrics)
        song_file.close()
    print("lyrics are saved as txts under "+path)


def read_loc(title):
    '''read lyrics from local files, remove
    everything inbetween [], i.e. words like
    verse, chorus...
    '''
    path = 'textgrips/lyrics-txt/'
    song_file = open(path+title+'.txt', 'r')
    raw_lyrics = song_file.read()
    lyrs = re.sub("[\[].*?[\]]", "", raw_lyrics)

    return lyrs


def lyrics_content(title):
    '''perform varuious operations on the lyrics
    and return corresponding metrics
    '''
    lyrs = read_loc(title)
    # lyrs = re.sub('\n', ' ', lyrs)
    doc = nlp(lyrs)
    print(lyrs)
    # doc = nlp("five o'clock")
    # json_data = docs_to_json([doc])
    # for token in doc:
    #     print(token.is_punct)
    nouns = [token.lemma_ for token in doc if token.pos_ == 'NOUN' and token.is_stop != True]
    verbs = [token.lemma_ for token in doc if token.pos_ == 'VERB' and token.is_stop != True]
    adjs = [token.lemma_ for token in doc if token.pos_ == 'ADJ' and token.is_stop != True]
    adverbs = [token.lemma_ for token in doc if token.pos_ == 'ADV' and token.is_stop != True]
    words = [token.lemma_.lower() for token in doc if token.is_punct != True and token.is_stop != True]
    word_freq = Counter(words)
    print(word_freq)

    # word_freq = Counter(nouns)
    # print(word_freq)
    # word_freq = Counter(verbs)
    # print(word_freq)
    # word_freq = Counter(adjs)
    # print(word_freq)
    # word_freq = Counter(adverbs)
    # print(word_freq)

    # print(json_data)

    return lyrs


