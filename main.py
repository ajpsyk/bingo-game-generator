import os
import random
from PIL import Image, ImageDraw, ImageFont

# globals
DPI = 150
PAGE_WIDTH = int(8.5 * DPI)
PAGE_HEIGHT = int(11 * DPI)
TOP_MARGIN = int(0.125 * DPI)
BOTTOM_MARGIN = int(0.25 * DPI)
SIDE_MARGIN = int(0.25 * DPI)
MARGIN = int(0.25 * DPI)
USABLE_WIDTH = PAGE_WIDTH - 2 * SIDE_MARGIN
USABLE_HEIGHT = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
VERTICAL_SPACING = int(0.125 * DPI)
FONT = "fonts/Dekko-Regular.ttf"
LINE_COLOR = "#545454"
LINE_THICKNESS = 2
image_folder = "Images/"

# calling cards (single page)

# todo: needs to be determined by user input
# header
header = Image.open("header\Calling_Card_Header.png").convert("RGBA")
header_width, header_height = header.size

if header_width > USABLE_WIDTH:
    scale_factor = USABLE_WIDTH / header_width
    header_height = int(header_height * scale_factor)
    header_width = int(header_width * scale_factor)
    header = header.resize((header_width, header_height), Image.LANCZOS)

HEADER_X =  SIDE_MARGIN + (USABLE_WIDTH - header_width) // 2
HEADER_Y = TOP_MARGIN

# grid dimensions
GRID_WIDTH = USABLE_WIDTH
GRID_HEIGHT = USABLE_HEIGHT - header_height - VERTICAL_SPACING
GRID_X = SIDE_MARGIN
GRID_Y = HEADER_Y + header_height + VERTICAL_SPACING
COLS = 5
ROWS = 6

CELL_WIDTH = GRID_WIDTH // COLS
CELL_HEIGHT = GRID_HEIGHT // ROWS 


canvas = Image.new("RGBA", (PAGE_WIDTH, PAGE_HEIGHT), (255, 255, 255, 255))
draw = ImageDraw.Draw(canvas)
canvas.paste(header, (HEADER_X, HEADER_Y), header)


# Draw grid lines
# Horizontal dashed lines
for i in range(ROWS + 1):
    y = GRID_Y + i * CELL_HEIGHT
    draw.line([(GRID_X, y), (GRID_X + GRID_WIDTH, y)], fill=LINE_COLOR, width=2)
    
top_y = GRID_Y
bottom_y = GRID_Y + ROWS * CELL_HEIGHT

# Vertical dashed lines
for j in range(COLS + 1):
    x = GRID_X + j * CELL_WIDTH
    draw.line([(x, top_y), (x, bottom_y)], fill=LINE_COLOR, width=2)

image_files = [
    f for f in os.listdir(image_folder)
    if f.lower().endswith(".png")
]

random.shuffle(image_files)

assert len(image_files) == 30, "Expected exactly 30 images"


# cell content
LABEL_HEIGHT = int(CELL_HEIGHT * 0.14)
GAP = int(LABEL_HEIGHT * 0.3)
PADDING_Y = int(CELL_HEIGHT * 0.05)  # equal top/bottom margin

available_img_height = CELL_HEIGHT - 2 * PADDING_Y - GAP - LABEL_HEIGHT
available_img_width = CELL_WIDTH - int(CELL_WIDTH * 0.1)

font_size = int(LABEL_HEIGHT * 1)
font = ImageFont.truetype("fonts/Dekko-Regular.ttf", size=font_size)

for idx, image_file in enumerate(image_files):
    row = idx // COLS
    col = idx % COLS

    x0 = GRID_X + col * CELL_WIDTH
    y0 = GRID_Y + row * CELL_HEIGHT

    img_path = os.path.join(image_folder, image_file)
    img = Image.open(img_path).convert("RGBA")

    # Resize to fit inside allowed area
    img.thumbnail((available_img_width, available_img_height), Image.LANCZOS)

    # Center image in X, top-aligned in drawable area
    img_x = x0 + (CELL_WIDTH - img.width) // 2
    img_y = y0 + PADDING_Y
    canvas.paste(img, (img_x, img_y), img)

    # Prepare label
    label = os.path.splitext(image_file)[0].replace("_", " ").upper()
    bbox = font.getbbox(label)
    text_width = bbox[2] - bbox[0]

    text_x = x0 + (CELL_WIDTH - text_width) // 2
    text_y = img_y + img.height + GAP

    draw.text((text_x, text_y), label, font=font, fill="black")

canvas.save("output/preview_grid.pdf", "PDF", dpi=(DPI, DPI))
print("Grid layout saved to output/preview_grid.pdf")

        # grid lines // dashed or solid, thickness, and color
        # grid space // cell spacing is 14.241
            # the bingo images // 5/6 of the height
            # the image names // 1/6 of the height

# cut and shuffle calling card pages

# large bingo card tokens

# small bingo card tokens

# big bingo cards

# small bingo cards

# stretch goal - marketing images