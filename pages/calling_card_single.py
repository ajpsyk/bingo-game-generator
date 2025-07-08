import os
import random
from PIL import Image, ImageDraw, ImageFont
from config import (
    DPI, PAGE_WIDTH, PAGE_HEIGHT,
    TOP_MARGIN, BOTTOM_MARGIN, SIDE_MARGIN,
    FONT_PATH
)

# Page-specific layout constants
VERTICAL_SPACING = int(0.125 * DPI)

COLS = 5
ROWS = 6

LINE_COLOR = "#545454"
LINE_THICKNESS = 2

LABEL_HEIGHT_RATIO = 0.14
LABEL_GAP_RATIO = 0.3
CELL_PADDING_Y_RATIO = 0.05
LABEL_FONT_SCALE = 1.0

HEADER_IMAGE_PATH = "header/Calling_Card_Header.png"

def load_header(path, usable_width):
    """
    Loads and resizes the header image to fit within the usable width of the page.
    
    Args:
        path (str): Path to the header image file.
        usable_width (int): Width available for the header.
    
    Returns:
        header (Image): The resized header image.
        header_width (int): Width of the resized header.
        header_height (int): Height of the resized header.
    """
    header = Image.open(path).convert("RGBA")
    header_width, header_height = header.size

    if header_width > usable_width:
        scale_factor = usable_width / header_width
        header_width = int(header_width * scale_factor)
        header_height = int(header_height * scale_factor)
        header = header.resize((header_width, header_height), Image.LANCZOS)

    return header, header_width, header_height


def draw_grid(draw, x, y, cols, rows, cell_width, cell_height, line_color, line_thickness):
    """
    Draws a rectangular grid on the canvas using the specified dimensions.
    
    Args:
        draw (ImageDraw.Draw): The drawing context.
        x (int): X-coordinate of the top-left corner of the grid.
        y (int): Y-coordinate of the top-left corner of the grid.
        cols (int): Number of columns.
        rows (int): Number of rows.
        cell_width (int): Width of each cell.
        cell_height (int): Height of each cell.
        line_color (str): Color of grid lines.
        line_thickness (int): Thickness of grid lines.
    """
    for i in range(rows + 1):
        y_line = y + i * cell_height
        draw.line([(x, y_line), (x + cols * cell_width, y_line)], fill=line_color, width=line_thickness)

    for j in range(cols + 1):
        x_line = x + j * cell_width
        draw.line([(x_line, y), (x_line, y + rows * cell_height)], fill=line_color, width=line_thickness)


def generate_calling_card_single(image_folder, output_path):
    """
    Generates a single-page calling card with a grid of labeled images and a header.
    
    Args:
        image_folder (str): Folder containing PNG images to include in the grid.
        output_path (str): File path to save the generated PDF.
    """
    usable_width = PAGE_WIDTH - 2 * SIDE_MARGIN
    usable_height = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN

    header, header_width, header_height = load_header(HEADER_IMAGE_PATH, usable_width)

    header_x = SIDE_MARGIN + (usable_width - header_width) // 2
    header_y = TOP_MARGIN

    grid_y = header_y + header_height + VERTICAL_SPACING
    grid_height = usable_height - header_height - VERTICAL_SPACING
    cell_width = usable_width // COLS
    cell_height = grid_height // ROWS
    grid_x = SIDE_MARGIN

    canvas = Image.new("RGBA", (PAGE_WIDTH, PAGE_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    canvas.paste(header, (header_x, header_y), header)

    draw_grid(draw, grid_x, grid_y, COLS, ROWS, cell_width, cell_height, LINE_COLOR, LINE_THICKNESS)

    image_files = [
        f for f in os.listdir(image_folder)
        if f.lower().endswith(".png")
    ]
    random.shuffle(image_files)

    assert len(image_files) == COLS * ROWS, f"Expected exactly {COLS * ROWS} images"

    label_height = int(cell_height * LABEL_HEIGHT_RATIO)
    gap = int(label_height * LABEL_GAP_RATIO)
    padding_y = int(cell_height * CELL_PADDING_Y_RATIO)

    available_img_height = cell_height - 2 * padding_y - gap - label_height
    available_img_width = cell_width - int(cell_width * 0.1)

    font_size = int(label_height * LABEL_FONT_SCALE)
    font = ImageFont.truetype(FONT_PATH, size=font_size)

    for idx, image_file in enumerate(image_files):
        row = idx // COLS
        col = idx % COLS

        x0 = grid_x + col * cell_width
        y0 = grid_y + row * cell_height

        img_path = os.path.join(image_folder, image_file)
        img = Image.open(img_path).convert("RGBA")
        img.thumbnail((available_img_width, available_img_height), Image.LANCZOS)

        img_x = x0 + (cell_width - img.width) // 2
        img_y = y0 + padding_y
        canvas.paste(img, (img_x, img_y), img)

        label = os.path.splitext(image_file)[0].replace("_", " ").upper()
        bbox = font.getbbox(label)
        text_width = bbox[2] - bbox[0]
        text_x = x0 + (cell_width - text_width) // 2
        text_y = img_y + img.height + gap

        draw.text((text_x, text_y), label, font=font, fill="black")

    canvas.save(output_path, "PDF", dpi=(DPI, DPI))
    print(f"Grid layout saved to {output_path}")