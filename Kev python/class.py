import nltk
import urllib.request
import re
from inscriptis import get_text
from nltk import word_tokenize, sent_tokenize
from googletrans import Translator

#nltk.download()

#articulo de wikipedia
enlace = "https://en.wikipedia.org/wiki/2022_Russian_invasion_of_Ukraine"
html = urllib.request.urlopen(enlace).read().decode('utf-8')
text = get_text(html)
article_text = text.replace("[ edit ]", "")
print("#############################################")


from nltk import word_tokenize, sent_tokenize
#Removing Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)


#nltk.download()
#En esta parte hace la tokenizacion
sentence_list = nltk.sent_tokenize(article_text)


#En esta parte encuentra la frecuencia de las palabras
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1


#Calcula las frases que mas se repiten
sentences_socores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentences_socores.keys():
                    sentences_socores[sent] = word_frequencies[word]
                else:
                    sentences_socores[sent] += word_frequencies[word]


maximum_frequncy = max(word_frequencies.values())


for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)


#Realiza el resumen con las mejores frases
import heapq
summary_sentences = heapq.nlargest(7, sentences_socores, key=sentences_socores.get)

summary = ' '.join(summary_sentences)

Traductor = Translator()
traducido = Traductor.translate(summary, dest='spanish' )
print(traducido.text)

from nltk.corpus import treebank
t = treebank.parsed_sents('wsj_0001.mrg')[0]
t.draw()

