import parameter_validator
import filter_utils
import cleaner
import processors

import pandas as pd
import pypeln.thread as th
import json
from datetime import datetime
from deep_translator import GoogleTranslator
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from collections import Counter
import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image
import io
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime
import warnings
warnings.simplefilter("ignore", UserWarning)

class NewsLakeDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return NewsLakeDataFrame
      
    # ----------------------------------------------------

    def __create_feature_map__(self, text):
        if text != '':
            temp = word_tokenize(text)
            vectorizer = TfidfVectorizer(max_features=10)
            tfidf_matrix = vectorizer.fit_transform(temp)
            keywords = vectorizer.get_feature_names_out()
            return keywords
        else:
            return text
    # ----------------------------------------------------

    def __handle_stopwords__(self,text):
        language = getattr(self, '_content_language', 'en')
        list_stop_word = stopwords.indonesia() if language == 'id' else stopwords.english()
        temp = word_tokenize(text)
        without_stop_word = ' '.join([ i.strip() for i in temp if i not in list_stop_word])
        without_stop_word = without_stop_word.split(' ')
        without_stop_word = [ i.strip() for i in without_stop_word if i not in list_stop_word]
        return ' '.join(without_stop_word)

    # ----------------------------------------------------
    
    def __get_all_words__(self, have_featute_map = False):
        if have_featute_map == False:
            self.content_feature_map = self['content']\
                            .apply(self.__handle_stopwords__)\
                            .apply(self.__create_feature_map__)
            
        combined_list = [item for sublist in self.content_feature_map for item in sublist]
        word_freq = Counter(combined_list)
        all_words = {word.upper(): count for word, count in word_freq.items()}
        return all_words
        
    # ----------------------------------------------------

    def __chunk_sentences__(self, text):
        sentences = text.split('. ')
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence) + 1 
            if current_length + sentence_length > 4900:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = []
                current_length = 0
            
            current_chunk.append(sentence)
            current_length += sentence_length

        if current_chunk:
            chunks.append('. '.join(current_chunk) + '.')

        return chunks


    def __translator__(self, text, target):

        if(len(text) <= 4900): 
            translated = GoogleTranslator(source='auto', target = target)\
                            .translate(text)
            return translated
        
        chunks = self.__chunk_sentences__(text)
        sentences = []
        for chunk in chunks:
            if len(chunk) > 4999:
                continue
            else:
                translated = GoogleTranslator(source='auto', target = target)\
                                .translate(chunk)
                sentences.append(translated)

        return '. '.join(sentences).strip()

    
    # ----------------------------------------------------

    def __build_wordcloud__(self):
        have_featute_map = True if hasattr(self, 'content_feature_map') else False
        words = self.__get_all_words__(have_featute_map)
        wordcloud = WordCloud(stopwords=stopwords.indonesia() , 
                              colormap="Blues",
                              max_words=100).generate_from_frequencies(words)
        return wordcloud
    
    def wordcloud(self, timeframe = None):
        if timeframe:
            t = datetime.strptime(timeframe,"%Y-%m-%d")
            wordcloud = self[self['published_date'].dt.date == t].__build_wordcloud__()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
        else:
            wordcloud = self.__build_wordcloud__()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()

    def timeseries_wordcloud(self):
        timeframes = sorted(self['published_date'].dt.date.unique())
    
        if len(timeframes) > 1:
            fig, ax = plt.subplots(figsize=(12, 4),ncols=len(timeframes))
            for i,time in enumerate(timeframes):
                wc = self[self['published_date'].dt.date == time]\
                        .__build_wordcloud__()
        
                # Convert to image array
                img_buf = io.BytesIO()
                wc.to_image().save(img_buf, format='PNG')
                img_buf.seek(0)
                img = Image.open(img_buf)
                # ax[i].set_xticks(time.strftime("%Y-%m-%d"))
                ax[i].set_xticklabels(time.strftime("%Y-%m-%d"), rotation=45)
                ax[i].set_yticks([])
                ax[i].set_xticks([])  # Hide y-axis
                # Insert image on plot
                ax[i].imshow(img, extent=(i-0.4, i+0.4, -0.5, 0.5), aspect='auto', zorder=10)
                ax[i].set_xlabel(time.strftime("%Y-%m-%d"))

            plt.tight_layout()
            plt.show()

        elif len(timeframes) == 1:
            fig,ax = plt.subplots(figsize=(7, 4))
            wc = self.__build_wordcloud__()
            time = self['published_date'].dt.date.unique()[0]
            # Convert to image array
            img_buf = io.BytesIO()
            wc.to_image().save(img_buf, format='PNG')
            img_buf.seek(0)
            img = Image.open(img_buf)
            # ax.set_xticks(time.strftime("%Y-%m-%d"))
            ax.set_xticklabels(time.strftime("%Y-%m-%d"), rotation=45)
            ax.set_yticks([])
            ax.set_xticks([])  # Hide y-axis
            # Insert image on plot
            ax.imshow(img, aspect='auto', zorder=10)
            ax.set_xlabel(time.strftime("%Y-%m-%d"))

            plt.tight_layout()
            plt.show()


    # ----------------------------------------------------
    
    def find_news(self, keyword):
        return self[self['content'].str.contains(rf'\b{keyword}\b', case=False, regex=True)]

    # ----------------------------------------------------

    def translate(self, target):
        self._content_language = target
        self['title'] = self['title'].apply(lambda x: self.__translator__(x, target))
        self['content'] = self['content'].apply(lambda x: self.__translator__(x, target))

# ----------------------------------------------------

def _clean_dataframe(df):
    df['title'] = df['title'] \
                    .apply(cleaner.basic)\
                    .apply(str.title)
    
    df['content'] = df[['link','content']]\
                        .apply(lambda x: cleaner.domain_base(x['content'],x['link']), axis=1)
    
    df.dropna(inplace= True)

# ----------------------------------------------------

def _transform_dataframe(df):
    df.reset_index(drop=True, inplace=True)
    df['published_date'] = pd.to_datetime(df['published_date'],utc=True)
    
# ----------------------------------------------------

def _translate_dataframe(df, language):
    df['title'] = df['title'].apply(lambda x: processors._translate(x,language))
    df['content'] = df['content'].apply(lambda x: processors._translate(x,language))

# ----------------------------------------------------

def _fetch(master_data, n_news, language, start_date = None, end_date = None):
    region = master_data['region_id']
    topic = master_data['topic']
    source = master_data['source']
    list_title = []
    list_link = []
    list_pubDate = []
    list_content = []

    for i, row in master_data.iterrows():
        title, link, pubDate, content = processors._get_attribute(row['rss_link'], n_news, start_date, end_date)
        list_title.append(title)
        list_link.append(link)
        list_pubDate.append(pubDate)
        list_content.append(content)
    
    data = {
        'region' :region,
        'topic' :topic,
        'source' :source,
        'title' :list_title,
        'link' :list_link,
        'published_date' :list_pubDate,
        'content' :list_content,
    }

    nl = NewsLakeDataFrame(data)\
        .explode(['title','link','published_date','content'])
    
    return nl

# ----------------------------------------------------

def _load_source_json():
    with open('sources.json') as json_data:
        data = json.load(json_data)
    
    rows = []
    for region_id, topics in data.items():
        for topic, sources in topics.items():
            for source, link in sources.items():
                if type(link) == list :
                    for l in link:
                        rows.append({
                            "region_id": region_id,
                            "topic": topic,
                            "source": source,
                            "rss_link": l
                        })
                else:
                    rows.append({
                        "region_id": region_id,
                        "topic": topic,
                        "source": source,
                        "rss_link": link
                    })
    return rows
    
def get_news(regions = ['id', 'us'],
            topics = '*', n_news = 5, 
            sources = '*', language = 'en', keyword=None,
            start_date = None, 
            end_date = None, 
            ):
    
    parameter_validator._nnews(n_news)
    parameter_validator._datetime(start_date, end_date)

    # ----------------------------------------------------

    parsed_json = _load_source_json()
    master_data = pd.DataFrame(parsed_json)
    
    # ----------------------------------------------------
    
    filter_by_region = filter_utils._region(master_data, regions)
    filter_by_topic = filter_utils._topic(filter_by_region, topics)
    filter_by_source = filter_utils._source(filter_by_topic, sources)
    
    # ----------------------------------------------------
    
    nl = None
    
    if  (start_date != None) or (end_date != None):
        start_date = datetime.strptime(start_date,"%Y-%m-%d") if start_date else None
        end_date = datetime.strptime(end_date,"%Y-%m-%d") if end_date else None
    
        nl =  _fetch(filter_by_source, n_news, language,
                    start_date, end_date)
    else:
        nl = _fetch(filter_by_source, n_news, language)

    _clean_dataframe(nl)
    _transform_dataframe(nl)
    nl.translate(language)

    nl = nl[nl['content'] != '']
    return nl
