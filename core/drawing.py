from PIL import Image, ImageDraw, ImageFont
from core.utils import draw_debug_box, fit_text_to_width 
import os, random
import time
from math import hypot, ceil

def generate_bingo_cards(page_layout, bingo_card_layout):
    global_start = time.time()
    """
    Generates a printable bingo card page with a frame, header, and image grid.
    """
    # generate white canvas and define print-safe area
    height = page_layout.HEIGHT_PIXELS
    width = page_layout.WIDTH_PIXELS
    base_card = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    
    usable_width = width - page_layout.LEFT_MARGIN - page_layout.RIGHT_MARGIN
    usable_height = height - page_layout.TOP_MARGIN - page_layout.BOTTOM_MARGIN

    # load and paste frame (optional)
    if bingo_card_layout.FRAME_ENABLED:
        frame = Image.open(bingo_card_layout.FRAME_IMAGE_PATH).convert("RGBA").resize((usable_width, usable_height), Image.LANCZOS)
        flattened_frame = Image.new("RGB", frame.size, (255, 255, 255))
        flattened_frame.paste(frame, (0,0), mask=frame.getchannel("A"))
        base_card.paste(flattened_frame, (page_layout.LEFT_MARGIN, page_layout.TOP_MARGIN))
        padding = bingo_card_layout.FRAME_INNER_PADDING
    else:
        padding = {"left": 0, "right": 0, "top": 0, "bottom": 0}

    # define content area
    content_x = page_layout.LEFT_MARGIN + padding["left"]
    content_y = page_layout.TOP_MARGIN + padding["top"]
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
    flattened_header = Image.new("RGB", header.size, (255, 255, 255))
    flattened_header.paste(header, (0, 0), mask=header.getchannel("A"))
    base_card.paste(flattened_header, (header_x, content_y))

    # draw grid
    start = time.time()
    draw = ImageDraw.Draw(base_card)
    line_color = bingo_card_layout.GRID_LINE_COLOR
    line_thickness = bingo_card_layout.GRID_LINE_THICKNESS
    cols = bingo_card_layout.GRID_COLS
    rows = bingo_card_layout.GRID_ROWS
    grid_x = content_x
    grid_y = content_y + header_height + bingo_card_layout.HEADER_MARGIN_BOTTOM
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

    # load images and labels and paste to cells
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
        selected = tuple(random.sample(image_pool, 24))
        if selected not in used_permutations:
            used_permutations.add(selected)
            card_image_sets.append(selected)
    
    bingo_cards = []
    start_total_cards = time.time()
    # todo: enable label length checking
    for image_set in card_image_sets:
        card = base_card.copy()
        draw = ImageDraw.Draw(card)
        image_iter = iter(image_set)

        for row in range(rows):
            for col in range(cols):
                if row == 2 and col == 2:
                    free_space_path = bingo_card_layout.FREE_SPACE_IMAGE_PATH
                    free_space_img = Image.open(free_space_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
                    flattened_fs = Image.new("RGB", free_space_img.size, (255, 255, 255))
                    flattened_fs.paste(free_space_img, (0, 0), mask=free_space_img.getchannel("A"))

                    center_x = grid_x + 2 * cell_width
                    center_y = grid_y + 2 * cell_height
                    fs_x = center_x + (cell_width - free_space_img.width) // 2
                    fs_y = center_y + (cell_height - free_space_img.height) // 2

                    card.paste(flattened_fs, (fs_x, fs_y))
                else:
                    x0 = grid_x + col * cell_width
                    y0 = grid_y + row * cell_height

                    img_path = os.path.join(bingo_card_layout.BINGO_IMAGES_PATH, next(image_iter))
                    img = Image.open(img_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
                    flattened_img = Image.new("RGB", img.size, (255, 255, 255))
                    flattened_img.paste(img, (0, 0), mask=img.getchannel("A"))

                    img_x = x0 + (cell_width - flattened_img.width) // 2
                    img_y = y0 + padding_y
                    card.paste(flattened_img, (img_x, img_y))

                    label = os.path.splitext(os.path.basename(img_path))[0].replace("_", " ").upper()

                    font_size = int(label_height * bingo_card_layout.LABEL_FONT_SCALE)
                    font_loader = lambda size: ImageFont.truetype(page_layout.FONT_PATH, size)
                    font = font_loader(font_size)

                    available_width = cell_width - 2 * padding_x
                    raw_text_width = font.getlength(label)
                    text_y = img_y + img.height + gap

                    if raw_text_width > available_width and len(label) > 1:
                        # Use even spacing
                        spacing = available_width / len(label)
                        start_x = x0 + (cell_width - available_width) / 2

                        for i, char in enumerate(label):
                            char_width = font.getlength(char)
                            char_x = start_x + (i + 0.5) * spacing - char_width / 2
                            draw.text((char_x, text_y), char, font=font, fill=bingo_card_layout.LABEL_COLOR)
                    else:
                        # Use normal centered label
                        text_width = font.getlength(label)
                        text_x = x0 + (cell_width - text_width) / 2
                        draw.text((text_x, text_y), label, font=font, fill=bingo_card_layout.LABEL_COLOR)
                            
            bingo_cards.append(card)
        
    print(f"Generating all cards: {time.time() - start_total_cards:.2f}s")
  
    if bingo_cards:
        first_card = bingo_cards[0].convert("RGB")
        rest_cards = [card.convert("RGB") for card in bingo_cards[1:]]
        first_card.save(
            bingo_card_layout.OUTPUT_PATH,
            "PDF",
            resolution=page_layout.DPI,
            save_all=True,
            append_images=rest_cards
        )
    print(f"Saving PDF: {time.time() - start:.2f}s")
    print(f"Total function time: {time.time() - global_start:.2f}s")

def generate_bingo_cards_multi(page_layout, bingo_card_multi_layout):
    global_start = time.time()
    """
    Generates a printable bingo card page with a frame, header, and image grid.
    """
    # generate white canvas and define print-safe area
    height = page_layout.WIDTH_PIXELS
    width = page_layout.HEIGHT_PIXELS
    base_card = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    side_margin = page_layout.LEFT_MARGIN
    top_margin = int(side_margin * 2.5)
    usable_width = (width - 4 * side_margin) // 2
    usable_height = height - 2 * top_margin
    x_offset = 3 * side_margin + usable_width

    # load and paste frame
    frame = Image.open(bingo_card_multi_layout.FRAME_IMAGE_PATH).convert("RGBA").resize((usable_width, usable_height), Image.LANCZOS)
    flattened_frame = Image.new("RGB", frame.size, (255, 255, 255))
    flattened_frame.paste(frame, (0,0), mask=frame.getchannel("A"))
    base_card.paste(flattened_frame, (side_margin, top_margin))
    base_card.paste(flattened_frame,  (x_offset,  top_margin))

    # define content area
    padding = bingo_card_multi_layout.FRAME_INNER_PADDING
    content_x = side_margin + padding["left"]
    content_2x = 3 * side_margin + usable_width + padding["left"]
    content_y = top_margin + padding["top"]
    content_width = usable_width - padding["left"] - padding["right"]
    content_height = usable_height - padding["top"] - padding["bottom"]

    # load and paste header
    header = Image.open(bingo_card_multi_layout.HEADER_IMAGE_PATH).convert("RGBA")
    header_width, header_height = header.size
    if header_width != content_width:
        scale_factor = content_width / header_width
        header_width = int(header_width * scale_factor)
        header_height = int(header_height * scale_factor)
        header = header.resize((header_width, header_height), Image.LANCZOS)
    header_x = content_x + (content_width - header_width) // 2
    header_2x = content_2x + (content_width - header_width) // 2
    flattened_header = Image.new("RGB", header.size, (255, 255, 255))
    flattened_header.paste(header, (0, 0), mask=header.getchannel("A"))
    base_card.paste(flattened_header, (header_x, content_y))
    base_card.paste(flattened_header, (header_2x, content_y))

    # draw grid
    start = time.time()
    draw = ImageDraw.Draw(base_card)
    line_color = bingo_card_multi_layout.GRID_LINE_COLOR
    line_thickness = bingo_card_multi_layout.GRID_LINE_THICKNESS
    cols = bingo_card_multi_layout.GRID_COLS
    rows = bingo_card_multi_layout.GRID_ROWS
    grid_x = content_x
    grid_2x = content_2x
    grid_y = content_y + header_height + bingo_card_multi_layout.HEADER_MARGIN_BOTTOM
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
        
    
    for i in range(rows + 1):
        y_line = grid_y + i * cell_height
        draw.line(
            [(grid_2x, y_line), (grid_2x + cols * cell_width, y_line)],
            fill=line_color,
            width=line_thickness)
    for j in range(cols + 1):
        x_line = grid_2x + j * cell_width
        draw.line([(x_line, grid_y), (x_line, grid_y + rows * cell_height)],
                  fill=line_color,
                  width=line_thickness)

    # load images and labels and paste to cells
    padding_y = int(cell_height * bingo_card_multi_layout.CELL_PADDING_Y_RATIO)
    padding_x = int(cell_width * bingo_card_multi_layout.CELL_PADDING_X_RATIO)
    label_height = int(cell_height * bingo_card_multi_layout.LABEL_HEIGHT_RATIO)
    gap = int(label_height * bingo_card_multi_layout.LABEL_GAP_RATIO)

    available_img_height = cell_height - 2 * padding_y - gap - label_height
    available_img_width = cell_width - 2 * padding_x

    image_pool = [
        f for f in os.listdir(bingo_card_multi_layout.BINGO_IMAGES_PATH)
        if f.lower().endswith(".png")
    ]

    used_permutations = set()
    card_image_sets = []

    while len(card_image_sets) < bingo_card_multi_layout.CARD_AMOUNT:
        selected = tuple(random.sample(image_pool, 24))
        if selected not in used_permutations:
            used_permutations.add(selected)
            card_image_sets.append(selected)
    
    bingo_cards = []
    start_total_cards = time.time()
    for i in range(0, len(card_image_sets), 2):
        left_card = card_image_sets[i]
        right_card = card_image_sets[i + 1] if i + 1 < len(card_image_sets) else None
        card = base_card.copy()
        draw = ImageDraw.Draw(card)
        
        image_iter_left = iter(left_card)
        image_iter_right = iter(right_card)
        for row in range(rows):
            for col in range(cols):
                if row == 2 and col == 2:
                    free_space_path = bingo_card_multi_layout.FREE_SPACE_IMAGE_PATH
                    free_space_img = Image.open(free_space_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
                    flattened_fs = Image.new("RGB", free_space_img.size, (255, 255, 255))
                    flattened_fs.paste(free_space_img, (0, 0), mask=free_space_img.getchannel("A"))

                    center_x = grid_x + 2 * cell_width
                    center_2x = grid_2x + 2 * cell_width
                    center_y = grid_y + 2 * cell_height
                    fs_x = center_x + (cell_width - free_space_img.width) // 2
                    fs_2x = center_2x + (cell_width - free_space_img.width) // 2
                    fs_y = center_y + (cell_height - free_space_img.height) // 2

                    card.paste(flattened_fs, (fs_x, fs_y))
                    card.paste(flattened_fs, (fs_2x, fs_y))
                else:
                    x0 = grid_x + col * cell_width
                    x20 = grid_2x + col * cell_width
                    y0 = grid_y + row * cell_height

                    img_left_path = os.path.join(bingo_card_multi_layout.BINGO_IMAGES_PATH, next(image_iter_left))
                    img_right_path = os.path.join(bingo_card_multi_layout.BINGO_IMAGES_PATH, next(image_iter_right))
                    img_left = Image.open(img_left_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
                    img_right = Image.open(img_right_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
                    flattened_left_img = Image.new("RGB", img_left.size, (255, 255, 255))
                    flattened_right_img = Image.new("RGB", img_right.size, (255, 255, 255))
                    flattened_left_img.paste(img_left, (0, 0), mask=img_left.getchannel("A"))
                    flattened_right_img.paste(img_right, (0, 0), mask=img_right.getchannel("A"))

                    img_x = x0 + (cell_width - flattened_left_img.width) // 2
                    img_2x = x20 + (cell_width - flattened_right_img.width) //2
                    img_y = y0 + padding_y
                    card.paste(flattened_left_img, (img_x, img_y))
                    card.paste(flattened_right_img, (img_2x, img_y))

                    label_left = os.path.splitext(os.path.basename(img_left_path))[0].replace("_", " ").upper()
                    label_right = os.path.splitext(os.path.basename(img_right_path))[0].replace("_", " ").upper()

                    font_size = int(label_height * bingo_card_multi_layout.LABEL_FONT_SCALE)
                    font_loader = lambda size: ImageFont.truetype(page_layout.FONT_PATH, size)

                    # Left label
                    font_left = font_loader(font_size)
                    available_width_left = cell_width - 2 * padding_x
                    raw_text_width_left = font_left.getlength(label_left)
                    text_y_left = img_y + img_left.height + gap

                    if raw_text_width_left > available_width_left and len(label_left) > 1:
                        spacing_left = available_width_left / len(label_left)
                        start_x_left = x0 + (cell_width - available_width_left) / 2
                        for i, char in enumerate(label_left):
                            char_width = font_left.getlength(char)
                            char_x = start_x_left + (i + 0.5) * spacing_left - char_width / 2
                            draw.text((char_x, text_y_left), char, font=font_left, fill=bingo_card_multi_layout.LABEL_COLOR)
                    else:
                        text_x_left = x0 + (cell_width - raw_text_width_left) / 2
                        draw.text((text_x_left, text_y_left), label_left, font=font_left, fill=bingo_card_multi_layout.LABEL_COLOR)

                    # Right label
                    font_right = font_loader(font_size)
                    available_width_right = cell_width - 2 * padding_x
                    raw_text_width_right = font_right.getlength(label_right)
                    text_y_right = img_y + img_right.height + gap

                    if raw_text_width_right > available_width_right and len(label_right) > 1:
                        spacing_right = available_width_right / len(label_right)
                        start_x_right = x20 + (cell_width - available_width_right) / 2
                        for i, char in enumerate(label_right):
                            char_width = font_right.getlength(char)
                            char_x = start_x_right + (i + 0.5) * spacing_right - char_width / 2
                            draw.text((char_x, text_y_right), char, font=font_right, fill=bingo_card_multi_layout.LABEL_COLOR)
                    else:
                        text_x_right = x20 + (cell_width - raw_text_width_right) / 2
                        draw.text((text_x_right, text_y_right), label_right, font=font_right, fill=bingo_card_multi_layout.LABEL_COLOR)

        bingo_cards.append(card)
        
    print(f"Generating all cards: {time.time() - start_total_cards:.2f}s")


  
    if bingo_cards:
        first_card = bingo_cards[0].convert("RGB")
        rest_cards = [card.convert("RGB") for card in bingo_cards[1:]]
        first_card.save(
            bingo_card_multi_layout.OUTPUT_PATH,
            "PDF",
            resolution=page_layout.DPI,
            save_all=True,
            append_images=rest_cards
        )
    print(f"Saving PDF: {time.time() - start:.2f}s")
    print(f"Total function time: {time.time() - global_start:.2f}s")


def generate_calling_cards_single(page_layout, calling_card_single_layout):
    # generate white canvas and define print-safe area
    height = page_layout.HEIGHT_PIXELS
    width = page_layout.WIDTH_PIXELS
    page = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    margin = page_layout.MARGIN
    usable_width = width - 2 * margin
    usable_height = height - 2 * margin

    # load and paste header
    header = Image.open(calling_card_single_layout.HEADER_IMAGE_PATH).convert("RGBA")
    header_width, header_height = header.size
    if header_width > usable_width:
        scale_factor = usable_width / header_width
        header_width = int(header_width * scale_factor)
        header_height = int(header_height * scale_factor)
        header = header.resize((header_width, header_height), Image.LANCZOS)
    header_x = page_layout.MARGIN + (usable_width - header_width) // 2
    header_y = page_layout.MARGIN
    flattened_header = Image.new("RGB", header.size, (255, 255, 255))
    flattened_header.paste(header, (0, 0), mask=header.getchannel("A"))
    page.paste(flattened_header, (header_x, header_y))



    # draw grid
    draw = ImageDraw.Draw(page)
    line_color = calling_card_single_layout.GRID_LINE_COLOR
    line_thickness = calling_card_single_layout.GRID_LINE_THICKNESS
    cols = calling_card_single_layout.GRID_COLS
    rows = calling_card_single_layout.GRID_ROWS
    grid_x = margin
    grid_y = margin + header_height
    grid_height = usable_height - header_height
    cell_width = usable_width // cols
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
    

    image_files = [
        f for f in os.listdir(calling_card_single_layout.BINGO_IMAGES_PATH)
        if f.lower().endswith(".png")
    ]
    assert len(image_files) == cols * rows, f"Expected exactly {cols * rows} images"

    label_height = int(cell_height * calling_card_single_layout.LABEL_HEIGHT_RATIO)
    gap = int(label_height * calling_card_single_layout.LABEL_GAP_RATIO)
    padding_y = int(cell_height * calling_card_single_layout.CELL_PADDING_Y_RATIO)
    padding_x = int(cell_width * calling_card_single_layout.CELL_PADDING_X_RATIO)

    available_img_height = cell_height - 2 * padding_y - gap - label_height
    available_img_width = cell_width - 2 * padding_x

    font_size = int(label_height * calling_card_single_layout.LABEL_FONT_SCALE)
    font = ImageFont.truetype(page_layout.FONT_PATH, size=font_size)

    image_iter = iter(image_files)

    for row in range(rows):
        for col in range(cols):
            x0 = grid_x + col * cell_width
            y0 = grid_y + row * cell_height

            img_path = os.path.join(calling_card_single_layout.BINGO_IMAGES_PATH, next(image_iter))
            img = Image.open(img_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
            flattened_img = Image.new("RGB", img.size, (255, 255, 255))
            flattened_img.paste(img, (0, 0), mask=img.getchannel("A"))

            img_x = x0 + (cell_width - flattened_img.width) // 2
            img_y = y0 + padding_y
            page.paste(flattened_img, (img_x, img_y))

            label = os.path.splitext(os.path.basename(img_path))[0].replace("_", " ").upper()

            font_size = int(label_height * calling_card_single_layout.LABEL_FONT_SCALE)
            font_loader = lambda size: ImageFont.truetype(page_layout.FONT_PATH, size)
            font = fit_text_to_width(label, font_loader, cell_width, font_size)
            dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
            bbox = dummy_draw.textbbox((0, 0), label, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_patch = Image.new("RGB", (text_width, text_height), (255, 255, 255))
            text_draw = ImageDraw.Draw(text_patch)
            text_draw.text((-bbox[0], -bbox[1]), label, font=font, fill=calling_card_single_layout.LABEL_COLOR)

            text_x = x0 + (cell_width - text_width) // 2
            text_y = img_y + img.height + gap

            page.paste(text_patch, (text_x, text_y))
    
    print(cell_width * cols, usable_width)

    page = page.convert("RGB")
    page.save(page_layout.OUTPUT_PATH, "PDF", dpi=(page_layout.DPI, page_layout.DPI))

def generate_calling_cards_multi(page_layout, calling_card_multi_layout):
    # generate white canvas and define print-safe area
    height = page_layout.HEIGHT_PIXELS
    width = page_layout.WIDTH_PIXELS
    base_page = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    margin = page_layout.MARGIN
    usable_width = width - 2 * margin
    usable_height = height - 2 * margin

    # load and paste scissors icon
    scissors = Image.open(calling_card_multi_layout.SCISSORS_IMAGE_PATH).convert("RGBA")
    scissors_width, scissors_height = scissors.size
    scissors_width = int(usable_width * calling_card_multi_layout.SCISSORS_WIDTH_SCALE_FACTOR)
    scissors_height = int(usable_height * calling_card_multi_layout.SCISSORS_HEIGHT_SCALE_FACTOR)
    scissors = scissors.resize((scissors_width, scissors_height), Image.LANCZOS)
    flattened_scissors = Image.new("RGB", scissors.size, (255, 255, 255))
    flattened_scissors.paste(scissors, (0, 0), mask=scissors.getchannel("A"))
    base_page.paste(flattened_scissors, (margin, margin))

    # draw grid
    draw = ImageDraw.Draw(base_page)
    line_color = calling_card_multi_layout.GRID_LINE_COLOR
    line_thickness = calling_card_multi_layout.GRID_LINE_THICKNESS
    cols = calling_card_multi_layout.GRID_COLS
    rows = calling_card_multi_layout.GRID_ROWS
    grid_x = margin
    grid_y = margin + scissors_height + calling_card_multi_layout.SCISSORS_BOTTOM_MARGIN
    grid_height = usable_height - scissors_height - calling_card_multi_layout.SCISSORS_BOTTOM_MARGIN
    cell_width = usable_width // cols
    cell_height = grid_height // rows

    image_files = [
        f for f in os.listdir(calling_card_multi_layout.BINGO_IMAGES_PATH)
        if f.lower().endswith(".png")
    ]

    num_pages = ceil(len(image_files) / (rows * cols))
    pages = []
    image_iter = iter(image_files)

    while num_pages > 0:
        page = base_page.copy()
        draw = ImageDraw.Draw(page)
        col_iter = cols

        if num_pages > 1:
            row_iter = rows
        else:
            row_iter = 1

        for i in range(row_iter + 1):
            y_line = grid_y + i * cell_height
            x1, y1 = (grid_x, y_line)
            x2, y2 = (grid_x + cols * cell_width, y_line)
            total_length = int(hypot(x2 - x1, y2 - y1))
            dot_length = 10
            gap_length = 5
            num_dots = (total_length // (dot_length + gap_length))
            dx = (x2 - x1) / total_length
            dy = (y2 - y1) / total_length

            for i in range(num_dots):
                dot_start_x = x1 + (dot_length + gap_length) * i * dx
                dot_start_y = y1 + (dot_length + gap_length) * i * dy
                dot_end_x = dot_start_x + dot_length * dx
                dot_end_y = dot_start_y + dot_length * dy
                draw.line([(dot_start_x, dot_start_y), (dot_end_x, dot_end_y)], fill=line_color, width=line_thickness)

        for j in range(col_iter + 1):
            x_line = grid_x + j * cell_width
            x1, y1 = (x_line, grid_y)
            x2, y2 = (x_line, grid_y + row_iter * cell_height)
            total_length = int(hypot(x2 - x1, y2 - y1))
            dot_length = 10
            gap_length = 5
            num_dots = total_length // (dot_length + gap_length) + 1

            dx = (x2 - x1) / total_length
            dy = (y2 - y1) / total_length

            for i in range(num_dots):
                dot_start_x = x1 + (dot_length + gap_length) * i * dx
                dot_start_y = y1 + (dot_length + gap_length) * i * dy
                dot_end_x = dot_start_x + dot_length * dx
                dot_end_y = dot_start_y + dot_length * dy
                draw.line([(dot_start_x, dot_start_y), (dot_end_x, dot_end_y)], fill=line_color, width=line_thickness)

    
        label_height = int(cell_height * calling_card_multi_layout.LABEL_HEIGHT_RATIO)
        gap = int(label_height * calling_card_multi_layout.LABEL_GAP_RATIO)
        padding_y = int(cell_height * calling_card_multi_layout.CELL_PADDING_Y_RATIO)
        padding_x = int(cell_width * calling_card_multi_layout.CELL_PADDING_X_RATIO)

        available_img_height = cell_height - 2 * padding_y - gap - label_height
        available_img_width = cell_width - 2 * padding_x

        font_size = int(label_height * calling_card_multi_layout.LABEL_FONT_SCALE)
        font = ImageFont.truetype(page_layout.FONT_PATH, size=font_size)

        for row in range(row_iter):
            for col in range(col_iter):
                x0 = grid_x + col * cell_width
                y0 = grid_y + row * cell_height

                img_path = os.path.join(calling_card_multi_layout.BINGO_IMAGES_PATH, next(image_iter))
                img = Image.open(img_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
                flattened_img = Image.new("RGB", img.size, (255, 255, 255))
                flattened_img.paste(img, (0, 0), mask=img.getchannel("A"))

                img_x = x0 + (cell_width - flattened_img.width) // 2
                img_y = y0 + padding_y
                page.paste(flattened_img, (img_x, img_y))

                label = os.path.splitext(os.path.basename(img_path))[0].replace("_", " ").upper()

                font_size = int(label_height * calling_card_multi_layout.LABEL_FONT_SCALE)
                font_loader = lambda size: ImageFont.truetype(page_layout.FONT_PATH, size)
                font = fit_text_to_width(label, font_loader, available_img_width, font_size)
                dummy_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
                bbox = dummy_draw.textbbox((0, 0), label, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_patch = Image.new("RGB", (text_width, text_height), (255, 255, 255))
                text_draw = ImageDraw.Draw(text_patch)
                text_draw.text((-bbox[0], -bbox[1]), label, font=font, fill=calling_card_multi_layout.LABEL_COLOR)

                text_x = x0 + (cell_width - text_width) // 2
                text_y = img_y + img.height + gap

                page.paste(text_patch, (text_x, text_y))

        num_pages = num_pages - 1
        pages.append(page)

    if pages:
        first_card = pages[0].convert("RGB")
        rest_cards = [card.convert("RGB") for card in pages[1:]]
        first_card.save(
            page_layout.OUTPUT_PATH,
            "PDF",
            resolution=page_layout.DPI,
            save_all=True,
            append_images=rest_cards
        )


def generate_tokens(page_layout, tokens_layout):
    # generate white canvas and define print-safe area
    height = page_layout.HEIGHT_PIXELS
    width = page_layout.WIDTH_PIXELS
    page = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    margin = page_layout.MARGIN
    usable_width = width - 2 * margin
    usable_height = height - 2 * margin

    # load and paste scissors icon
    scissors = Image.open(tokens_layout.SCISSORS_IMAGE_PATH).convert("RGBA")
    scissors_width, scissors_height = scissors.size
    scissors_width = int(usable_width * tokens_layout.SCISSORS_WIDTH_SCALE_FACTOR)
    scissors_height = int(usable_height * tokens_layout.SCISSORS_HEIGHT_SCALE_FACTOR)
    scissors = scissors.resize((scissors_width, scissors_height), Image.LANCZOS)
    flattened_scissors = Image.new("RGB", scissors.size, (255, 255, 255))
    flattened_scissors.paste(scissors, (0, 0), mask=scissors.getchannel("A"))
    page.paste(flattened_scissors, (margin, margin))

    # draw grid
    draw = ImageDraw.Draw(page)
    line_color = tokens_layout.GRID_LINE_COLOR
    line_thickness = tokens_layout.GRID_LINE_THICKNESS
    cols = tokens_layout.GRID_COLS
    rows = tokens_layout.GRID_ROWS
    grid_x = margin
    grid_y = margin + scissors_height + tokens_layout.SCISSORS_BOTTOM_MARGIN
    grid_height = usable_height - scissors_height - tokens_layout.SCISSORS_BOTTOM_MARGIN
    cell_width = usable_width // cols
    cell_height = grid_height // rows

    print("cell_width:", cell_width, "cell_height:", cell_height)
    print("grid_width:", cell_width * cols, "grid_height:", cell_height * rows)

    for i in range(rows + 1):
        y_line = grid_y + i * cell_height
        x1, y1 = (grid_x, y_line)
        x2, y2 = (grid_x + cols * cell_width, y_line)
        total_length = int(hypot(x2 - x1, y2 - y1))
        dot_length = 5
        gap_length = 5
        num_dots = total_length // (dot_length + gap_length)
        dx = (x2 - x1) / total_length
        dy = (y2 - y1) / total_length

        for i in range(num_dots):
            dot_start_x = x1 + (dot_length + gap_length) * i * dx
            dot_start_y = y1 + (dot_length + gap_length) * i * dy
            dot_end_x = dot_start_x + dot_length * dx
            dot_end_y = dot_start_y + dot_length * dy
            draw.line([(dot_start_x, dot_start_y), (dot_end_x, dot_end_y)], fill=line_color, width=line_thickness)

    for j in range(cols + 1):
        x_line = grid_x + j * cell_width
        x1, y1 = (x_line, grid_y)
        x2, y2 = (x_line, grid_y + rows * cell_height)
        total_length = int(hypot(x2 - x1, y2 - y1))
        dot_length = 5
        gap_length = 5
        num_dots = total_length // (dot_length + gap_length)

        dx = (x2 - x1) / total_length
        dy = (y2 - y1) / total_length

        for i in range(num_dots):
            dot_start_x = x1 + (dot_length + gap_length) * i * dx
            dot_start_y = y1 + (dot_length + gap_length) * i * dy
            dot_end_x = dot_start_x + dot_length * dx
            dot_end_y = dot_start_y + dot_length * dy
            draw.line([(dot_start_x, dot_start_y), (dot_end_x, dot_end_y)], fill=line_color, width=line_thickness)

    padding_x = int(cell_width * tokens_layout.CELL_PADDING_X_RATIO)
    available_img_width = cell_width - 2 * padding_x
    token = Image.open(tokens_layout.TOKEN_IMAGE_PATH).convert("RGBA").resize((available_img_width, available_img_width), Image.LANCZOS)
    flattened_token = Image.new("RGB", token.size, (255, 255, 255))
    flattened_token.paste(token, (0, 0), mask=token.getchannel("A"))

    for row in range(rows):
            for col in range(cols):
                x0 = grid_x + col * cell_width
                y0 = grid_y + row * cell_height
                img_x = x0 + (cell_width - flattened_token.width) // 2
                img_y = y0 + (cell_height - flattened_token.height) // 2
                page.paste(flattened_token, (img_x, img_y))

    page = page.convert("RGB")
    page.save(page_layout.OUTPUT_PATH, "PDF", dpi=(page_layout.DPI, page_layout.DPI))
