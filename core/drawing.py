from PIL import Image, ImageDraw, ImageFont
from core.utils import draw_debug_box, fit_text_to_width 
import os, random
import time

def generate_bingo_cards(page_layout, bingo_card_layout):
    global_start = time.time()
    """
    Generates a printable bingo card page with a frame, header, and image grid.
    """
    # generate white canvas and define print-safe area
    height = page_layout.HEIGHT_PIXELS
    width = page_layout.WIDTH_PIXELS
    base_card = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    margin = page_layout.MARGIN
    usable_width = width - 2 * margin
    usable_height = height - 2 * margin

    # load and paste frame
    start = time.time()
    frame = Image.open(bingo_card_layout.FRAME_IMAGE_PATH).convert("RGBA").resize((usable_width, usable_height), Image.LANCZOS)
    base_card.paste(frame, (margin, margin), frame)
    print(f"Frame load and paste: {time.time() - start:.2f}s")

    # define content area
    padding = bingo_card_layout.FRAME_INNER_PADDING
    content_x = margin + padding["left"]
    content_y = margin + padding["top"]
    content_width = usable_width - padding["left"] - padding["right"]
    content_height = usable_height - padding["top"] - padding["bottom"]

    # load and paste header
    start = time.time()
    header = Image.open(bingo_card_layout.HEADER_IMAGE_PATH).convert("RGBA")
    header_width, header_height = header.size
    if header_width != content_width:
        scale_factor = content_width / header_width
        header_width = int(header_width * scale_factor)
        header_height = int(header_height * scale_factor)
        header = header.resize((header_width, header_height), Image.LANCZOS)
    header_x = content_x + (content_width - header_width) // 2
    base_card.paste(header, (header_x, content_y), header)
    print(f"Header load and paste: {time.time() - start:.2f}s")

    # draw grid
    start = time.time()
    draw = ImageDraw.Draw(base_card)
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
    print(f"Grid drawing: {time.time() - start:.2f}s")
    # load images and labels and paste to cells
    start = time.time()
    padding_y = int(cell_height * bingo_card_layout.CELL_PADDING_Y_RATIO)
    padding_x = int(cell_width * bingo_card_layout.CELL_PADDING_X_RATIO)
    label_height = int(cell_height * bingo_card_layout.LABEL_HEIGHT_RATIO)
    gap = int(label_height * bingo_card_layout.LABEL_GAP_RATIO)

    available_img_height = cell_height - 2 * padding_y - gap - label_height
    available_img_width = cell_width - 2 * padding_x

    image_pool = [
        f for f in os.listdir(bingo_card_layout.BINGO_IMAGES_PATH)
        if f.lower().endswith(".png")
    ]

    used_permutations = set()
    card_image_sets = []

    while len(card_image_sets) < bingo_card_layout.CARD_AMOUNT:
        selected = tuple(random.sample(image_pool, 24))  # preserves order
        if selected not in used_permutations:
            used_permutations.add(selected)
            card_image_sets.append(selected)
    print(f"Image selection for {bingo_card_layout.CARD_AMOUNT} cards: {time.time() - start:.2f}s")
    bingo_cards = []
    start_total_cards = time.time()
    for image_set in card_image_sets:
        # Work on a copy of the base canvas
        card = base_card.copy()
        draw = ImageDraw.Draw(card)
        image_iter = iter(image_set)

        for row in range(rows):
            for col in range(cols):
                if row == 2 and col == 2:
                    fs_path = bingo_card_layout.FREE_SPACE_IMAGE_PATH
                    free_space_img = Image.open(fs_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)

                    center_x = grid_x + 2 * cell_width
                    center_y = grid_y + 2 * cell_height
                    fs_x = center_x + (cell_width - free_space_img.width) // 2
                    fs_y = center_y + (cell_height - free_space_img.height) // 2

                    card.paste(free_space_img, (fs_x, fs_y), free_space_img)
                else:
                    x0 = grid_x + col * cell_width
                    y0 = grid_y + row * cell_height

                    img_path = os.path.join(bingo_card_layout.BINGO_IMAGES_PATH, next(image_iter))
                    img = Image.open(img_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
                    img_x = x0 + (cell_width - img.width) // 2
                    img_y = y0 + padding_y
                    card.paste(img, (img_x, img_y), img)

                    label = os.path.splitext(os.path.basename(img_path))[0].replace("_", " ").upper()

                    font_size = int(label_height * bingo_card_layout.LABEL_FONT_SCALE)
                    font_loader = lambda size: ImageFont.truetype(page_layout.FONT_PATH, size)
                    font = fit_text_to_width(label, font_loader, cell_width, font_size)
                    bbox = font.getbbox(label)
                    text_width = bbox[2] - bbox[0]
                    text_x = x0 + (cell_width - text_width) // 2
                    text_y = img_y + img.height + gap

                    draw.text((text_x, text_y), label, font=font, fill=bingo_card_layout.LABEL_COLOR)
        
        bingo_cards.append(card)
        
    print(f"Generating all cards: {time.time() - start_total_cards:.2f}s")
    '''
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
    
    '''
    if bingo_cards:
        first_card = bingo_cards[0]
        rest_cards = bingo_cards[1:]
        first_card.save(
            page_layout.OUTPUT_PATH,
            "PDF",
            resolution=page_layout.DPI,
            save_all=True,
            append_images=rest_cards
        )
    print(f"Saving PDF: {time.time() - start:.2f}s")
    print(f"Total function time: {time.time() - global_start:.2f}s")


def generate_calling_cards_single(page_layout, calling_card_single_layout):
    pass

def generate_calling_cards_multi(page_layout, calling_card_multi_layout):
    pass

def generate_tokens_large(page_layout, tokens_large_layout):
    pass

def generate_tokens_small(page_layout, tokens_small_layout):
    pass
