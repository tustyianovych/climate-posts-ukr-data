from string import punctuation
import re
import logging
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline
import emoji


class NumbersFromTextSeparator(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.re_sep_digit = re.compile(r"([\d]+)([а-яА-Я]+)")
        return self

    def transform(self, X):
        X = X.copy()
        return X.apply(lambda x: self.re_sep_digit.sub(r"\1 \2", x))


class WhitespaceCharacterRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.re_whitespaces_rem = re.compile(r'\s+', re.MULTILINE)
        return self

    def transform(self, X):
        return X.apply(lambda x: self.re_whitespaces_rem.sub(r" ", x))


class MultipleWhitespaceRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(lambda x: re.sub(' +', ' ', x))


class PunctuationRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.punctiation = punctuation + '—«»–“”―‼…‒' + '№•°¯−→⁃'
        return self

    def transform(self, X):
        return X.apply(
            lambda x: re.sub('[%s]' % re.escape(self.punctiation), '', x)
            )


class EmojiRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.re_emojis_rem = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U0001F1F2-\U0001F1F4"  # Macau flag
            u"\U0001F1E6-\U0001F1FF"  # flags
            u"\U0001F600-\U0001F64F"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U0001F1F2"
            u"\U0001F1F4"
            u"\U0001F620"
            u"\u200d"
            u"\u2640-\u2642"
            "]+", flags=re.UNICODE
            )
        return self

    def transform(self, X):
        return X.apply(lambda x: self.re_emojis_rem.sub(r"", x))


class EmojiRemover2(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.apply(lambda x: emoji.replace_emoji(x, replace=''))
        return X


class StripFlankingSpaces(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.str.strip()


class LowerCaser(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.str.lower()


class UrlRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.re_url = re.compile(r"https?://\S+|www\.\S+")
        return self

    def transform(self, X):
        return X.apply(lambda x: self.re_url.sub(r" ", x))


class TmeRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.tme = re.compile(r'\st.me/.+')
        return self

    def transform(self, X):
        return X.apply(lambda x: self.tme.sub(r" ", x))


class EmailRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.re_email = re.compile(r'[\w\.-]+@[\w\.-]+')
        return self

    def transform(self, X):
        return X.apply(lambda x: self.re_email.sub(r" ", x))


class HashtagRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.re_hashtag = re.compile(r'#(?<=)\w+')
        return self

    def transform(self, X):
        return X.apply(lambda x: self.re_hashtag.sub(r" ", x))


class AtRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.re_at = re.compile(r'@(?<=)\w+')
        return self

    def transform(self, X):
        return X.apply(lambda x: self.re_at.sub(r" ", x))


class HeaderCleaner(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    @staticmethod
    def filt(text):
        subs_filt = re.search(
            r'(п[іо]дпи[сш])(и|уй|ывай|ать)(те)?(с[ья])',
            text,
            flags=re.IGNORECASE | re.UNICODE
            )
        bot_channel_filt = re.search(
            r'(\W@)|( \| )|(наш канал)|((в|на) ?.{0,5} бот)|(посилання на)|(Реальная? В[іо]йна)|(Осведомитель)|(Блокнот пропагандиста)|(Поколение «ZOV»)|(ВПШ)|(Два майора)|(РИА Новости\b)|(Украина\.ру)|(гаспарян)|(архангел спецназа)|(труха)|(слат[иь] нов)',
            text,
            flags=re.IGNORECASE | re.UNICODE
            )
        bank_info = re.search(
            r'(UAH|USD|EUR|Paypal|BTC|ETH|Банк[ауи]|Приват|картк?и|Моно(банк)?|Ціль|Крипта|Privat|Mono|Р\/р |Реквізити|Patreon|coffee|валюта).{0,5}:',
            text,
            flags=re.IGNORECASE | re.UNICODE
            )

        return (
            len(text) > 4
            # and not set(text) & set(['@', '|'])
            and subs_filt is None
            and bot_channel_filt is None
            and bank_info is None
            )

    @staticmethod
    def header_detector(row):
        res = []
        # for sent in row.split('. '):
        for sent in re.split(r'(?<=[\.\!\?])\s+', row):
            res.extend(el for el in re.split(r'(\r\n|\r|\n)', sent)
                       if HeaderCleaner.filt(el)
                       )

        return '. '.join(res)

    def transform(self, X):
        return X.apply(HeaderCleaner.header_detector)


class SentenceEnding(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        # self.sent_ending = re.compile('[!?\\. ]{3,}')
        self.sent_ending = re.compile(r'(?<=[!?\.: ])[\. ]{1,2}')
        self.sent_ending2 = re.compile(r'( [\.:] )')
        return self

    def transform(self, X):
        X = X.apply(lambda x: self.sent_ending2.sub(r". ", x))
        return X.apply(lambda x: self.sent_ending.sub(r" ", x))


class SentenceSeparator(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.sent_separator = re.compile(r'(\.|\. | )?\\n\s*\\n')
        return self

    def transform(self, X):
        return X.apply(lambda x: self.sent_separator.sub(r". ", x))


class CardNumberRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):

        self.card_num = re.compile(r'U?A?\d{2} ?[\d ]{14,}')
        return self

    def transform(self, X):
        return X.apply(lambda x: self.card_num.sub(r" ", x))


class PhoneNumberRemover(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        self.card_num = re.compile(r'\+?3?8? ?\(?\d{3}\)?[ -]*\d{3,4}[ -]*\d{2,4}[ -]*\d{2,4}?')
        return self

    def transform(self, X):
        return X.apply(lambda x: self.card_num.sub(r" ", x))


class ShortMessageFilterer(BaseEstimator):

    def fit(self, X, y=None):
        logging.info(f'Input shape: {X.shape[0]}')
        return self

    def fit_transform(self, X, y=None):
        logging.info(f'Input shape: {X.shape[0]}')
        filt = (X.apply(len) > 10) & (X.notna())
        logging.info(f'Output shape: {filt.sum()}')
        return X[filt]

    def transform(self, X):
        return X


preprocessing_pipe = make_pipeline(
    NumbersFromTextSeparator(),
    TmeRemover(),  # expand
    UrlRemover(),
    SentenceSeparator(),
    HeaderCleaner(),
    WhitespaceCharacterRemover(),
    EmailRemover(),
    CardNumberRemover(),
    PhoneNumberRemover(),  # use after CardNumberRemover!
    HashtagRemover(),
    # AtRemover(),  # redundant if HeaderCleaner is present upstream
    # EmojiRemover(),  # fast, doesn't remove all; redundant if #2 is used
    EmojiRemover2(),  # too slow: 105 seconds, but removes all emojis
    # EmoticonRemover(),  # too slow: 47 seconds
    SentenceEnding(),
    PunctuationRemover(),
    MultipleWhitespaceRemover(),  # after removing punctuation
    StripFlankingSpaces(),
    LowerCaser(),
    # ShortMessageFilterer()
)