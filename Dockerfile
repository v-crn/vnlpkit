FROM python:3.10-slim-buster
WORKDIR /root
ENV PYTHONUNBUFFERED=true
ENV PYTHONPATH /root:$PYTHONPATH

RUN apt update && apt install -y \
    sudo \
    vim \
    curl \
    wget \
    git \
    build-essential \
    npm

# --- NodeJS ---
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt install -y nodejs

# -- Locales ---
RUN apt update && apt install -y locales
RUN localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

# --- Fonts ---
RUN apt update && apt install -y \
    fontconfig \
    fonts-ipaexfont

# --- MeCab ---
RUN apt update && apt install -y \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    file
RUN mecab --version

# --- mecab-ipadic-NEologd ---
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
RUN mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y
# To install all dictionaries:
# RUN mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -a -y

ENV MECABRC /etc/mecabrc
RUN cp /etc/mecabrc /etc/mecabrc.default
RUN cat /etc/mecabrc.default | sed -e "s/^dicdir/; dicdir/" \
    | sed -e "/; dicdir/a dicdir = $(find / -path */mecab/dic/mecab-ipadic-neologd 2> /dev/null | head -1)" \
    > $MECABRC
RUN rm -rf mecab-ipadic-neologd

# --- Delete unnecessary packages ---
RUN apt -y clean \
    && apt -y autoremove \
    && rm -rf /var/lib/apt/lists/*

# --- pip ---
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

# --- Poetry ---
ENV POETRY_HOME /opt/poetry
ENV PATH $POETRY_HOME/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false

# --- Python packages ---
COPY pyproject.toml ./
RUN poetry install

# --- Jupyter ---
RUN jupyter lab build --minimize False
RUN jupyter notebook --generate-config

CMD jupyter lab --allow-root --ip 0.0.0.0 --port ${PORT}
