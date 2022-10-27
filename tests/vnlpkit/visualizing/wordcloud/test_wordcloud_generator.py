import MeCab
import pprint

from vnlpkit.visualizing.wordcloud.wordcloud_generator import WordCloudGenerator

text = "うちの息子がいつもお世話になってます。いつもいつもすみません"
document_1 = "りんご ごりら らっぱ"
document_2 = "りんご 子ゴリラ ラッパー"
document_3 = "ニシゴリラの学名は「Gorilla gorilla（ゴリラ ゴリラ）」。「ニシゴリラ」の亜種である「ニシローランドゴリラ」は「Gorilla gorilla gorilla（ゴリラ ゴリラ ゴリラ）」。"
documents = [document_1, document_2, document_3]


def test_generate_from_text() -> None:
    tagger = MeCab.Tagger("-Owakati")
    parsed_text = tagger.parse(text)
    print(f"parsed_text: {parsed_text}")

    generator = WordCloudGenerator()
    result_dict = generator.generate_from_text(tokenized_text=parsed_text)
    freq_dict = result_dict["freq_dict"]
    pprint.pprint(f"freq_dict: {freq_dict}")
    assert freq_dict["いつも"] > freq_dict["息子"]


def test_generate_from_tfidf_for_text_and_documents() -> None:
    tagger = MeCab.Tagger("-Owakati")
    parsed_text_list = [tagger.parse(document) for document in documents]
    print(f"parsed_text_list: {parsed_text_list}")
    tokenized_text = parsed_text_list[0]
    fig_path = "tests/vnlpkit/visualizing/wordcloud/output/wordcloud_tfidf.png"

    generator = WordCloudGenerator()
    result_dict = generator.generate_from_tfidf_for_text_and_documents(
        tokenized_text=tokenized_text,
        documents=documents,
        fig_path=fig_path,
    )
    freq_dict = result_dict["freq_dict"]
    pprint.pprint(f"freq_dict: {freq_dict}")
    assert freq_dict["りんご"] > freq_dict["ごりら"]
