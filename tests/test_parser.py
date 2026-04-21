import os
from utils.file_parser import extract_text

SAMPLE_DIR = "sample_files"


class UploadedFileMock:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.file = open(path, "rb")

    def read(self, *args):
        return self.file.read(*args)

    def seek(self, offset, whence=0):
        return self.file.seek(offset, whence)

    def tell(self):
        return self.file.tell()

    def close(self):
        self.file.close()


def test_sample_1_pdf_exists():
    assert os.path.exists(f"{SAMPLE_DIR}/Sample_1.pdf")


def test_sample_2_pdf_exists():
    assert os.path.exists(f"{SAMPLE_DIR}/Sample_2.pdf")


def test_extract_text_sample_1():
    file = UploadedFileMock(f"{SAMPLE_DIR}/Sample_1.pdf")
    text = extract_text(file)

    assert isinstance(text, str)
    assert len(text.strip()) > 20

    file.close()


def test_extract_text_sample_2():
    file = UploadedFileMock(f"{SAMPLE_DIR}/Sample_2.pdf")
    text = extract_text(file)

    assert isinstance(text, str)
    assert len(text.strip()) > 20

    file.close()