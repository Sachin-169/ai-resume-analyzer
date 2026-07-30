import fitz
import re

def extract_text_from_pdf(file_path):
    pdf_document = fitz.open(file_path)

    text = ""
    for page in pdf_document:
        text += page.get_text()

    text = text.strip()

    # Normalize line endings from different operating systems
    # Windows uses \r\n while macOS/Linux use \n thats why there are 2 replace statements
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    #remove invisible unicode characters
    # 200b = Zero Width Space, 200c = Zero Width Non-Joiner, 200d = Zero Width Joiner, feff= Byte Order Mark  
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)

    #remove leading/trailing spaces from every line
    text = "\n".join(line.strip() for line in text.splitlines())

    #normalize blank lines, and in this case if there are 3 or more lines to 2 lines, looks cleaner
    text = re.sub(r"\n{3,}", "\n\n", text)

    #normalize multiple spaces in between words, so in this case if there are 2 or more spaces bw 2 words, it reduces to 1 space
    text = re.sub(r" {2,}", " ", text)

    #so we are converting any type of bullet point to 1 specific type of bullet point
    text = re.sub(r"[▪●◦►]", "•", text)

    #changing hyphens to • but we didnt add it to the prev statement because there are few hyphens in middle like say Full-Stack
    text = re.sub(r"^(\s*)-", r"\1•", text, flags=re.MULTILINE)

    return text