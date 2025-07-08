from core.utils import draw_margin_box
from PIL import Image, ImageDraw


def generate_bingo_card(page_layout, bingo_card_layout):
    #create canvas, load assets
    canvas = Image.new("RGBA", (page_layout.WIDTH_PIXELS, page_layout.HEIGHT_PIXELS), (255, 255, 255, 255))
    usable_width = page_layout.WIDTH_PIXELS - 2 * page_layout.MARGIN
    usable_height = page_layout.HEIGHT_PIXELS - 2 * page_layout.MARGIN
    draw = ImageDraw.Draw(canvas)
    
    draw_margin_box(draw, page_layout)
    canvas.save(page_layout.OUTPUT_PATH, "PDF", dpi=(page_layout.DPI, page_layout.DPI))
    # define padding within frame
    # load header

def generate_calling_cards_single(page_layout, calling_card_single_layout):
    pass

def generate_calling_cards_multi(page_layout, calling_card_multi_layout):
    pass

def generate_tokens_large(page_layout, tokens_large_layout):
    pass

def generate_tokens_small(page_layout, tokens_small_layout):
    pass
