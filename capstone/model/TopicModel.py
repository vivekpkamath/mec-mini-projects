from ModelInterface import ModelInterface
import pandas as pd
import nltk
import tqdm
import gensim
import pickle
import base64
from datetime import datetime
'''
Default topic model using gensim and LDA
'''
class TopicModel(ModelInterface):

    def __init__(self ) -> None:
        super().__init__()


    def __normalize_corpus(self, documents):
        stop_words = nltk.corpus.stopwords.words('english')
        wtk = nltk.tokenize.RegexpTokenizer(r'\w+')
        wnl = nltk.stem.wordnet.WordNetLemmatizer()

        norm_documents = []
        for document in tqdm.tqdm(documents):
            document = document.lower()
            document_tokens = [token.strip() for token in wtk.tokenize(document)]
            document_tokens = [wnl.lemmatize(token) for token in document_tokens if not token.isnumeric()]
            document_tokens = [token for token in document_tokens if len(token) > 1]
            document_tokens = [token for token in document_tokens if token not in stop_words]
            document_tokens = list(filter(None, document_tokens))
            if document_tokens:
                norm_documents.append(document_tokens)
                
        return norm_documents
        
    def pre_process(self):
        print('pre_process')
        #nltk.download('punkt')
        #nltk.download('stopwords')
        #nltk.download('wordnet')
        #nltk.download('omw-1.4')
        
        #load all documents from database
        document_df = self._dal.getAllDocuments()
        self._norm_documents = self.__normalize_corpus(document_df['body'].to_list())
        #create bigram phrases
        #print(self._norm_documents)
        # higher threshold fewer phrases.
        #bigram = gensim.models.Phrases(self._norm_documents, min_count=20, threshold=20, delimiter= b'_') 
        bigram = gensim.models.Phrases(self._norm_documents, min_count=20, threshold=20) 

        bigram_model = gensim.models.phrases.Phraser(bigram)
        print(bigram_model[self._norm_documents[0]][:50])

        self._norm_corpus_bigrams = [bigram_model[doc] for doc in self._norm_documents]

        # Create a dictionary representation of the documents.
        self._dictionary = gensim.corpora.Dictionary(self._norm_corpus_bigrams)
        print('Sample word to number mappings:', list(self._dictionary.items())[:15])
        print('Total Vocabulary Size:', len(self._dictionary))

        # Filter out words that occur less than 20 documents, or more than 60% of the documents.
        self._dictionary.filter_extremes(no_below=20, no_above=0.6)
        print('Total Vocabulary Size:', len(self._dictionary))

        #Create BOW
        self._bow_corpus = [self._dictionary.doc2bow(text) for text in self._norm_corpus_bigrams]
        print(self._bow_corpus[1][:50])
        print('Total number of documents:', len(self._bow_corpus))

    def train(self):
        # TODO: Put hyperparameter tuning here by taking parameters to this class
        print('train')
        TOTAL_TOPICS = 10
        lda_model = gensim.models.LdaModel(corpus=self._bow_corpus, id2word=self._dictionary, chunksize=1740, 
                                        alpha='auto', eta='auto', random_state=42,
                                        iterations=500, num_topics=TOTAL_TOPICS, 
                                        passes=20, eval_every=None)
        '''
        for topic_id, topic in lda_model.print_topics(num_topics=TOTAL_TOPICS, num_words=20):
            print('Topic #'+str(topic_id+1)+':')
            print(topic)
            print()
        '''
        # model quality
        cv_coherence_model_lda = gensim.models.CoherenceModel(model=lda_model, corpus=self._bow_corpus, 
                                                            texts=self._norm_corpus_bigrams,
                                                            dictionary=self._dictionary, 
                                                            coherence='c_v')
        avg_coherence_cv = cv_coherence_model_lda.get_coherence()

        umass_coherence_model_lda = gensim.models.CoherenceModel(model=lda_model, corpus=self._bow_corpus, 
                                                                texts=self._norm_corpus_bigrams,
                                                                dictionary=self._dictionary, 
                                                                coherence='u_mass')
        avg_coherence_umass = umass_coherence_model_lda.get_coherence()

        perplexity = lda_model.log_perplexity(self._bow_corpus)

        print('Avg. Coherence Score (Cv):', avg_coherence_cv)
        print('Avg. Coherence Score (UMass):', avg_coherence_umass)
        print('Model Perplexity:', perplexity)            
        # pickle model save it to the database along with training date and metrics.
        # We will also need to pickle  bow, dictionary and other supporting stuff.
        pickle_lda_model = base64.b64encode(pickle.dumps(lda_model))
        pickle_bow_corpus = base64.b64encode(pickle.dumps(self._bow_corpus))
        pickle_dictionary = base64.b64encode(pickle.dumps(self._dictionary))
        print(len(pickle_lda_model))
        print(len(pickle_bow_corpus))
        #store model
        model_id = self._dal.addOneModel('topicLDA', pickle_lda_model, pickle_bow_corpus, pickle_dictionary)
        #store metric
        self._dal.addModelMetric(model_id[0][0], 'Avg. Coherence Score (Cv)', str(avg_coherence_cv))
        self._dal.addModelMetric(model_id[0][0], 'Avg. Coherence Score (UMass)', str(avg_coherence_umass))
        self._dal.addModelMetric(model_id[0][0], 'Model Perplexity', str(perplexity))
        for topic_id, topic in lda_model.print_topics(num_topics=TOTAL_TOPICS, num_words=20):
            print('Topic #'+str(topic_id+1)+':')
            print(topic)
            print()
            self._dal.addTopicforModel(model_id, topic)


    def predict(self, unseen_doc):
        print('predict')
        # read the current model from database.
        rows = self._dal.getCurrentModelOfType('topicLDA')
        if (len(rows) != 1):
            return
        
        #get model pickle from rows and see if we can rehydrate the model from the pickle
        print(type(rows))
        print(len(rows))
        
        lda_model = pickle.loads(base64.b64decode(rows[0][2]))
        #bow_corpus = pickle.loads(base64.b64decode(rows[0][3]))
        dictionary = pickle.loads(base64.b64decode(rows[0][4]))

        #get the new document and find topics in it
        norm_documents = self.__normalize_corpus(unseen_doc)
        bigram = gensim.models.Phrases(norm_documents, min_count=20, threshold=20) 

        bigram_model = gensim.models.phrases.Phraser(bigram)
        

        norm_corpus_bigrams = [bigram_model[doc] for doc in norm_documents]
        new_doc_bow_corpus = [dictionary.doc2bow(text) for text in norm_corpus_bigrams]
        TOTAL_TOPICS = 10
        '''
        lda_model = gensim.models.LdaModel(new_doc_bow_corpus, id2word=dictionary, chunksize=1740, 
                                        alpha='auto', eta='auto', random_state=42,
                                        iterations=500, num_topics=TOTAL_TOPICS, 
                                        passes=20, eval_every=None)        
        '''
        #lda_model[new_doc_bow_corpus]
        print(lda_model.get_document_topics(new_doc_bow_corpus))
        
        for topic_id, topic in lda_model.print_topics(num_topics=10, num_words=20):
            print('Topic #'+str(topic_id+1)+':')
            print(topic)
            print()
            

        
        
