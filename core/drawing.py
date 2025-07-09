from core.utils import draw_margin_box
from PIL import Image, ImageDraw


def generate_bingo_card(page_layout, bingo_card_layout):
    # generate white canvas and define print-safe area
    canvas = Image.new("RGBA", (page_layout.WIDTH_PIXELS, page_layout.HEIGHT_PIXELS), (255, 255, 255, 255))
    usable_width = page_layout.WIDTH_PIXELS - 2 * page_layout.MARGIN
    usable_height = page_layout.HEIGHT_PIXELS - 2 * page_layout.MARGIN

    # load and paste frame
    frame = Image.open(bingo_card_layout.FRAME_IMAGE_PATH).convert("RGBA").resize((usable_width, usable_height), Image.LANCZOS)
    canvas.paste(frame, (page_layout.MARGIN, page_layout.MARGIN))

    # define content area
    padding = bingo_card_layout.FRAME_INNER_PADDING
    content_x = page_layout.MARGIN + padding["left"]
    content_y = page_layout.MARGIN + padding["top"]
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
    grid_x = content_x
    grid_y = content_y + header_height
    grid_height = usable_height - header_height
    cell_width = bingo_card_layout.GRID_COL

    # add content to cells

    # prinatble area    
    draw_margin_box(draw, page_layout)
    # content area
    draw.rectangle(
        [(content_x, content_y), (content_x + content_width, content_y + content_height)],
        outline="green",
        width=2
    )
    # header area
    draw.rectangle(
        [(header_x, content_y), (header_x + header_width, content_y + header_height)],
        outline="blue",
        width=1
    )

    canvas.save(page_layout.OUTPUT_PATH, "PDF", dpi=(page_layout.DPI, page_layout.DPI))


def generate_calling_cards_single(page_layout, calling_card_single_layout):
    pass

def generate_calling_cards_multi(page_layout, calling_card_multi_layout):
    pass

def generate_tokens_large(page_layout, tokens_large_layout):
    pass

def generate_tokens_small(page_layout, tokens_small_layout):
    pass
