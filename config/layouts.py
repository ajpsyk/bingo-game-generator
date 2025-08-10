from dataclasses import dataclass, field

@dataclass
class PageLayout:
    BINGO_IMAGES_PATH: str = field(default="", metadata={"label": "Bingo Images:", "input_type": "directory", "group": "Assets", "section":"", "order": 1, "hidden": False, "spacer_after": False})
    HEADER_IMAGE_PATH: str = field(default="", metadata={"label": "Bingo Header Image:", "input_type": "file", "group": "Assets", "section":"", "order": 2, "hidden": False, "spacer_after": False})
    FRAME_IMAGE_PATH: str = field(default="", metadata={"label": "Frame Image:", "input_type": "file", "group": "Assets", "section":"", "order": 3, "hidden": False, "spacer_after": False})
    FREE_SPACE_IMAGE_PATH: str = field(default="", metadata={"label": "Free Space Image:", "input_type": "file", "group": "Assets", "section":"", "order": 4, "hidden": False, "spacer_after": False})
    CALLING_CARDS_HEADER_IMAGE_PATH: str = field(default="", metadata={"label": "Calling Cards Header:", "input_type": "file", "group": "Assets", "section":"", "order": 5, "hidden": False, "spacer_after": False})
    TOKEN_IMAGE_PATH: str = field(default="", metadata={"label": "Token Image:", "input_type": "file", "group": "Assets", "section":"", "order": 6, "hidden": False, "spacer_after": False})
    OUTPUT_PATH: str = field(default="", metadata={"label": "Output Path:", "input_type": "directory", "group": "Assets", "section":"", "order": 7, "hidden": False, "spacer_after": True})

    INSTRUCTIONS_PATH: str = field(default="", metadata={"label": "Instructions Path:", "input_type": "file", "group": "Assets", "section":"", "order": 8, "hidden": False, "spacer_after": False})
    FONT_PATH: str = field(default="", metadata={"label": "Font Path:", "input_type": "file", "group": "Assets", "section":"", "order": 9, "hidden": False, "spacer_after": False})
    SCISSORS_IMAGE_PATH: str = field(default="", metadata={"label": "Scissors Image Path:", "input_type": "file", "group": "Assets", "section":"", "order": 10, "hidden": False, "spacer_after": True})
    
    THEME: str = field(default="", metadata={"label": "Theme Name:", "input_type": "entry", "group": "Page Layout (in)", "section": "", "order": 1, "hidden": False, "spacer_after": False})
    DPI: int = field(default=300, metadata={"label": "DPI (dots per inch):", "input_type": "entry", "group": "Page Layout (in)", "section": "", "order": 2, "hidden": False, "spacer_after": False})
    WIDTH_INCHES: float = field(default=8.5, metadata={"label": "Width (in):", "input_type": "entry", "group": "Page Layout (in)", "section": "", "order": 3, "hidden": False, "spacer_after": False})
    HEIGHT_INCHES: float = field(default=11.0, metadata={"label": "Height (in):", "input_type": "entry", "group": "Page Layout (in)", "section": "", "order": 4, "hidden": False, "spacer_after": True})
    
    MARGIN_TOP_INCHES: float = field(default=0.3, metadata={"label": "Margin Top (in):", "input_type": "entry", "group": "Page Layout (in)", "section": "Margin", "order": 5, "hidden": False, "spacer_after": False})
    MARGIN_RIGHT_INCHES: float = field(default=0.3, metadata={"label": "Margin Right (in):", "input_type": "entry", "group": "Page Layout (in)", "section": "Margin", "order": 6, "hidden": False, "spacer_after": False})
    MARGIN_BOTTOM_INCHES: float = field(default=0.3, metadata={"label": "Margin Bottom (in):", "input_type": "entry", "group": "Page Layout (in)", "section": "Margin", "order": 7, "hidden": False, "spacer_after": False})
    MARGIN_LEFT_INCHES: float = field(default=0.3, metadata={"label": "Margin Left (in):", "input_type": "entry", "group": "Page Layout (in)", "section": "Margin", "order": 8, "hidden": False, "spacer_after": False})


@dataclass
class BingoCardLayout:
    HAS_FREE_SPACE = True
    GRID_LINE_COLOR: str = field(default="#7d6055", metadata={"label": "Grid Line Color:", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 1, "hidden": False, "spacer_after": False})
    LABEL_COLOR: str = field(default="#6b3f3f", metadata={"label": "Label Color:", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 2, "hidden": False, "spacer_after": False})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.023, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 3, "hidden": False, "spacer_after": False})
    GRID_MARGIN_TOP_INCHES: float = field(default=0.1, metadata={"label": "Grid Margin Top (in):", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 4, "hidden": False, "spacer_after": True})

    LABEL_HEIGHT_RATIO: float = field(default=0.14, metadata={"label": "Label Height Ratio:", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 5, "hidden": False, "spacer_after": False})
    LABEL_GAP_RATIO: float = field(default=0.3, metadata={"label": "Label Gap Ratio:", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 6, "hidden": False, "spacer_after": False})
    CELL_PADDING_X_RATIO: float = field(default=0.1, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 7, "hidden": False, "spacer_after": False})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 8, "hidden": False, "spacer_after": True})

    FRAME_PADDING_TOP_INCHES: float = field(default=0.45, metadata={"label": "Frame Padding Top (in):", "input_type": "entry","group": "Single Card", "section":"Frame Padding", "order": 9, "hidden": False, "spacer_after": False})
    FRAME_PADDING_RIGHT_INCHES: float = field(default=0.45, metadata={"label": "Frame Padding Right (in):", "input_type": "entry","group": "Single Card", "section":"Frame Padding", "order": 10, "hidden": False, "spacer_after": False})
    FRAME_PADDING_BOTTOM_INCHES: float = field(default=0.45, metadata={"label": "Frame Padding Bottom (in):", "input_type": "entry","group": "Single Card", "section":"Frame Padding", "order": 11, "hidden": False, "spacer_after": False})
    FRAME_PADDING_LEFT_INCHES: float = field(default=0.45, metadata={"label": "Frame Padding Left (in):", "input_type": "entry","group": "Single Card", "section":"Frame Padding", "order": 12, "hidden": False, "spacer_after": True})

    CARD_AMOUNT: int = field(default=50, metadata={"label": "Card Amount:", "input_type": "entry","group": "Single Card", "section":"Card Quantity Output", "order": 13, "hidden": False, "spacer_after": False})
    NUM_PDFS: int = field(default=2, metadata={"label": "Number of PDFs:", "input_type": "entry","group": "Single Card", "section":"Card Quantity Output", "order": 14, "hidden": False, "spacer_after": False})
    FILE_NAME: str = field(default="1PerPage", metadata={"label": "File Name:", "input_type": "entry","group": "Single Card", "section":"Card Quantity Output", "order": 15, "hidden": False, "spacer_after": True})

    FRAME_ENABLED: bool = field(default=True, metadata={"label": "Frame Enabled:", "input_type": "checkbox","group": "Single Card", "section":"Card Quantity Output", "order": 16, "hidden": False, "spacer_after": False})

    GRID_COLS: int = field(default=5, metadata={"label": "Grid Columns:", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})
    GRID_ROWS: int = field(default=5, metadata={"label": "Grid Rows:", "input_type": "entry","group": "Single Card", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})
    
    

@dataclass
class BingoCardMultiLayout:
    HAS_FREE_SPACE = True
    GRID_LINE_COLOR: str = field(default="#7d6055", metadata={"label": "Grid Line Color:", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 1, "hidden": False, "spacer_after": False})
    LABEL_COLOR: str = field(default="#6b3f3f", metadata={"label": "Label Color:", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 2, "hidden": False, "spacer_after": False})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.01, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 3, "hidden": False, "spacer_after": False})
    GRID_MARGIN_TOP_INCHES: float = field(default=0.1, metadata={"label": "Grid Margin Top (in):", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 4, "hidden": False, "spacer_after": True})

    LABEL_HEIGHT_RATIO: float = field(default=0.14, metadata={"label": "Label Height Ratio:", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 5, "hidden": False, "spacer_after": False})
    LABEL_GAP_RATIO: float = field(default=0.3, metadata={"label": "Label Gap Ratio:", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 6, "hidden": False, "spacer_after": False})
    CELL_PADDING_X_RATIO: float = field(default=0.1, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 7, "hidden": False, "spacer_after": False})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 8, "hidden": False, "spacer_after": True})

    FRAME_PADDING_TOP_INCHES: float = field(default=0.3, metadata={"label": "Frame Padding Top (in):", "input_type": "entry","group": "Double Card", "section":"Frame Padding", "order": 9, "hidden": False, "spacer_after": False})
    FRAME_PADDING_RIGHT_INCHES: float = field(default=0.333, metadata={"label": "Frame Padding Right (in):", "input_type": "entry","group": "Double Card", "section":"Frame Padding", "order": 10, "hidden": False, "spacer_after": False})
    FRAME_PADDING_BOTTOM_INCHES: float = field(default=0.333, metadata={"label": "Frame Padding Bottom (in):", "input_type": "entry","group": "Double Card", "section":"Frame Padding", "order": 11, "hidden": False, "spacer_after": False})
    FRAME_PADDING_LEFT_INCHES: float = field(default=0.333, metadata={"label": "Frame Padding Left (in):", "input_type": "entry","group": "Double Card", "section":"Frame Padding", "order": 12, "hidden": False, "spacer_after": True})

    CARD_AMOUNT: int = field(default=50, metadata={"label": "Card Amount:", "input_type": "entry","group": "Double Card", "section":"Card Quantity Output", "order": 13, "hidden": False, "spacer_after": False})
    NUM_PDFS: int = field(default=1, metadata={"label": "Number of PDFs:", "input_type": "entry","group": "Double Card", "section":"Card Quantity Output", "order": 14, "hidden": False, "spacer_after": False})
    FILE_NAME: str = field(default="", metadata={"label": "File Name:", "input_type": "entry","group": "Double Card", "section":"Card Quantity Output", "order": 15, "hidden": False, "spacer_after": True})

    FRAME_ENABLED: bool = field(default=True, metadata={"label": "Frame Enabled:", "input_type": "checkbox","group": "Double Card", "section":"Card Quantity Output", "order": 16, "hidden": False, "spacer_after": False})

    GRID_COLS: int = field(default=5, metadata={"label": "Grid Columns:", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})
    GRID_ROWS: int = field(default=5, metadata={"label": "Grid Rows:", "input_type": "entry","group": "Double Card", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})


@dataclass
class TokensLayout:
    HAS_FREE_SPACE: bool = field(default=False, metadata={"hidden": True})
    GRID_COLS: int = field(default=9, metadata={"label": "Grid Columns:", "input_type": "entry"})
    GRID_ROWS: int = field(default=9, metadata={"label": "Grid Rows:", "input_type": "entry"})

    SCISSORS_WIDTH_SCALE_FACTOR: float = field(default=0.15625, metadata={"label": "Scissors Width Scale Factor:", "input_type": "entry"})
    SCISSORS_HEIGHT_SCALE_FACTOR: float = field(default=0.07142857142857143, metadata={"label": "Scissors Height Scale Factor:", "input_type": "entry"})
    SCISSORS_BOTTOM_MARGIN_INCHES: float = field(default=0.167, metadata={"label": "Scissors Bottom Margin (in):", "input_type": "entry"})

    GRID_LINE_COLOR: str = field(default="#545454", metadata={"label": "Grid Line Color:", "input_type": "entry"})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.007, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry"})

    CELL_PADDING_X_RATIO: float = field(default=0.1, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry"})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry"})

    FILE_NAME: str = field(default="Tokens", metadata={"hidden": True})
    SCISSORS_IMAGE_PATH: str = field(default="", metadata={"label": "Scissors Image Path:", "input_type": "file"})
    OUTPUT_PATH: str = field(default="", metadata={"label": "Output Path:", "input_type": "directory"})

@dataclass
class CallingCardsSinglePageLayout:
    HAS_FREE_SPACE: bool = field(default=False, metadata={"hidden": True})
    GRID_LINE_COLOR: str = field(default="#7d6055", metadata={"label": "Grid Line Color:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 1, "hidden": False, "spacer_after": False})
    LABEL_COLOR: str = field(default="#6b3f3f", metadata={"label": "Label Color:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 2, "hidden": False, "spacer_after": False})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.007, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 3, "hidden": False, "spacer_after": False})
    GRID_MARGIN_TOP_INCHES: float = field(default=0.15, metadata={"label": "Grid Margin Top (in):", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 4, "hidden": False, "spacer_after": False})

    CELL_PADDING_X_RATIO: float = field(default=0.2, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 5, "hidden": False, "spacer_after": False})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 6, "hidden": False, "spacer_after": False})
    LABEL_HEIGHT_RATIO: float = field(default=0.14, metadata={"label": "Label Height Ratio:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 7, "hidden": False, "spacer_after": False})
    LABEL_GAP_RATIO: float = field(default=0.3, metadata={"label": "Label Gap Ratio:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 8, "hidden": False, "spacer_after": False})


    NUM_PDFS: int = field(default=1, metadata={"label": "Number of PDFs:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})

    GRID_COLS: int = field(default=5, metadata={"label": "Grid Columns:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})
    GRID_ROWS: int = field(default=6, metadata={"label": "Grid Rows:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})
    FILE_NAME: str = field(default="Calling_Cards_Single", metadata={"hidden": True})
    FRAME_ENABLED: bool = field(default=False, metadata={"label": "Frame Enabled:", "input_type": "checkbox","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})

@dataclass
class CallingCardsMultiPageLayout:
    HAS_FREE_SPACE: bool = field(default=False, metadata={"hidden": True})
    GRID_LINE_COLOR: str = field(default="#7d6055", metadata={"label": "Grid Line Color:", "input_type": "entry","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 1, "hidden": False, "spacer_after": False})
    LABEL_COLOR: str = field(default="#6b3f3f", metadata={"label": "Label Color:", "input_type": "entry","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 2, "hidden": False, "spacer_after": False})
    GRID_LINE_THICKNESS_INCHES: float = field(default=0.007, metadata={"label": "Grid Line Thickness (in):", "input_type": "entry","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 3, "hidden": False, "spacer_after": False})
    GRID_MARGIN_TOP_INCHES: float = field(default=0.167, metadata={"label": "Grid Margin Top (in):", "input_type": "entry","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 4, "hidden": False, "spacer_after": False})

    CELL_PADDING_X_RATIO: float = field(default=0.1, metadata={"label": "Cell Padding X Ratio:", "input_type": "entry","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 5, "hidden": False, "spacer_after": False})
    CELL_PADDING_Y_RATIO: float = field(default=0.05, metadata={"label": "Cell Padding Y Ratio:", "input_type": "entry","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 6, "hidden": False, "spacer_after": False})

    LABEL_HEIGHT_RATIO: float = field(default=0.14, metadata={"label": "Label Height Ratio:", "input_type": "entry","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 7, "hidden": False, "spacer_after": False})
    LABEL_GAP_RATIO: float = field(default=0.3, metadata={"label": "Label Gap Ratio:", "input_type": "entry","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 8, "hidden": False, "spacer_after": False})

    CARD_AMOUNT: int = field(default=1, metadata={"label": "Card Amount:", "input_type": "entry","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 9, "hidden": True, "spacer_after": False})

    FRAME_ENABLED: bool = field(default=False, metadata={"label": "Frame Enabled:", "input_type": "checkbox","group": "Calling Cards Multi Page (big)", "section":"Grid", "order": 10, "hidden": True, "spacer_after": False})

    SCISSORS_WIDTH_SCALE_FACTOR: float = field(default=0.15625, metadata={"label": "Scissors Width Scale Factor:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})
    SCISSORS_HEIGHT_SCALE_FACTOR: float = field(default=0.07142857142857143, metadata={"label": "Scissors Height Scale Factor:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})
    FILE_NAME: str = field(default="Calling_Cards_Multi", metadata={"hidden": True})
    GRID_COLS: int = field(default=2, metadata={"label": "Grid Columns:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})
    GRID_ROWS: int = field(default=2, metadata={"label": "Grid Rows:", "input_type": "entry","group": "Calling Cards Single Page (small)", "section":"Grid", "order": 1, "hidden": True, "spacer_after": False})
