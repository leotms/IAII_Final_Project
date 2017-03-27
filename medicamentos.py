'''
    File:        medicamentos.py
    Description: Connects to twitter API to retreive tweets and classify them.
    Authors:     Leonardo Martinez #11-10576
                 Nicolas Manan     #06-39883
                 Joel Rivas        #11-10866
    Updated:     03/05/2017
'''
import tweepy as tp
import sys
sys.path.append('./resources' )
from neuralnetwork    import *
from palabras_comunes import palabras_positivas, palabras_negativas

known_medicines = [
    'clexane',
    'fenobarbital',
    'valpron',
    'carboplatino',
    'epamin',
    'losartan',
    'doxorrubicina',
    'concor',
    'albumina',
    'valcote',
    'benicar',
    'pregabalina',
    'prednisona',
    'sinemet',
    'metronidazol',
    'xarelto',
    'avastin',
    'cisplatino',
    'valsartan',
    'leucovorina',
    'clindamicina',
    'keppra',
    'plaquinol',
    'unasyn',
    'madopar',
    'amlodipina',
    'tramal',
    'neupogen',
    'hidroclorotiazida',
    'aprovel',
    'sertralina',
    'stalevo',
    'moderan',
    'granocyte',
    'euthyrox',
    'plavix',
    'aciclovir',
    'glaucotensil',
    'pradaxa',
    'oxicodal',
    'femara',
    'dostinex',
    'insulina',
    'badan',
    'omeprazol',
    'atorvastatina',
    'diclofenac',
    'furosemida',
    'metfor',
    'metformina',
    'meropenem',
    'glucofage',
    'captopril',
    'dexametasona',
    'azitromicina',
    'amikacina',
    'inmunoglobulina',
    'aluron',
    'methotrexato',
    'ciprofloxacina',
    'ampicilina',
    'budecort',
    'ceftriaxona',
    'pegyt',
    'ridal',
    'atenolol',
    'neurixa',
    'ulcon',
    'aldactazida',
    'clonazepam',
    'bicalutamida',
    'pentoxifilina',
    'humalox',
    'novolin',
    'solumedrol',
    'trozolet',
    'bacipro',
    'carvedilol',
    'fulgram',
    'erbitux',
    'tegretol',
    'somazina',
    'trileptal',
    'carbamazepina',
    'enalapril',
    'levofloxacina',
    'alprazolam',
    'herceptin',
    'digoxina',
    'valproico'
]

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

offer_words_list = [
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

demand_words_list = [
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

#tfidf for offer tweets
tfidf_offer = {
    'tener': 0.0859352255954428,
    'disponibilidad': 0.08553598902477605,
    'conseguir': 0.08484282865990753,
    'cambiar': 0.08484282865990751,
    'necesitar': 0.08484282865990753,
    'donar': 0.089120618340239,
    'farmacia': 0.08888296335799836,
    'vender': 0.09191306438156648,
    'confirmar': 0.08484282865990753,
    'ofrecer': 0.08484282865990753
}

#tfidf for demand words
tfidf_demand = {
    'tener': 0.07786342754808066,
    'tratamiento': 0.07786342754808066,
    'emergencia': 0.07786342754808066,
    'gracias': 0.07786342754808066,
    'necesitar': 0.07898744028171438,
    'solicitar': 0.07830583338642202,
    'ayudar': 0.07853466399246069,
    'comprar': 0.07786342754808066,
    'conseguir': 0.07786342754808068,
    'buscar': 0.10029865243481578,
    'adquirir': 0.07786342754808066,
    'requerir': 0.07823597983299971,
    'favor': 0.07999667213843903,
    'informar': 0.07865795231897946,
    'urgente': 0.08040937068316777,
    'agradecer': 0.07786342754808066,
    'donde': 0.07823244853172086
}

def extract_minmax(trainset):

    mins = {}
    maxs = {}

    dataset = pd.read_csv(trainset, delimiter = ",", index_col = False, usecols=['lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words', 'tfidf_demand', 'tfidf_offer',  'neg_words', 'pos_words',  'n_known_medicines'])

    n_columns = dataset.shape[1]
    for i in range(0, n_columns):
        m = np.min(dataset[dataset.columns[i]])
        M = np.max(dataset[dataset.columns[i]])
        mins[dataset.columns[i]] = m
        maxs[dataset.columns[i]] = M

    return mins, maxs

def extract_features(text):

    features = {
        'lenght' : 0,
        'retweet_count' : 0,
        'hashtags' : 0,
        'mentions' : 0,
        'contains_url' : 0,
        'demand_words' : 0,
        'offer_words' : 0,
        'tfidf_demand' : 0,
        'tfidf_offer' : 0,
        'neg_words' : 0,
        'pos_words' : 0,
        'n_known_medicines' : 0,
    }

    text = text.lower()

    features['lenght'] = len(text)

    hashtags = 0
    mentions = 0
    contains_url = 0

    demand_words = 0
    offer_words  = 0
    tfidf_demand_count = 0
    tfidf_offer_count = 0

    neg_words = 0
    pos_words = 0

    n_known_medicines = 0

    text = text.split(' ')
    # Sustituimos las palabras
    for j in range(len(text)):
        if '@' in text[j]:
            continue
        else:
            for word in sustituir_offer:
                if word in text[j]:
                    text[j] = sustituir_offer[word]
            for word in sustituir_demand:
                if word in text[j]:
                    text[j] = sustituir_demand[word]

    for word in text:
        #remove commas, spaces and points
        if "http" in word:
            contains_url = 1
            continue
        if "@" in word:
            mentions += 1
            continue
        if "#" in word:
            hashtags += 1

        for j in demand_words_list:
            if j in word:
                demand_words += 1
                tfidf_demand_count += tfidf_demand[j]
        for j in offer_words_list:
            if j in word:
                offer_words  += 1
                tfidf_offer_count += tfidf_offer[j]
        for j in palabras_positivas:
            if j in word:
                pos_words += 1
        for j in palabras_negativas:
            if j in word:
                neg_words += 1
        for j in known_medicines:
            if j in word:
                n_known_medicines  += 1

    features['hashtags'] = hashtags
    features['mentions'] = mentions
    features['contains_url'] = contains_url
    features['demand_words'] = demand_words
    features['offer_words'] = offer_words
    features['tfidf_demand'] = tfidf_demand_count
    features['tfidf_offer'] = tfidf_offer_count
    features['neg_words'] = neg_words
    features['pos_words'] = pos_words
    features['n_known_medicines'] = n_known_medicines

    return features

# Authenticating for twitter app

# For streaming python
class MyStreamListener(tp.StreamListener):

    def on_status(self, status):
        send_to_neuronal(status)

    def on_error(self, status_code):
        print(status_code)
        return True

def tweetpy_auth():

    # Keys
    consumer_key = 'ayOjM353RdIr9OL85CzTa4ymr'
    consumer_secret = 'NSgQLchCDvVXmsMHRxaehEHjc3SaWSMYZ1vCN3qqbwHE9VFgqv'
    access_token = '77759767-e9K9RtJMHRzmxLIpzykgG9aeViAvsoVCavqAUUoLr'
    access_secret = '5kquNGlQKCOCnWsbVdKMvDCD9vvZlomlg5Hnp1pSuTpLR'

    auth = tp.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # Construct the API instance
    api = tp.API(auth)

    return api

#loading datasets for E3 part 1
print("Loading network...")
network = load_network('trained_networks/NN_N10_TS0.js')
print("Done.")

mins, maxs = extract_minmax('data/TrainingSet_0.csv')

def send_to_neuronal(status):

    medicines = []
    for medicine in known_medicines:
        if medicine in status.text.lower():
            medicines.append(medicine.upper())

    if medicines != []:
        features = extract_features(status.text)
        features['retweet_count'] = status.retweet_count
        process_tweet(status.user.screen_name, status.text, medicines, features)
    else:
        print("Tweet de @%s no contiene medicinas conocidas. Tuit = [%s]"%(status.user.screen_name, status.text))

def process_tweet(user, text, medicines, features):

    normalized_vector = []

    normalized_vector.append((features['lenght'] - mins['lenght'])/(maxs['lenght'] - mins['lenght']))
    normalized_vector.append((features['retweet_count'] - mins['retweet_count'])/(maxs['retweet_count'] - mins['retweet_count']))
    normalized_vector.append((features['hashtags'] - mins['hashtags'])/(maxs['hashtags'] - mins['hashtags']))
    normalized_vector.append((features['mentions'] - mins['mentions'])/(maxs['mentions'] - mins['mentions']))
    normalized_vector.append((features['contains_url'] - mins['contains_url'])/(maxs['contains_url'] - mins['contains_url']))
    normalized_vector.append((features['demand_words'] - mins['demand_words'])/(maxs['demand_words'] - mins['demand_words']))
    normalized_vector.append((features['offer_words'] - mins['offer_words'])/(maxs['offer_words'] - mins['offer_words']))
    normalized_vector.append((features['tfidf_demand'] - mins['tfidf_demand'])/(maxs['tfidf_demand'] - mins['tfidf_demand']))
    normalized_vector.append((features['tfidf_offer'] - mins['tfidf_offer'])/(maxs['tfidf_offer'] - mins['tfidf_offer']))
    normalized_vector.append((features['neg_words'] - mins['neg_words'])/(maxs['neg_words'] - mins['neg_words']))
    normalized_vector.append((features['pos_words'] - mins['pos_words'])/(maxs['pos_words'] - mins['pos_words']))
    normalized_vector.append((features['n_known_medicines'] - mins['n_known_medicines'])/(maxs['n_known_medicines'] - mins['n_known_medicines']))

    # calculate normalized features
    result = predict(network, normalized_vector)

    if result == 0:
        print("Tweet de @%s NO BUSCA NI OFERTA las siguientes medicinas %s. Tuit = [%s]"%(user, str(medicines), text))
    if result == 1:
        print("Tweet de @%s OFERTA las siguientes medicinas %s. Tuit = [%s]"%(user, str(medicines), text))
    if result == 2:
        print("Tweet de @%s SOLICITA las siguientes medicinas %s. Tuit = [%s]"%(user, str(medicines), text))

def start_streaming():

    print('Starting Streaming... \n')
    api = tweetpy_auth()
    myStreamListener = MyStreamListener()
    myStream = tp.Stream(auth = api.auth, listener = myStreamListener)

    myStream.filter(track=['ServicioPublico'])

if __name__ == '__main__':

    start_streaming()
