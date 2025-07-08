class PageLayout:
    DPI = 300
    PAGE_WIDTH_INCHES = 8.5
    PAGE_HEIGHT_INCHES = 11
    PAGE_WIDTH_PIXELS = int(PAGE_WIDTH_INCHES * DPI)
    PAGE_HEIGHT_PIXELS = int(PAGE_HEIGHT_INCHES * DPI)
    PAGE_MARGIN = int(0.5 * DPI)

    FONT_PATH = "fonts/Dekko-Regular.ttf"
    DEFAULT_OUTPUT_PATH = "output/preview_grid.pdf"


class BingoCardLayout:
    GRID_COLS = 5
    GRID_ROWS = 5

    GRID_LINE_COLOR = "#69622c"
    GRID_LINE_THICKNESS = 2

    LABEL_COLOR = "#581a4d"

    LABEL_HEIGHT_RATIO = 0.14
    LABEL_GAP_RATIO = 0.3
    CELL_PADDING_Y_RATIO = 0.05
    LABEL_FONT_SCALE = 1.0

    BINGO_IMAGES_PATH = "Images/Bingo Images"
    HEADER_IMAGE_PATH = "Images/header/Bingo_Card_Header.png"
    FRAME_IMAGE_PATH = "Images/frame/Halloween_Border.png"
    FREE_SPACE_IMAGE_PATH = "Images/Free Space/Free_Space.png"


class CallingCardsSinglePageLayout:
    GRID_COLS = 5
    GRID_ROWS = 6

    GRID_LINE_COLOR = "#545454"
    GRID_LINE_THICKNESS = 2

    LABEL_HEIGHT_RATIO = 0.14
    LABEL_GAP_RATIO = 0.3
    CELL_PADDING_Y_RATIO = 0.05
    LABEL_FONT_SCALE = 1.0

    BINGO_IMAGES_PATH = "Images/Bingo Images"
    HEADER_IMAGE_PATH = "Images/header/Calling_Card_Header.png"


class CallingCardsMultiPageLayout:
    GRID_COLS = 2
    GRID_ROWS = 2
    BINGO_IMAGES_PATH = "Images/Bingo Images"
    SCISSORS_IMAGE_PATH = "Images/scissors/scissors.png"


class TokensLargeLayout:
    GRID_COLS = 5
    GRID_ROWS = 5
    TOKEN_IMAGE_PATH = "Images/Bingo Token/bingotoken.png"
    SCISSORS_IMAGE_PATH = "Images/scissors/scissors.png"


class TokensSmallLayout:
    GRID_COLS = 10
    GRID_ROWS = 10
    TOKEN_IMAGE_PATH = "Images/Bingo Token/bingotoken.png"
    SCISSORS_IMAGE_PATH = "Images/scissors/scissors.png"
