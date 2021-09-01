import pke
import ginza
import nltk

pke.base.ISO_to_language['ja_ginza'] = 'japanese'
stopwords = list(ginza.STOP_WORDS)
nltk.corpus.stopwords.words_org = nltk.corpus.stopwords.words
nltk.corpus.stopwords.words = lambda lang: stopwords \
    if lang == 'japanese' else nltk.corpus.stopwords.words_org(lang)


def extract_kw_by_pke(
        text: str, method='multipartie_rank',
        language='ja_ginza', normalization=None,
        candidate_selection_params: dict = None,
        candidate_weighting_params: dict = None,
        get_n_best_params: dict = None,
        return_type='with_score'):
    if method == 'position_rank':
        extractor = pke.unsupervised.PositionRank()
    elif method == 'multipartie_rank':
        extractor = pke.unsupervised.MultipartiteRank()
    elif method == 'kpminer':
        extractor = pke.unsupervised.KPMiner()
    elif method == 'yake':
        extractor = pke.unsupervised.YAKE()

    # normalization が未指定だと NLTK のステミング処理がかかって日本語未対応でエラーになるので デフォルトでは None を指定
    extractor.load_document(
        input=text, language=language, normalization=normalization)

    # フレーズ候補を形成する品詞
    extractor.candidate_selection(**candidate_selection_params)

    # トピック分類する際のクラスタリングの結合閾値と距離の計算方法、重み調整のハイパーパラメータの指定
    try:
        extractor.candidate_weighting(**candidate_weighting_params)
    except:
        None
    output = extractor.get_n_best(**get_n_best_params)
    if return_type == 'with_score':
        return output

    output = [e[0] for e in output]
    if return_type == 'str':
        return ' '.join(output)
    return output
