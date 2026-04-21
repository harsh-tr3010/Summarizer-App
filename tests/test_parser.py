import os
from utils.file_parser import extract_text

SAMPLE_DIR = "sample_files"


class UploadedFileMock:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)

    def read(self):
        with open(self.path, "rb") as f:
            return f.read()

    def seek(self, pos):
        pass


def test_sample_1_pdf_exists():
    assert os.path.exists(f"{SAMPLE_DIR}/Sample_1.pdf")


def test_sample_2_pdf_exists():
    assert os.path.exists(f"{SAMPLE_DIR}/Sample_2.pdf")


def test_extract_text_sample_1():
    file = UploadedFileMock(f"{SAMPLE_DIR}/Sample_1.pdf")
    text = extract_text(file)

    assert isinstance(text, str)
    assert len(text.strip()) > 20


def test_extract_text_sample_2():
    file = UploadedFileMock(f"{SAMPLE_DIR}/Sample_2.pdf")
    text = extract_text(file)

    assert isinstance(text, str)
    assert len(text.strip()) > 20