import PyPDF2


def load_pdf(file):

    text = ""

    pdf_reader = PyPDF2.PdfReader(file)

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def load_txt(file):

    return file.read().decode("utf-8")