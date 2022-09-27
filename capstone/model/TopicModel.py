import sys

sys.path.append('../sql')
from DatabaseIO import DatabaseIO 
from ModelInterface import ModelInterface
import pandas as pd
import nltk
import tqdm
import gensim

class TopicModel(ModelInterface):

    def __init__(self, db_io ) -> None:
        super().__init__(db_io)


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
        document_df = self._db_io.read_to_dataframe('select * from documents;')
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
        print('train')
        TOTAL_TOPICS = 100
        lda_model = gensim.models.LdaModel(corpus=self._bow_corpus, id2word=self._dictionary, chunksize=1740, 
                                        alpha='auto', eta='auto', random_state=42,
                                        iterations=500, num_topics=TOTAL_TOPICS, 
                                        passes=20, eval_every=None)
        for topic_id, topic in lda_model.print_topics(num_topics=TOTAL_TOPICS, num_words=20):
            print('Topic #'+str(topic_id+1)+':')
            print(topic)
            print()                                        
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
        # save pickled model so that it can be pulled up for predictions

    def predict(self):
        #How do we get topics from individual document from now on?
        pass
