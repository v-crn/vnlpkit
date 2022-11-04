FROM vcrn/jupyterlab-nlp-ja:python3.8
WORKDIR $WORK_DIR
USER $USER

# --- Install python packages ---
RUN poetry add git+https://github.com/v-crn/vnlpkit.git
COPY pyproject.toml $WORK_DIR
RUN poetry update

# --- Update & Upgrade ---
# --- Create the necessary links and cache ---
# --- Delete unnecessary packages ---
RUN apt-get update && apt-get upgrade -y \
    && ldconfig \
    && apt-get -y clean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

COPY scripts/ $WORK_DIR/scripts/
CMD [ "sh", "scripts/run.sh" ]
