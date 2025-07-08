from PIL import Image


def generate_bingo_card(page_layout, bingo_card_layout):
    #create canvas
    canvas = Image.new("RGBA", (page_layout.PAGE_HEIGHT_PIXELS, page_layout.PAGE_WIDTH_PIXELS), (255, 255, 255, 255))
    # if there is a frame, position frame within page margins
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
