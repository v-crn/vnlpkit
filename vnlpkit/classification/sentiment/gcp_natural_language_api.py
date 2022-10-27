from concurrent.futures import ProcessPoolExecutor
import json
import multiprocessing
import os
import time
from typing import Dict, Optional, Tuple
from google.cloud import language_v1
from tqdm.auto import tqdm
import pandas as pd
import numpy as np

tqdm.pandas()
client = language_v1.LanguageServiceClient()
N_MAX_REQUEST_PER_MINUTE = 600
N_MAX_REQUEST_PER_SEC = N_MAX_REQUEST_PER_MINUTE / 60


def attatch_sentiment_label(
    sentiment_score: float,
    pos_thresh: float = 0.15,
    neg_thresh: float = -0.15,
    sentiment_labels: Dict[str, str] = {
        "NEGATIVE": "NEGATIVE",
        "NEUTRAL": "NEUTRAL",
        "POSITIVE": "POSITIVE",
    },
) -> str:
    sentiment_label = sentiment_labels["NEUTRAL"]
    if sentiment_score >= pos_thresh:
        sentiment_label = sentiment_labels["POSITIVE"]
    elif sentiment_score <= neg_thresh:
        sentiment_label = sentiment_labels["NEGATIVE"]

    return sentiment_label


def analyze_sentiment_with_gcp_natural_language_api(
    text: str,
    language: str = "ja",
    pos_thresh: float = 0.15,
    neg_thresh: float = 0.15,
) -> dict:
    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {
        "content": text,
        "type_": type_,
        "language": language,
    }

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(
        document=document,
        encoding_type=encoding_type,
    )

    document_score = response.document_sentiment.score
    sentiment_label = attatch_sentiment_label(
        sentiment_score=document_score,
        pos_thresh=pos_thresh,
        neg_thresh=neg_thresh,
    )

    output = {
        "document_sentiment": {
            "magnitude": response.document_sentiment.magnitude,
            "score": document_score,
            "sentiment_label": sentiment_label,
        },
        "language": response.language,
        "sentences": [
            {
                "text": {
                    "content": sentence.text.content,
                    "begin_offset": sentence.text.begin_offset,
                },
                "sentence": {
                    "magnitude": sentence.sentiment.magnitude,
                    "score": sentence.sentiment.score,
                },
            }
            for sentence in response.sentences
        ],
    }
    return output


def _analyze(params: Tuple) -> dict:
    (
        text,
        language,
        pos_thresh,
        neg_thresh,
        splitted_output_dir,
        index,
    ) = params
    output = analyze_sentiment_with_gcp_natural_language_api(
        text=text,
        language=language,
        pos_thresh=pos_thresh,
        neg_thresh=neg_thresh,
    )

    if splitted_output_dir is not None:
        filename = "splitted_result" + str(index)
        splitted_filepath = os.path.join(splitted_output_dir, filename)
        os.makedirs(splitted_output_dir, exist_ok=True)

        with open(splitted_filepath, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

    return output


def add_sentiment_labels_with_gcp_nl_api_without_rate_limit(
    df: pd.DataFrame,
    text_col: str,
    score_col: str = "sentiment_score",
    magnitude_col: str = "sentiment_magnitude",
    sentiment_col: str = "sentiment",
    language: str = "ja",
    pos_thresh: float = 0.15,
    neg_thresh: float = -0.15,
    splitted_output_dir: Optional[str] = None,
) -> pd.DataFrame:
    df = df.copy()
    text_list = df[text_col].tolist()
    params_list = [
        (text, language, pos_thresh, neg_thresh, splitted_output_dir, index)
        for index, text in enumerate(text_list)
    ]

    sentiment_score_list = []
    sentiment_magnitude_list = []
    sentiment_label_list = []

    max_workers = multiprocessing.cpu_count()
    with ProcessPoolExecutor(max_workers) as executor:
        output_list = list(
            tqdm(executor.map(_analyze, params_list), total=len(params_list))
        )

    for output in tqdm(output_list):
        sentiment_score_list.append(output["document_sentiment"]["score"])
        sentiment_magnitude_list.append(output["document_sentiment"]["magnitude"])
        sentiment_label_list.append(output["document_sentiment"]["sentiment_label"])

    df[score_col] = sentiment_score_list
    df[magnitude_col] = sentiment_magnitude_list
    df[sentiment_col] = sentiment_label_list

    return df


def add_sentiment_labels_with_gcp_nl_api(
    df: pd.DataFrame,
    text_col: str,
    score_col: str = "sentiment_score",
    magnitude_col: str = "sentiment_magnitude",
    sentiment_col: str = "sentiment",
    language: str = "ja",
    pos_thresh: float = 0.15,
    neg_thresh: float = -0.15,
    n_split: int = 10,
    n_max_request_per_sec: float = 10,
    safety_margin_sec: float = 0.1,
    splitted_output_dir: Optional[str] = None,
) -> pd.DataFrame:
    df = df.copy()

    # API リクエスト制限に配慮するためのインターバル時間を設定する
    len_df = len(df)
    n_unit = len_df // n_split
    sleep_sec = n_unit / n_max_request_per_sec + safety_margin_sec
    print(f"sleep_sec: {sleep_sec}\n")

    df_list = np.array_split(df, n_split)
    df_output_list = []
    for index, df_p in tqdm(enumerate(df_list)):
        output_dir = (
            os.path.join(splitted_output_dir, f"df_{index}")
            if isinstance(splitted_output_dir, str)
            else None
        )
        df_p = add_sentiment_labels_with_gcp_nl_api_without_rate_limit(
            df=df_p,
            text_col=text_col,
            score_col=score_col,
            magnitude_col=magnitude_col,
            sentiment_col=sentiment_col,
            language=language,
            pos_thresh=pos_thresh,
            neg_thresh=neg_thresh,
            splitted_output_dir=output_dir,
        )
        df_output_list.append(df_p)
        time.sleep(sleep_sec)

    df_output = pd.concat(df_output_list)

    return df_output
