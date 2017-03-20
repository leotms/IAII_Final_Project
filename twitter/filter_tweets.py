import pandas as pd
import random as rd

def readData(file):
    '''
        Reads data inside a .txt file containing the vectors of training/testing data.
        returns the attributes normalized.
    '''
    dataset = pd.read_csv(file, delimiter = "," , encoding='mac_roman', index_col = False)
    return dataset

target_words = [
    "solicit",
    "necesit",
    "urgen",
    "medic",
    "mg",
    "gr",
    "dosis",
    "ampollas",
    "pastillas",
    "disponib",
    "fundaci",
    "hosp",
    "dona",
    "requi",
    "reque",
    "paciente",
    "serviciopublico",
    "pediat",
    "tabletas",
    "comprimidos",
    "tratamiento"
]

offer_dict = [
    "dispon",
    "dona",
    'dono',
    "ofre",
    "vend",
    "vent",
    'cambio',
    'cambia',
    'farmacia',
    'droguer',
    'botiquer',
    'tengo',
    'tenemos',
    'conseg',
    'confirm',
    'necesitas',
]

demand_dict = [
    'urge',
    'favor',
    'gracias',
    'requie',
    'requerimos',
    'necesit',
    'emergencia',
    'solicit',
    'agrade',
    'consig',
    'conseg',
    'donde',
    'dónde',
    'busca',
    'busq',
    'busco',
    'ubica',
    'encontrar',
    'ayuda',
    'adquirir',
    'informa',
    'referencia',
    'compra',
    'compro',
    'trata'
]

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

#This stores already human classified data.
demand_data = pd.DataFrame()
offer_data  = pd.DataFrame()
other_data  = pd.DataFrame()

def first_filter(filename):
    '''
        Applies first filter to saparte usefull data from random tweets in a
        first instance
    '''

    #Set up new dataframes
    #This stores the dataframe for a first filtered data.
    needed_data = pd.DataFrame()

    known_tweets = []
    data = readData(filename)

    for i in range(len(data)):
        row = data.iloc[i]
        text = row['text'].lower()

        if text in known_tweets:
            continue
        else:
            known_tweets.append(text)

        is_useful = False
        is_demand = False

        for word in target_words:
            if word in text:
                is_useful = True

        if is_useful:
            needed_data = needed_data.append(row)


        print(i)

    #rearranging columns
    needed_data = needed_data[['id', 'user_id', 'text', 'retweet_count', 'posted_at']]

    print('First filter completed.')
    print("Useful: %d"%(len(needed_data)))
    needed_data.to_csv('CollectedData/needed_data.csv', index=None, sep=',')

def second_filter(filename):
    ''' this applies a second filter to all data already classified by a human.
    '''
    data = readData(filename)
    #This stores already human classified data.

    demand_data = pd.DataFrame()
    offer_data  = pd.DataFrame()
    other_data  = pd.DataFrame()

    for i in range(len(data)):
        row = data.iloc[i]
        cluster = row['cluster']
        cluster = int(cluster)

        if cluster == 1:
            offer_data = offer_data.append(row)
        if cluster == 2:
            demand_data = demand_data.append(row)
        else:
            other_data = other_data.append(row)


    #rearranging columns
    offer_data = offer_data[['id', 'user_id', 'text', 'retweet_count', 'posted_at','cluster']]
    demand_data = demand_data[['id', 'user_id', 'text', 'retweet_count', 'posted_at','cluster']]
    other_data = other_data[['id', 'user_id', 'text', 'retweet_count', 'posted_at','cluster']]

    print("Demand: %d"%(len(demand_data)))
    print("Offer: %d"%(len(offer_data)))
    print("Other: %d"%(len(other_data)))

    demand_data.to_csv('CollectedData/demand_data.csv', index=None, sep=',')
    offer_data.to_csv('CollectedData/offer_data.csv',   index=None, sep=',')
    other_data.to_csv('CollectedData/other_data.csv',   index=None, sep=',')

def identify_medicines(filename):

    print("identifying medicines...")
    from palabras_comunes import palabras_comunes

    known_words = {}
    hashtags    = []

    data = readData(filename)

    for i in range(len(data)):
        row = data.iloc[i]
        text = row['text'].lower()
        text = text.split(' ')

        for word in text:
            #remove commas, spaces and points
            word = word.replace(",",'')
            word = word.replace(".",'')
            word = word.replace(":",'')
            if "http" in word:
                continue
            if "@" in word:
                continue
            if word in palabras_comunes:
                continue
            if "#" in word:
                hashtags.append(word.lower())
            else:
                if word in known_words:
                    known_words[word] += 1
                else:
                    known_words[word] = 1

    for word in known_words:
        for hashtag in hashtags:
            if word in hashtag:
                known_words[word] += 1

    words    = open('words.csv', 'w')

    for word in known_words:
        words.write("%s, %s\n"%(word, str(known_words[word])))

    words.close()

    print("Done.")


def get_features(filenames):
    print("Calculating features...")
    from palabras_comunes import palabras_positivas, palabras_negativas

    for filename in filenames:

        data = readData(filename)
        new_filename = filename.split(".")[0] + "_featured." + filename.split(".")[1]

        featured_data = pd.DataFrame(columns=('id', 'lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words', 'neg_words', 'pos_words', 'n_known_medicines','cluster'))

        for i in range(len(data)):
            new_row = []
            row = data.iloc[i]

            text = row['text'].lower()

            lenght = len(text)
            retweet_count = row['retweet_count']

            hashtags = 0
            mentions = 0
            contains_url = 0

            demand_words = 0
            offer_words  = 0

            neg_words = 0
            pos_words = 0

            n_known_medicines = 0

            print(text)
            print("Len: %d"%(lenght))
            print("RT: %d"%(retweet_count))

            text = text.split(' ')

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

                for i in demand_dict:
                    if i in word:
                        demand_words += 1
                for i in offer_dict:
                    if i in word:
                        offer_words  += 1
                for i in palabras_positivas:
                    if i in word:
                        pos_words += 1
                for i in palabras_negativas:
                    if i in word:
                        neg_words += 1
                for i in known_medicines:
                    if i in word:
                        n_known_medicines  += 1

            new_row.append(row['id'])
            new_row.append(lenght)
            new_row.append(retweet_count)
            new_row.append(hashtags)
            new_row.append(mentions)
            new_row.append(contains_url)
            new_row.append(demand_words)
            new_row.append(offer_words)
            new_row.append(neg_words)
            new_row.append(pos_words)
            new_row.append(n_known_medicines)
            new_row.append(row['cluster'])

            featured_data.loc[len(featured_data)] = new_row

            print("hashtags: %d"%(hashtags))
            print("mentions: %d"%(mentions))
            print("contains_url: %d"%(contains_url))
            print("demand_words: %d"%(demand_words))
            print("offer_words: %d"%(offer_words))
            print("neg_words: %d"%(neg_words))
            print("pos_words: %d"%(pos_words))
            print("known_medicines: %d"%(n_known_medicines))

        featured_data = featured_data[['id', 'lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words', 'neg_words', 'pos_words', 'n_known_medicines','cluster']]
        featured_data.to_csv(new_filename, index = None, sep=',')

def select_samle(filename, n):

    print("Selecting samples for %s..."%(filename))
    data = readData(filename)

    new_filename = filename.split(".")[0] + "_" + str(n) + '.' + filename.split(".")[1]

    n_data = len(data)
    rand = list(range(n_data))
    rand = rd.sample(rand, n)

    newfile = pd.DataFrame()

    for i in rand:
        row = data.iloc[i]
        newfile = newfile.append(row)

    newfile = newfile[['id', 'user_id', 'text', 'retweet_count', 'posted_at','cluster']]
    newfile.to_csv(new_filename, index=None, sep=',')

def split_testset_for_training(filenames):
    print("splitting training and test set...")

    training_data = pd.DataFrame(columns=('id', 'lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words', 'neg_words', 'pos_words', 'n_known_medicines','cluster'))
    test_data     = pd.DataFrame(columns=('id', 'lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words', 'neg_words', 'pos_words', 'n_known_medicines','cluster'))

    for filename in filenames:

        data = readData(filename)
        n_data = len(data)
        rand = list(range(n_data))
        percentage = round(n_data*0.8)
        rand = rd.sample(rand, percentage)

        for i in range(len(data)):
            row = data.iloc[i]
            if i in rand:
                training_data = training_data.append(row)
            else:
                test_data = test_data.append(row)

    training_data.to_csv('TrainingSet3.csv', index = None, sep=',')
    test_data.to_csv('TestSet3.csv', index = None, sep=',')

    print(len(training_data))
    print(len(test_data))

def split_crossvalidation(filenames):
    print("splitting training and test set...")

    training_data = pd.DataFrame(columns=('id', 'lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words', 'neg_words', 'pos_words', 'n_known_medicines','cluster'))
    test_data     = pd.DataFrame(columns=('id', 'lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words', 'neg_words', 'pos_words', 'n_known_medicines','cluster'))

    array_1 = []
    array_2 = []
    array_3 = []

    #first_array
    data = readData(filenames[0])
    n_data = len(data)
    rand = list(range(n_data))
    percentage = round(n_data*0.1)

    while rand:
        samples = rd.sample(rand,percentage)
        new_arr = []
        for sample in samples:
            rand.remove(sample)
            row = data.iloc[sample]
            new_arr.append(row)

        array_1.append(new_arr)

    #first_array
    data = readData(filenames[1])
    n_data = len(data)
    rand = list(range(n_data))
    percentage = round(n_data*0.1)

    while rand:
        samples = rd.sample(rand,percentage)
        new_arr = []
        for sample in samples:
            rand.remove(sample)
            row = data.iloc[sample]
            new_arr.append(row)

        array_2.append(new_arr)

    #first_array
    data = readData(filenames[2])
    n_data = len(data)
    rand = list(range(n_data))
    percentage = round(n_data*0.1)

    while rand:
        samples = rd.sample(rand,percentage)
        new_arr = []
        for sample in samples:
            rand.remove(sample)
            row = data.iloc[sample]
            new_arr.append(row)

        array_3.append(new_arr)

    print(len(array_1[0]))
    print(len(array_2[0]))
    print(len(array_3[0]))

    for i in range(10):
        training_data = pd.DataFrame(columns=('id', 'lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words', 'neg_words', 'pos_words', 'n_known_medicines','cluster'))
        test_data     = pd.DataFrame(columns=('id', 'lenght', 'retweet_count', 'hashtags', 'mentions', 'contains_url', 'demand_words', 'offer_words', 'neg_words', 'pos_words', 'n_known_medicines','cluster'))
        for j in range(10):
            if i == j:
                for elem in array_1[j]:
                    test_data = test_data.append(elem)
                for elem in array_2[j]:
                    test_data = test_data.append(elem)
                for elem in array_3[j]:
                    test_data = test_data.append(elem)
            else:
                for elem in array_1[j]:
                    training_data = training_data.append(elem)
                for elem in array_2[j]:
                    training_data = training_data.append(elem)
                for elem in array_3[j]:
                    training_data = training_data.append(elem)

        training_data.to_csv('TrainingSet_' + str(i) + '.csv', index = None, sep=',')
        test_data.to_csv('TestSet_' + str(i) + '.csv', index = None, sep=',')

# print("Running first filter...")
# # first_filter("CollectedData/TweetsBirdwatcher.csv")
# print("Done.")
# print("------------------")
# print("Running second filter...")
# second_filter("CollectedData/TweetsHumanClassified.csv")
# print("Done.")
# print("------------------")

# identify_medicines("CollectedData/offer_data.csv")
# get_features(["CollectedData/demand_data_2000.csv", "CollectedData/offer_data_2000.csv", "CollectedData/other_data_2000.csv"])
# split_testset_for_training(["CollectedData/demand_data_2000_featured.csv", "CollectedData/offer_data_2000_featured.csv", "CollectedData/other_data_2000_featured.csv"])
split_crossvalidation(["CollectedData/demand_data_2000_featured.csv", "CollectedData/offer_data_2000_featured.csv", "CollectedData/other_data_2000_featured.csv"])

# get_features("CollectedData/demand_data_2000_verified.csv")
# select_samle("CollectedData/offer_data.csv", 2000)
# select_samle("CollectedData/demand_data.csv", 2000)
# select_samle("CollectedData/other_data.csv", 2000)
