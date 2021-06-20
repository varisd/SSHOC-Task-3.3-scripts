# TODO: method argument signatures
import re
import xml.etree.ElementTree as ET

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def xml2charlist(filename):
    """Extract the list of characters from the input TEI file."""

    root = ET.parse(filename).getroot()
    res = set()

    ns = re.match(r'{.*}', root.tag).group(0)
    for e in root.iter('{}person'.format(ns)):
        namespace = "{http://www.w3.org/XML/1998/namespace}"

        val = e.attrib["{}id".format(namespace)]
        res.add(val)

    return res


def xml2docs(filename):
    """Process the input TEI file.

    In this context, a ``document'' is a set of sentences spoken
    by a single character.
    """
    root = ET.parse(filename).getroot()
    res = {}

    ns = re.match(r'{.*}', root.tag).group(0)
    for e in root.iter('{}sp'.format(ns)):
        if 'who' in e.attrib:
            who_all = e.attrib['who'].split(" ")
        else:
            continue
        for who in who_all:
            if who not in res:
                res[who] = []

        lines = []
        for e_ch in e.iter('{}l'.format(ns)):
            line = " ".join([
                "".join(w.itertext()) for w in e_ch.iter('{}w'.format(ns))
            ])
            if not line:
                line = e_ch.text
            lines.append(line)
        if not lines:
            lines = [
                " ".join([
                    "".join(w.itertext()) for w in p.iter('{}w'.format(ns))
                ]) for p in e.iter('{}p'.format(ns))
            ]
        for who in who_all:
            res[who] += lines
    return res


def extract_tfidf_vectors(docs, ngram_range=[1, 1], language="english"):
    assert len(ngram_range) == 2
    
    # A document is a list of sentences...
    for k, v in docs.items():
        docs[k] = " ".join(v)

    ps = PorterStemmer()
    keys = docs.keys()

    tfidf_vectors = TfidfVectorizer(
        tokenizer=word_tokenize,
        preprocessor=ps.stem,
        lowercase=True,
        stop_words=set(stopwords.words(language)),
        ngram_range=ngram_range,
        ).fit_transform(docs.values()).todense()

    return {k: v for k, v in zip(keys, tfidf_vectors)}


def extract_count_vectors(docs, ngrams=1, language="english"):
    assert ngrams > 0
    
    # A document is a list of sentences...
    for k, v in docs.items():
        docs[k] = " ".join(v)

    ps = PorterStemmer()
    keys = docs.keys()

    vectorizer = CountVectorizer(
        tokenizer=word_tokenize,
        preprocessor=ps.stem,
        lowercase=True,
        stop_words=set(stopwords.words(language)),
        ngram_range=[ngrams, ngrams],
    ).fit(docs.values())

    tokens = vectorizer.get_feature_names()

    return {
        key : {
            k : v for k, v in zip(tokens, vectorizer.transform([docs[key]]).toarray()[0])
        } for key in docs
    }
