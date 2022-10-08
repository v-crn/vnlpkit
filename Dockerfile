FROM python:3.10-slim
ENV PYTHONUNBUFFERED=true
WORKDIR /root

RUN apt update -y \
    && apt install -y --no-install-recommends \
    sudo \
    curl \
    wget \
    git \
    gcc \
    g++ \
    build-essential \
    nodejs \
    npm \
    ca-certificates \
    software-properties-common \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    file \
    && apt -y clean \
    && apt -y autoremove \
    && rm -rf /var/lib/apt/lists/*

# config
RUN ldconfig
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONPATH /root:$PYTHONPATH

# mecab ipadic-neologd
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && cd mecab-ipadic-neologd \
    && bin/install-mecab-ipadic-neologd -n -y
COPY mecabrc /usr/local/etc/mecabrc
ENV MECABRC /usr/local/etc/mecabrc

# pip
RUN pip install --upgrade pip && \
    pip install setuptools -U

# Install Poetry
ENV POETRY_HOME /opt/poetry
ENV PATH $POETRY_HOME/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false

# Install python packages
COPY pyproject.toml ./
RUN poetry install

# jupyter
RUN jupyter lab build --minimize False && \
    jupyter notebook --generate-config

CMD jupyter lab --allow-root --ip 0.0.0.0 --no-browser
