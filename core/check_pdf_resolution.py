import fitz  # PyMuPDF
doc = fitz.open("my_pdf.pdf")

for page in doc:
    for img in page.get_images(full=True):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        print(f"Image: {pix.width}x{pix.height} px")