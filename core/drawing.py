from core.utils import draw_debug_box
from PIL import Image, ImageDraw


def generate_bingo_card(page_layout, bingo_card_layout):
    # generate white canvas and define print-safe area
    height = page_layout.HEIGHT_PIXELS
    width = page_layout.WIDTH_PIXELS
    canvas = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    margin = page_layout.MARGIN
    usable_width = width - 2 * margin
    usable_height = height - 2 * margin

    # load and paste frame
    frame = Image.open(bingo_card_layout.FRAME_IMAGE_PATH).convert("RGBA").resize((usable_width, usable_height), Image.LANCZOS)
    canvas.paste(frame, (margin, margin))

    # define content area
    padding = bingo_card_layout.FRAME_INNER_PADDING
    content_x = margin + padding["left"]
    content_y = margin + padding["top"]
    content_width = usable_width - padding["left"] - padding["right"]
    content_height = usable_height - padding["top"] - padding["bottom"]

    # load and paste header
    header = Image.open(bingo_card_layout.HEADER_IMAGE_PATH).convert("RGBA")
    header_width, header_height = header.size
    if header_width != content_width:
        scale_factor = content_width / header_width
        header_width = int(header_width * scale_factor)
        header_height = int(header_height * scale_factor)
        header = header.resize((header_width, header_height), Image.LANCZOS)
    header_x = content_x + (content_width - header_width) // 2
    canvas.paste(header, (header_x, content_y), header)

    # draw grid
    draw = ImageDraw.Draw(canvas)
    line_color = bingo_card_layout.GRID_LINE_COLOR
    line_thickness = bingo_card_layout.GRID_LINE_THICKNESS
    cols = bingo_card_layout.GRID_COLS
    rows = bingo_card_layout.GRID_ROWS
    grid_x = content_x
    grid_y = content_y + header_height
    grid_height = content_height - header_height
    cell_width = content_width // cols
    cell_height = grid_height // rows

    for i in range(rows + 1):
        y_line = grid_y + i * cell_height
        draw.line(
            [(grid_x, y_line), (grid_x + cols * cell_width, y_line)],
            fill=line_color,
            width=line_thickness)
    for j in range(cols + 1):
        x_line = grid_x + j * cell_width
        draw.line([(x_line, grid_y), (x_line, grid_y + rows * cell_height)],
                  fill=line_color,
                  width=line_thickness)

    # load images and labels and paste to cells
    """
    # Margin box
    draw_debug_box(
        draw,
        page_layout.MARGIN,
        page_layout.MARGIN,
        page_layout.WIDTH_PIXELS - page_layout.MARGIN,
        page_layout.HEIGHT_PIXELS - page_layout.MARGIN,
        color="red"
    )

    # Content box
    draw_debug_box(
        draw,
        content_x,
        content_y,
        content_x + content_width,
        content_y + content_height,
        color="green"
    )

    # Header box
    draw_debug_box(
        draw,
        header_x,
        content_y,
        header_x + header_width,
        content_y + header_height,
        color="blue"
    )
    """
    canvas.save(page_layout.OUTPUT_PATH, "PDF", dpi=(page_layout.DPI, page_layout.DPI))    


def generate_calling_cards_single(page_layout, calling_card_single_layout):
    pass

def generate_calling_cards_multi(page_layout, calling_card_multi_layout):
    pass

def generate_tokens_large(page_layout, tokens_large_layout):
    pass

def generate_tokens_small(page_layout, tokens_small_layout):
    pass
