'''
    calculates TI*IDF for given words.
'''

import pandas as pd
import random as rd

sustituir_offer = {
    'dispon'   : 'disponibilidad',
    'dona'     : 'donar',
    'dono'     : 'donar',
    'ofre'     : 'ofrecer',
    'vend'     : 'vender',
    'vent'     : 'vender',
    'cambio'   : 'cambiar',
    'cambia'   : 'cambiar',
    'farmacia' : 'farmacia',
    'droguer'  : 'farmacia',
    'botiquer' : 'farmacia',
    'tengo'    : 'tener',
    'tenemos'  : 'tener',
    'conseg'   : 'conseguir',
    'consig'   : 'conseguir',
    'confirm'  : 'confirmar',
    'necesit'  : 'necesitar'
}


sustituir_demand = {
    'urge'      : 'urgente',
    'favor'     : 'favor',
    'xfa'       : 'favor',
    'gracias'   : 'gracias',
    'requie'    : 'requerir',
    'requerimos': 'requerir',
    'necesit'   : 'necesitar',
    'emergencia': 'emergencia',
    'solicit'   : 'solicitar',
    'agrade'    : 'agradecer',
    'consig'    : 'conseguir',
    'conseg'    : 'conseguir',
    'donde'     : 'donde',
    'dónde'     : 'donde',
    'busca'     : 'buscar',
    'busq'      : 'buscar',
    'busco'     : 'buscar',
    'ubica'     : 'buscar',
    'encontrar' : 'buscar',
    'ayuda'     : 'ayudar',
    'adquirir'  : 'adquirir',
    'informa'   : 'informar',
    'referencia': 'informar',
    'compra'    : 'comprar',
    'compro'    : 'comprar',
    'trata'     : 'tratamiento',
    'tiene'     : 'tener',
    'tener'     : 'tener'
}

offer_words = [
    'disponibilidad',
    'donar',
    'ofrecer',
    'vender',
    'cambiar',
    'farmacia',
    'tener',
    'conseguir',
    'confirmar',
    'necesitar'
]

demand_words = [
    'urgente',
    'favor',
    'gracias',
    'requerir',
    'necesitar',
    'emergencia',
    'solicitar',
    'agradecer',
    'conseguir',
    'donde',
    'buscar',
    'ayudar',
    'adquirir',
    'informar',
    'comprar',
    'tratamiento',
    'tener'
]

def readData(file):
    '''
        Reads data inside a .txt file containing the vectors of training/testing data.
        returns the attributes normalized.
    '''
    dataset = pd.read_csv(file, delimiter = "," , encoding='mac_roman', index_col = False)
    return dataset

#This stores already human classified data.
demand_data = pd.DataFrame()
offer_data  = pd.DataFrame()
other_data  = pd.DataFrame()


def tfidf_offer(filename):
    '''
        Applies first filter to saparte usefull data from random tweets in a
        first instance
    '''

    from palabras_comunes import stopwords

    #Set up new dataframes
    #This stores the dataframe for a first filtered data.
    needed_data = pd.DataFrame()

    word_count     = 0
    term_frecuency = {}
    word_in_tweet  = {}
    idf     = {}
    tfidf   = {}
    count   = {}

    for word in offer_words :
        term_frecuency[word] = 0
        word_in_tweet[word]  = 0
        count[word] = 0
        tfidf[word] = 0
        idf[word] = 0

    data = readData(filename)

    for i in range(len(data)):
        row = data.iloc[i]
        text = row['text'].lower()
        text = text.split(' ')

        # Sustituimos las palabras
        for i in range(len(text)):
            if '@' in text[i]:
                continue
            else:
                for word in sustituir_offer:
                    if word in text[i]:
                        text[i] = sustituir_offer[word]

        for word in text:
            if (word in stopwords) or ('@' in word):
                continue
            else:
                word_count += 1
                for offer_word in offer_words:
                    if offer_word in word:
                        count[offer_word] += 1

        #rejoin the words to count appearences in tweets
        new_text = []
        for word in text:
            if (word in stopwords) or ('@' in word):
                continue
            else:
                new_text.append(word)

        new_text = ''.join(new_text)
        for offer_word in offer_words:
            if offer_word in new_text:
                word_in_tweet[offer_word] += 1


    #calculating term frequency:
    for word in offer_words:
        term_frecuency[word] = count[word]/word_count
        if word_in_tweet[word] != 0:
            idf[word]   =  len(data)/word_in_tweet[word]
        tfidf[word] =  term_frecuency[word]*idf[word]

    print("FOR OFFER WORDS: ")
    print("Total Words: %d"%word_count)
    print("Count: ")
    print(count)
    print("Appearences of word in tweets: ")
    print(word_in_tweet)
    print("TF: ")
    print(term_frecuency)
    print("IDF: ")
    print(idf)
    print("TF*IDF: ")
    print(tfidf)

def tfidf_demand(filename):
    '''
        Applies first filter to saparte usefull data from random tweets in a
        first instance
    '''

    from palabras_comunes import stopwords

    #Set up new dataframes
    #This stores the dataframe for a first filtered data.
    needed_data = pd.DataFrame()

    word_count     = 0
    term_frecuency = {}
    word_in_tweet  = {}
    idf     = {}
    tfidf   = {}
    count   = {}

    for word in demand_words :
        term_frecuency[word] = 0
        word_in_tweet[word]  = 0
        count[word] = 0
        tfidf[word] = 0
        idf[word] = 0

    data = readData(filename)

    for i in range(len(data)):
        row = data.iloc[i]
        text = row['text'].lower()
        text = text.split(' ')

        # Sustituimos las palabras
        for i in range(len(text)):
            if '@' in text[i]:
                continue
            else:
                for word in sustituir_demand:
                    if word in text[i]:
                        text[i] = sustituir_demand[word]

        for word in text:
            if (word in stopwords) or ('@' in word):
                continue
            else:
                word_count += 1
                for demand_word in demand_words:
                    if demand_word in word:
                        count[demand_word] += 1

        #rejoin the words to count appearences in tweets
        new_text = []
        for word in text:
            if (word in stopwords) or ('@' in word):
                continue
            else:
                new_text.append(word)

        new_text = ''.join(new_text)
        for demand_word in demand_words:
            if demand_word in new_text:
                word_in_tweet[demand_word] += 1


    #calculating term frequency:
    for word in demand_words:
        term_frecuency[word] = count[word]/word_count
        if word_in_tweet[word] != 0:
            idf[word]   =  len(data)/word_in_tweet[word]
        tfidf[word] =  term_frecuency[word]*idf[word]

    print("\nFOR DEMAND WORDS: ")
    print("Total Words: %d"%word_count)
    print("Count: ")
    print(count)
    print("Appearences of word in tweets: ")
    print(word_in_tweet)
    print("TF: ")
    print(term_frecuency)
    print("IDF: ")
    print(idf)
    print("TF*IDF: ")
    print(tfidf)

#Running
tfidf_offer('CollectedData/offer_data_2000.csv')
tfidf_demand('CollectedData/demand_data_2000.csv')
