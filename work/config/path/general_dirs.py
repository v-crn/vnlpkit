import os


class GeneralDirs:
    WORK_DIR = "~/work"
    DATA_DIR = os.path.join(WORK_DIR, "data")
    CORPUS_DIR = os.path.join(DATA_DIR, "corpus")
