
from pathlib import Path
from file_processor import extract_text


class TestUploadedFile:
    def __init__(self, path):
        self.path = Path(path)
        self.name = self.path.name

    def getvalue(self):
        return self.path.read_bytes()


file = TestUploadedFile(
    "sample_materials/sample_lesson.txt"
)

try:
    text = extract_text(file)

    print("FILE EXTRACTION SUCCESSFUL!\n")
    print("Extracted lesson:\n")
    print(text)

except Exception as error:
    print("Error:", error)
