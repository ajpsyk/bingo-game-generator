from pypdf import PdfWriter, PdfReader
import fitz  # PyMuPDF

def draw_debug_box(draw, x0, y0, x1, y1, color="red", thickness=1):
    """
    Draws a rectangle outline for visual debugging.

    Args:
        draw: PIL.ImageDraw.Draw object.
        x0, y0, x1, y1: Rectangle coordinates (top-left to bottom-right).
        color: Outline color.
        thickness: Outline thickness in pixels.
    """
    draw.rectangle([(x0, y0), (x1, y1)], outline=color, width=thickness)

def fit_text_to_width(text, font_loader, max_width, initial_size, min_size=8):
    """
    Dynamically adjusts font size to fit text within max_width.
    
    Parameters:
        text (str): The text string to measure.
        font_loader (callable): A function like lambda size: ImageFont.truetype(path, size).
        max_width (int): The maximum allowed pixel width.
        initial_size (int): Starting font size.
        min_size (int): Minimum font size allowed.

    Returns:
        font (ImageFont.FreeTypeFont): A font instance that fits within max_width.
    """
    size = initial_size
    font = font_loader(size)
    text_width = font.getbbox(text)[2] - font.getbbox(text)[0]

    while text_width > max_width and size > min_size:
        size -= 1
        font = font_loader(size)
        text_width = font.getbbox(text)[2] - font.getbbox(text)[0]

    return font

def merge_pdfs(output_path, pdf_paths):
    writer = PdfWriter()
    for path in pdf_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f_out:
        writer.write(f_out)

def get_resolution_from_pdf():
    doc = fitz.open("my_pdf.pdf")

    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            print(f"Image: {pix.width}x{pix.height} px")

