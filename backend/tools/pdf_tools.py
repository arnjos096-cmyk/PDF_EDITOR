import fitz # PyMuPDF

def redact_text(file_path: str, output_path: str, text_to_redact: str):
    """
    Finds all instances of a specific text string in the PDF and draws a black redaction box over them.
    Returns the path to the redacted PDF.
    """
    doc = fitz.open(file_path)
    for page in doc:
        text_instances = page.search_for(text_to_redact)
        for inst in text_instances:
            page.add_redact_annot(inst, fill=(0, 0, 0))
        page.apply_redactions()
    
    doc.save(output_path)
    return output_path

def add_watermark(file_path: str, output_path: str, watermark_text: str):
    """
    Adds a watermark text diagonally across all pages of the PDF.
    """
    doc = fitz.open(file_path)
    for page in doc:
        rect = page.rect
        page.insert_text(
            fitz.Point(rect.width / 4, rect.height / 2),
            watermark_text,
            fontsize=50,
            color=(1, 0, 0),
            fill_opacity=0.3,
            rotate=45
        )
    doc.save(output_path)
    return output_path
