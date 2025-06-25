import os
import random
from PIL import Image, ImageDraw, ImageFont
from config import (
    DPI, PAGE_WIDTH, PAGE_HEIGHT,
    TOP_MARGIN, BOTTOM_MARGIN, SIDE_MARGIN,
    FONT_PATH
)

# Page-specific constants
COLS = 5
ROWS = 5

LINE_COLOR = "#69622c"
LINE_THICKNESS = 2

LABEL_HEIGHT_RATIO = 0.14
LABEL_GAP_RATIO = 0.3
CELL_PADDING_Y_RATIO = 0.05
LABEL_FONT_SCALE = 1.0

HEADER_IMAGE_PATH = "header/Bingo_Card_Header.png"
FRAME_IMAGE_PATH = "frame/Halloween_Border.png"
FREE_SPACE_IMAGE_PATH = "Images/Free Space/Free_Space.png"

LABEL_COLOR = "#581a4d"


def load_header(path, usable_width):
    header = Image.open(path).convert("RGBA")
    header_width, header_height = header.size

    if header_width > usable_width:
        scale_factor = usable_width / header_width
        header_width = int(header_width * scale_factor)
        header_height = int(header_height * scale_factor)
        header = header.resize((header_width, header_height), Image.LANCZOS)

    return header, header_width, header_height


def draw_grid(draw, x, y, cols, rows, cell_width, cell_height, line_color, line_thickness):
    for i in range(rows + 1):
        y_line = y + i * cell_height
        draw.line([(x, y_line), (x + cols * cell_width, y_line)], fill=line_color, width=line_thickness)
    for j in range(cols + 1):
        x_line = x + j * cell_width
        draw.line([(x_line, y), (x_line, y + rows * cell_height)], fill=line_color, width=line_thickness)


def draw_text_with_spacing(draw, text, font, fill, position, spacing):
    x, y = position
    for char in text:
        draw.text((x, y), char, font=font, fill=fill)
        bbox = font.getbbox(char)
        char_width = bbox[2] - bbox[0]
        x += char_width + spacing


def get_frame_thickness_from_alpha(image):
    
    width, height = image.size
    pixels = image.load()
    
    mid_x = width // 2
    mid_y = height // 2
    
    def scan_top():
        for y in range(height):
            alpha = pixels[mid_x, y][3]
            if alpha == 0:
                return y
        return 0  # No transparent pixel found
    
    def scan_bottom():
        for y in reversed(range(height)):
            alpha = pixels[mid_x, y][3]
            if alpha == 0:
                return height - y - 1
        return 0
    
    def scan_left():
        for x in range(width):
            alpha = pixels[x, mid_y][3]
            if alpha == 0:
                return x
        return 0
    
    def scan_right():
        for x in reversed(range(width)):
            alpha = pixels[x, mid_y][3]
            if alpha == 0:
                return width - x - 1
        return 0
    
    top = scan_top()
    bottom = scan_bottom()
    left = scan_left()
    right = scan_right()
    
    return {
        "top": top,
        "bottom": bottom,
        "left": left,
        "right": right
    }


def generate_bingo_cards_big(image_folder, output_path):
    frame_padding = {"top": 0, "bottom": 0, "left": 0, "right": 0}
    frame = Image.open(FRAME_IMAGE_PATH).convert("RGBA").resize((PAGE_WIDTH, PAGE_HEIGHT), Image.LANCZOS)
    if os.path.isfile(FRAME_IMAGE_PATH):
        frame_padding = get_frame_thickness_from_alpha(frame)

    left_margin = SIDE_MARGIN + frame_padding["left"]
    right_margin = SIDE_MARGIN + frame_padding["right"]
    top_margin = TOP_MARGIN + frame_padding["top"]
    bottom_margin = BOTTOM_MARGIN + frame_padding["bottom"]

    usable_width = PAGE_WIDTH - left_margin - right_margin
    usable_height = PAGE_HEIGHT - top_margin - bottom_margin

    header, header_width, header_height = load_header(HEADER_IMAGE_PATH, usable_width)

    header_x = left_margin
    header_y = top_margin

    grid_x = left_margin
    grid_y = header_y + header_height
    grid_height = usable_height - header_height
    cell_width = usable_width // COLS
    cell_height = grid_height // ROWS

    canvas = Image.new("RGBA", (PAGE_WIDTH, PAGE_HEIGHT), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    canvas.paste(frame, (0, 0), frame)

    canvas.paste(header, (header_x, header_y), header)

    draw_grid(draw, grid_x, grid_y, COLS, ROWS, cell_width, cell_height, LINE_COLOR, LINE_THICKNESS)

    # Optional: Draw debug box for content bounds
    # draw.rectangle([(left_margin, top_margin), (PAGE_WIDTH - right_margin, PAGE_HEIGHT - bottom_margin)],
    #                outline="red", width=3)

    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(".png")]
    random.shuffle(image_files)

    assert len(image_files) >= 24, "Need at least 24 images for big bingo card"
    image_files = image_files[:24]

    label_height = int(cell_height * LABEL_HEIGHT_RATIO)
    gap = int(label_height * LABEL_GAP_RATIO)
    padding_y = int(cell_height * CELL_PADDING_Y_RATIO)

    available_img_height = cell_height - 2 * padding_y - gap - label_height
    available_img_width = cell_width - int(cell_width * 0.1)

    font_size = int(label_height * LABEL_FONT_SCALE)
    font = ImageFont.truetype(FONT_PATH, size=font_size)

    free_img = Image.open(FREE_SPACE_IMAGE_PATH).convert("RGBA")

    image_idx = 0
    for idx in range(COLS * ROWS):
        row = idx // COLS
        col = idx % COLS
        x0 = grid_x + col * cell_width
        y0 = grid_y + row * cell_height

        if row == 2 and col == 2:
            free_img_copy = free_img.copy()
            free_img_copy.thumbnail((available_img_width, available_img_height), Image.LANCZOS)
            img_x = x0 + (cell_width - free_img_copy.width) // 2
            img_y = y0 + (cell_height - free_img_copy.height) // 2
            canvas.paste(free_img_copy, (img_x, img_y), free_img_copy)
        else:
            image_file = image_files[image_idx]
            image_idx += 1

            img_path = os.path.join(image_folder, image_file)
            img = Image.open(img_path).convert("RGBA")
            img.thumbnail((available_img_width, available_img_height), Image.LANCZOS)

            img_x = x0 + (cell_width - img.width) // 2
            img_y = y0 + padding_y
            canvas.paste(img, (img_x, img_y), img)

            label = os.path.splitext(image_file)[0].replace("_", " ").upper()
            char_widths = [font.getbbox(c)[2] - font.getbbox(c)[0] for c in label]
            total_char_width = sum(char_widths)

            letter_spacing = (
                (cell_width - total_char_width) // (len(label) - 1)
                if len(label) > 1 else 0
            )
            if letter_spacing > 0:
                letter_spacing = 0  # only squeeze, don't expand

            text_width = total_char_width + (len(label) - 1) * letter_spacing
            text_x = x0 + (cell_width - text_width) // 2
            text_y = img_y + img.height + gap

            draw_text_with_spacing(draw, label, font, LABEL_COLOR, (text_x, text_y), letter_spacing)

    canvas.save(output_path, "PDF", dpi=(DPI, DPI))
    print(f"Grid layout saved to {output_path}")
