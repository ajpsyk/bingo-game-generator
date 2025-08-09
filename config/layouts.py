from dataclasses import dataclass, field

@dataclass
class PageLayout:
    DPI: int = field(default=300, metadata={"label": "DPI (dots per inch):", "input_type": "entry"})

    WIDTH_INCHES: float = field(default=8.5, metadata={"label": "Width (in):", "input_type": "entry"})
    HEIGHT_INCHES: float = field(default=11.0, metadata={"label": "Height (in):", "input_type": "entry"})
    
    MARGIN_TOP_INCHES: float = field(default=0.3, metadata={"label": "Margin Top (in):", "input_type": "entry"})
    MARGIN_RIGHT_INCHES: float = field(default=0.3, metadata={"label": "Margin Right (in):", "input_type": "entry"})
    MARGIN_BOTTOM_INCHES: float = field(default=0.3, metadata={"label": "Margin Bottom (in):", "input_type": "entry"})
    MARGIN_LEFT_INCHES: float = field(default=0.3, metadata={"label": "Margin Left (in):", "input_type": "entry"})
    
    FONT_PATH: str = field(default="", metadata={"label": "Font Path:", "input_type": "file"})
    TOKENS_PAGE: str = field(default="", metadata={"label": "Tokens File Path:", "input_type": "file"})
    CALLING_CARDS_SINGLE_PAGE: str = field(default="", metadata={"label": "Calling Cards File Path:", "input_type": "file"})
    CALLING_CARDS_MULTI_PAGE: str = field(default="", metadata={"label": "Calling Cards Multi Path:", "input_type": "file"})
    INSTRUCTIONS_PATH: str = field(default="", metadata={"label": "Instructions Path:", "input_type": "file"})
    OUTPUT_PATH: str = field(default="", metadata={"label": "Output Path:", "input_type": "directory"})

@dataclass
class BingoCardLayout:
    CARD_AMOUNT: int = field(default=50, metadata={"label": "Card Amount:", "input_type": "entry"})
    NUM_PDFS: int = field(default=2, metadata={"label": "Number of PDFs:", "input_type": "entry"})

    FRAME_ENABLED: bool = field(default=True, metadata={"label": "Frame Enabled:", "input_type": "checkbox"})
    FRAME_PADDING_TOP_INCHES: float = field(default=0.45, metadata={"label": "Frame Padding Top (in):", "input_type": "entry"})
    FRAME_PADDING_RIGHT_INCHES: float = field(default=0.45, metadata={"label": "Frame Padding Right (in):", "input_type": "entry"})
    FRAME_PADDING_BOTTOM_INCHES: float = field(default=0.45, metadata={"label": "Frame Padding Bottom (in):", "input_type": "entry"})
    FRAME_PADDING_LEFT_INCHES: float = field(default=0.45, metadata={"label": "Frame Padding Left (in):", "input_type": "entry"})

    GRID_COLS: int = field(default=5, metadata={"label": "Grid Columns:", "input_type": "entry"})
    GRID_ROWS: int = field(default=5, metadata={"label": "Grid Rows:", "input_type": "entry"})
    GRID_MARGIN_TOP_INCHES: float = field(default=0.1, metadata={"label": "Grid Margin Top (in):", "input_type": "entry"})
    GRID_LINE_COLOR: str = field(default="#7d6055", metadata={"label": "Grid Line Color:", "input_type": "entry"})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.023, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry"})

    CELL_PADDING_X_RATIO: float = field(default=0.1, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry"})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry"})

    LABEL_COLOR: str = field(default="#6b3f3f", metadata={"label": "Label Color:", "input_type": "entry"})
    LABEL_HEIGHT_RATIO: float = field(default=0.14, metadata={"label": "Label Height Ratio:", "input_type": "entry"})
    LABEL_GAP_RATIO: float = field(default=0.3, metadata={"label": "Label Gap Ratio:", "input_type": "entry"})

    BINGO_IMAGES_PATH: str = field(default="", metadata={"label": "Bingo Images Path:", "input_type": "directory"})
    HEADER_IMAGE_PATH: str = field(default="", metadata={"label": "Header Image Path:", "input_type": "file"})
    FRAME_IMAGE_PATH: str = field(default="", metadata={"label": "Frame Image Path:", "input_type": "file"})
    FREE_SPACE_IMAGE_PATH: str = field(default="", metadata={"label": "Free Space Image Path:", "input_type": "file"})
    OUTPUT_PATH: str = field(default="", metadata={"label": "Output Path:", "input_type": "directory"})

@dataclass
class BingoCardMultiLayout:
    CARD_AMOUNT: int = field(default=50, metadata={"label": "Card Amount:", "input_type": "entry"})
    NUM_PDFS: int = field(default=1, metadata={"label": "Number of PDFs:", "input_type": "entry"})

    FRAME_ENABLED: bool = field(default=True, metadata={"label": "Frame Enabled:", "input_type": "checkbox"})
    FRAME_PADDING_TOP_INCHES: float = field(default=0.3, metadata={"label": "Frame Padding Top (in):", "input_type": "entry"})
    FRAME_PADDING_RIGHT_INCHES: float = field(default=0.333, metadata={"label": "Frame Padding Right (in):", "input_type": "entry"})
    FRAME_PADDING_BOTTOM_INCHES: float = field(default=0.333, metadata={"label": "Frame Padding Bottom (in):", "input_type": "entry"})
    FRAME_PADDING_LEFT_INCHES: float = field(default=0.333, metadata={"label": "Frame Padding Left (in):", "input_type": "entry"})

    GRID_MARGIN_TOP_INCHES: float = field(default=0.1, metadata={"label": "Grid Margin Top (in):", "input_type": "entry"})
    GRID_COLS: int = field(default=5, metadata={"label": "Grid Columns:", "input_type": "entry"})
    GRID_ROWS: int = field(default=5, metadata={"label": "Grid Rows:", "input_type": "entry"})
    GRID_LINE_COLOR: str = field(default="#7d6055", metadata={"label": "Grid Line Color:", "input_type": "entry"})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.01, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry"})

    CELL_PADDING_X_RATIO: float = field(default=0.1, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry"})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry"})

    LABEL_COLOR: str = field(default="#6b3f3f", metadata={"label": "Label Color:", "input_type": "entry"})
    LABEL_HEIGHT_RATIO: float = field(default=0.14, metadata={"label": "Label Height Ratio:", "input_type": "entry"})
    LABEL_GAP_RATIO: float = field(default=0.3, metadata={"label": "Label Gap Ratio:", "input_type": "entry"})
    LABEL_FONT_SCALE: float = field(default=1.0, metadata={"label": "Label Font Scale:", "input_type": "entry"})

    BINGO_IMAGES_PATH: str = field(default="", metadata={"label": "Bingo Images Path:", "input_type": "directory"})
    HEADER_IMAGE_PATH: str = field(default="", metadata={"label": "Header Image Path:", "input_type": "file"})
    FRAME_IMAGE_PATH: str = field(default="", metadata={"label": "Frame Image Path:", "input_type": "file"})
    FREE_SPACE_IMAGE_PATH: str = field(default="", metadata={"label": "Free Space Image Path:", "input_type": "file"})
    OUTPUT_PATH: str = field(default="", metadata={"label": "Output Path:", "input_type": "directory"})

@dataclass
class TokensLayout:
    GRID_COLS: int = field(default=9, metadata={"label": "Grid Columns:", "input_type": "entry"})
    GRID_ROWS: int = field(default=9, metadata={"label": "Grid Rows:", "input_type": "entry"})

    SCISSORS_WIDTH_SCALE_FACTOR: float = field(default=0.15625, metadata={"label": "Scissors Width Scale Factor:", "input_type": "entry"})
    SCISSORS_HEIGHT_SCALE_FACTOR: float = field(default=0.07142857142857143, metadata={"label": "Scissors Height Scale Factor:", "input_type": "entry"})
    SCISSORS_BOTTOM_MARGIN_INCHES: float = field(default=0.167, metadata={"label": "Scissors Bottom Margin (in):", "input_type": "entry"})

    GRID_LINE_COLOR: str = field(default="#545454", metadata={"label": "Grid Line Color:", "input_type": "entry"})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.007, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry"})

    CELL_PADDING_X_RATIO: float = field(default=0.1, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry"})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry"})

    TOKEN_IMAGE_PATH: str = field(default="", metadata={"label": "Token Image Path:", "input_type": "file"})
    SCISSORS_IMAGE_PATH: str = field(default="", metadata={"label": "Scissors Image Path:", "input_type": "file"})
    OUTPUT_PATH: str = field(default="", metadata={"label": "Output Path:", "input_type": "directory"})

@dataclass
class CallingCardsSinglePageLayout:
    NUM_PDFS: int = field(default=1, metadata={"label": "Number of PDFs:", "input_type": "entry"})

    GRID_COLS: int = field(default=5, metadata={"label": "Grid Columns:", "input_type": "entry"})
    GRID_ROWS: int = field(default=6, metadata={"label": "Grid Rows:", "input_type": "entry"})

    FRAME_ENABLED: bool = field(default=False, metadata={"label": "Frame Enabled:", "input_type": "checkbox"})

    GRID_LINE_COLOR: str = field(default="#7d6055", metadata={"label": "Grid Line Color:", "input_type": "entry"})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.007, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry"})

    GRID_MARGIN_TOP_INCHES: float = field(default=0.15, metadata={"label": "Grid Margin Top (in):", "input_type": "entry"})

    CELL_PADDING_X_RATIO: float = field(default=0.2, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry"})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry"})

    LABEL_COLOR: str = field(default="#6b3f3f", metadata={"label": "Label Color:", "input_type": "entry"})
    LABEL_HEIGHT_RATIO: float = field(default=0.14, metadata={"label": "Label Height Ratio:", "input_type": "entry"})
    LABEL_GAP_RATIO: float = field(default=0.3, metadata={"label": "Label Gap Ratio:", "input_type": "entry"})

    BINGO_IMAGES_PATH: str = field(default="", metadata={"label": "Bingo Images Path:", "input_type": "directory"})
    HEADER_IMAGE_PATH: str = field(default="", metadata={"label": "Header Image Path:", "input_type": "file"})
    OUTPUT_PATH: str = field(default="", metadata={"label": "Output Path:", "input_type": "directory"})

@dataclass
class CallingCardsMultiPageLayout:
    CARD_AMOUNT: int = field(default=1, metadata={"label": "Card Amount:", "input_type": "entry"})

    FRAME_ENABLED: bool = field(default=False, metadata={"label": "Frame Enabled:", "input_type": "checkbox"})

    SCISSORS_WIDTH_SCALE_FACTOR: float = field(default=0.15625, metadata={"label": "Scissors Width Scale Factor:", "input_type": "entry"})
    SCISSORS_HEIGHT_SCALE_FACTOR: float = field(default=0.07142857142857143, metadata={"label": "Scissors Height Scale Factor:", "input_type": "entry"})

    GRID_COLS: int = field(default=2, metadata={"label": "Grid Columns:", "input_type": "entry"})
    GRID_ROWS: int = field(default=2, metadata={"label": "Grid Rows:", "input_type": "entry"})

    GRID_LINE_COLOR: str = field(default="#7d6055", metadata={"label": "Grid Line Color:", "input_type": "entry"})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.007, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry"})
    GRID_MARGIN_TOP_INCHES: float = field(default=0.167, metadata={"label": "Grid Margin Top (in):", "input_type": "entry"})

    CELL_PADDING_X_RATIO: float = field(default=0.1, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry"})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry"})

    LABEL_COLOR: str = field(default="#6b3f3f", metadata={"label": "Label Color:", "input_type": "entry"})
    LABEL_HEIGHT_RATIO: float = field(default=0.14, metadata={"label": "Label Height Ratio:", "input_type": "entry"})
    LABEL_GAP_RATIO: float = field(default=0.3, metadata={"label": "Label Gap Ratio:", "input_type": "entry"})

    BINGO_IMAGES_PATH: str = field(default="", metadata={"label": "Bingo Images Path:", "input_type": "directory"})
    SCISSORS_IMAGE_PATH: str = field(default="", metadata={"label": "Scissors Image Path:", "input_type": "file"})
    OUTPUT_PATH: str = field(default="", metadata={"label": "Output Path:", "input_type": "directory"})
