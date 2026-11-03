
import pymupdf
from docx import Document
from io import BytesIO

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_TEXT_LENGTH = 30000


def extract_text(uploaded_file):
    """
    Extract readable text from PDF, DOCX, or TXT.
    """

    if uploaded_file is None:
        raise ValueError("Please upload a file.")

    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("File must be 10 MB or smaller.")

    if filename.endswith(".pdf"):
        with pymupdf.open(
            stream=file_bytes,
            filetype="pdf"
        ) as pdf:
            text = "\n".join(
                page.get_text("text")
                for page in pdf
            )

    elif filename.endswith(".docx"):
        document = Document(BytesIO(file_bytes))

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        # Include text from tables
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += "\n" + cell.text

    elif filename.endswith(".txt"):
        try:
            text = file_bytes.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ValueError(
                "TXT file must use UTF-8 encoding."
            )

    else:
        raise ValueError(
            "Unsupported file type. Use PDF, DOCX, or TXT."
        )

    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text found in the file."
        )

    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(
            "Lesson is too long. Use a shorter file "
            "or divide it into smaller sections."
        )

    return text
