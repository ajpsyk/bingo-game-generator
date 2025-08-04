"""Static layout config. Might convert to dataclass later if made dynamic."""
# specific output paths for each layout
# make frame optional
# maybe make way to save settings

class PageLayout:
    DPI = 200

    WIDTH_INCHES = 8.5
    HEIGHT_INCHES = 11
    WIDTH_PIXELS = int(WIDTH_INCHES * DPI)
    HEIGHT_PIXELS = int(HEIGHT_INCHES * DPI)

    BOTTOM_MARGIN = int(0.5 * DPI)
    LEFT_MARGIN = int(0.5 * DPI)
    RIGHT_MARGIN = int(0.5 * DPI)
    TOP_MARGIN = int(0.3 * DPI)

    FONT_PATH = "assets/fonts/Dekko-Regular.ttf"
    OUTPUT_PATH = "output/preview_grid.pdf"

class BingoCardLayout:
    CARD_AMOUNT = 1


    LABEL_COLOR = "#581a4d"

    FRAME_ENABLED = False
    FRAME_INNER_PADDING = {
        "top": int(95 * (PageLayout.DPI / 300)),
        "bottom": int(120 * (PageLayout.DPI / 300)),
        "left": int(100 * (PageLayout.DPI / 300)),
        "right": int(100 * (PageLayout.DPI / 300))
    } # all values in pixels


    HEADER_MARGIN_BOTTOM = int(0.1 * PageLayout.DPI)

    GRID_COLS = 5
    GRID_ROWS = 5

    GRID_LINE_COLOR = "#69622c"
    GRID_LINE_THICKNESS = 2

    LABEL_HEIGHT_RATIO = 0.14
    LABEL_GAP_RATIO = 0.3
    CELL_PADDING_X_RATIO = 0.1
    CELL_PADDING_Y_RATIO = 0.05
    LABEL_FONT_SCALE = 1.0

    BINGO_IMAGES_PATH = "assets/bingo images"
    HEADER_IMAGE_PATH = "assets/header/Bingo_Card_Header.png"
    FRAME_IMAGE_PATH = "assets/frame/Halloween_Border.png"
    FREE_SPACE_IMAGE_PATH = "assets/free space/Free_Space.png"

class BingoCardMultiLayout:
    CARD_AMOUNT = 2
    #CARD_SPACING = int(PageLayout.MARGIN * 2 * PageLayout.DPI)

    GRID_COLS = 5
    GRID_ROWS = 5

    GRID_LINE_COLOR = "#69622c"
    GRID_LINE_THICKNESS = 2

    LABEL_COLOR = "#581a4d"

    FRAME_INNER_PADDING = {
        "top": int(95 * (PageLayout.DPI / 300)),
        "bottom": int(120 * (PageLayout.DPI / 300)),
        "left": int(100 * (PageLayout.DPI / 300)),
        "right": int(100 * (PageLayout.DPI / 300))
    } # all values in pixels

    LABEL_HEIGHT_RATIO = 0.14
    LABEL_GAP_RATIO = 0.3
    CELL_PADDING_X_RATIO = 0.1
    CELL_PADDING_Y_RATIO = 0.05
    LABEL_FONT_SCALE = 1.0

    BINGO_IMAGES_PATH = "assets/bingo images"
    HEADER_IMAGE_PATH = "assets/header/Bingo_Card_Header.png"
    FRAME_IMAGE_PATH = "assets/frame/Halloween_Border.png"
    FREE_SPACE_IMAGE_PATH = "assets/free space/Free_Space.png"

class CallingCardsSinglePageLayout:
    GRID_COLS = 5
    GRID_ROWS = 6

    GRID_LINE_COLOR = "#545454"
    GRID_LINE_THICKNESS = 2

    LABEL_COLOR = "#581a4d"

    LABEL_HEIGHT_RATIO = 0.14
    LABEL_GAP_RATIO = 0.3
    CELL_PADDING_X_RATIO = 0.1
    CELL_PADDING_Y_RATIO = 0.05
    LABEL_FONT_SCALE = 1.0

    BINGO_IMAGES_PATH = "assets/Bingo Images"
    HEADER_IMAGE_PATH = "assets/header/Calling_Card_Header.png"

class CallingCardsMultiPageLayout:
    GRID_COLS = 2
    GRID_ROWS = 2

    GRID_LINE_COLOR = "#69622c"
    GRID_LINE_THICKNESS = 2

    LABEL_COLOR = "#581a4d"

    LABEL_HEIGHT_RATIO = 0.14
    LABEL_GAP_RATIO = 0.3
    CELL_PADDING_X_RATIO = 0.1
    CELL_PADDING_Y_RATIO = 0.05
    LABEL_FONT_SCALE = 1.0

    SCISSORS_WIDTH_SCALE_FACTOR = 0.15625
    SCISSORS_HEIGHT_SCALE_FACTOR = 0.07142857142857142857142857142857
    SCISSORS_BOTTOM_MARGIN = 50

    BINGO_IMAGES_PATH = "assets/Bingo Images"
    SCISSORS_IMAGE_PATH = "assets/scissors/scissors.png"

class TokensLayout:
    GRID_COLS = 9
    GRID_ROWS = 9

    GRID_LINE_COLOR = "#545454"
    GRID_LINE_THICKNESS = 2

    CELL_PADDING_X_RATIO = 0.1
    CELL_PADDING_Y_RATIO = 0.05

    TOKEN_SCALE_FACTOR = 0

    SCISSORS_WIDTH_SCALE_FACTOR = 0.15625
    SCISSORS_HEIGHT_SCALE_FACTOR = 0.07142857142857142857142857142857
    SCISSORS_BOTTOM_MARGIN = 50

    TOKEN_IMAGE_PATH = "assets/Bingo Token/bingotoken.png"
    SCISSORS_IMAGE_PATH = "assets/scissors/Scissors.png"
