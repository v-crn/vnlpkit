echo "--- MeCab Sample ---"
echo
echo "--- Dictionary paths ---"
find / -path */mecab/dic 2> /dev/null
echo
echo
echo "--- Morphological analysis samples ---"
echo
echo "[debian]"
DEBIAN_DIC_PATH=$(find / -path */mecab/dic/debian 2> /dev/null | head -1)
echo すもももももももものうち | mecab -d $DEBIAN_DIC_PATH
echo
echo 彼女はペンパイナッポーアッポーペンと恋ダンスを踊った。 | mecab -d $DEBIAN_DIC_PATH
echo
echo アーニャピーナッツが好き | mecab -d $DEBIAN_DIC_PATH
echo
echo
echo "[ipadic-utf8]"
IPADIC_UTF8_DIC_PATH=$(find / -path */mecab/dic/ipadic-utf8 2> /dev/null | head -1)
echo すもももももももものうち | mecab -d $IPADIC_UTF8_DIC_PATH
echo
echo 彼女はペンパイナッポーアッポーペンと恋ダンスを踊った。 | mecab -d $IPADIC_UTF8_DIC_PATH
echo
echo アーニャピーナッツが好き | mecab -d $IPADIC_UTF8_DIC_PATH
echo
echo
echo "[juman-utf8]"
JUMAN_UTF8_DIC_PATH=$(find / -path */mecab/dic/juman-utf8 2> /dev/null | head -1)
echo すもももももももものうち | mecab -d $JUMAN_UTF8_DIC_PATH
echo
echo 彼女はペンパイナッポーアッポーペンと恋ダンスを踊った。 | mecab -d $JUMAN_UTF8_DIC_PATH
echo
echo アーニャピーナッツが好き | mecab -d $JUMAN_UTF8_DIC_PATH
echo
echo
echo "[mecab-ipadic-neologd]"
MECAB_IPADIC_NEOLOGD_DIC_PATH=$(find / -path */mecab/dic/mecab-ipadic-neologd 2> /dev/null | head -1)
echo
echo すもももももももものうち | mecab -d $MECAB_IPADIC_NEOLOGD_DIC_PATH
echo
echo 彼女はペンパイナッポーアッポーペンと恋ダンスを踊った。 | mecab -d $MECAB_IPADIC_NEOLOGD_DIC_PATH
echo
echo アーニャピーナッツが好き | mecab -d $MECAB_IPADIC_NEOLOGD_DIC_PATH
