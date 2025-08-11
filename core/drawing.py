from config.layouts import PageLayout, BingoCardLayout, BingoCardMultiLayout, CallingCardsSinglePageLayout, CallingCardsMultiPageLayout, TokensLayout
from PIL import Image, ImageDraw, ImageFont
from core.utils import draw_debug_box, fit_text_to_width, create_canvas, load_and_paste_header, draw_grid, load_images_and_labels, shuffle_images, paste_images, paste_single_card, save_as_pdf
import os
import time
from math import hypot, ceil

def generate_bingo_cards(page_layout: PageLayout, bingo_card_layout: BingoCardLayout):
    global_start = time.time()
    """
    Generates a printable bingo card page with a frame, header, and image grid.
    """
    start = time.time()
    base_card, content_x, content_y, content_width, content_height = create_canvas(page_layout, bingo_card_layout)
    print(f"Create Canvas: {time.time() - start:.2f}s")

    start = time.time()
    header_height = load_and_paste_header(page_layout.HEADER_IMAGE_PATH, bingo_card_layout, base_card, content_width, content_x, content_y)
    print(f"Load and paste header: {time.time() - start:.2f}s")
    
    start = time.time()
    cell_width, cell_height, grid_x, grid_y = draw_grid(page_layout, bingo_card_layout, base_card, content_x, content_y, content_width, content_height, header_height)
    print(f"Draw Grid: {time.time() - start:.2f}s")

    start = time.time()
    loaded_images, free_space_img = load_images_and_labels(page_layout, bingo_card_layout, cell_height, cell_width)
    print(f"Load images: {time.time() - start:.2f}s")

    start = time.time() 
    image_sets = shuffle_images(bingo_card_layout, loaded_images)
    print(f"Shuffle images: {time.time() - start:.2f}s") 

    start_total_cards = time.time()
    bingo_cards = paste_images(page_layout, bingo_card_layout, base_card, loaded_images, free_space_img, image_sets, cell_width, cell_height, grid_x, grid_y)
    print(f"Generating bingo cards: {time.time() - start_total_cards:.2f}s")
    
    start = time.time()
    save_as_pdf(page_layout, bingo_card_layout, bingo_cards)
    print(f"Saving PDF: {time.time() - start:.2f}s")
    print(f"Total function time: {time.time() - global_start:.2f}s")

def generate_bingo_cards_multi(page_layout: PageLayout, bingo_card_multi_layout: BingoCardMultiLayout):
    global_start = time.time()
    """
    Generates a printable bingo card page with a frame, header, and image grid.
    """

    base_card, content_x, content_y, content_2x, content_width, content_height = create_canvas(page_layout, bingo_card_multi_layout)

    header_height = load_and_paste_header(page_layout.HEADER_IMAGE_PATH, bingo_card_multi_layout, base_card, content_width, content_x, content_y)
    header_height = load_and_paste_header(page_layout.HEADER_IMAGE_PATH, bingo_card_multi_layout, base_card, content_width, content_2x, content_y)

    cell_width, cell_height, grid_x, grid_y = draw_grid(page_layout, bingo_card_multi_layout, base_card, content_x, content_y, content_width, content_height, header_height)
    cell_width, cell_height, grid_2x, grid_y = draw_grid(page_layout, bingo_card_multi_layout, base_card, content_2x, content_y, content_width, content_height, header_height)

    loaded_images, free_space_img = load_images_and_labels(page_layout, bingo_card_multi_layout, cell_height, cell_width)
    image_sets = list(shuffle_images(bingo_card_multi_layout, loaded_images))

    bingo_cards = []
    for i in range(0, len(image_sets), 2):
        left_set = image_sets[i]
        right_set = image_sets[i+1] if (i+1) < len(image_sets) else None

        card = base_card.copy()
        draw = ImageDraw.Draw(card)

        paste_single_card(page_layout, card, draw, loaded_images, free_space_img, left_set, cell_width, cell_height, grid_x, grid_y, bingo_card_multi_layout)
        paste_single_card(page_layout, card, draw, loaded_images, free_space_img, right_set, cell_width, cell_height, grid_2x, grid_y, bingo_card_multi_layout)

        bingo_cards.append(card)

    save_as_pdf(page_layout, bingo_card_multi_layout, bingo_cards)
    print(f"Total function time: {time.time() - global_start:.2f}s")

def generate_calling_cards_single(page_layout: PageLayout, calling_card_single_layout: CallingCardsSinglePageLayout):
    base_card, content_x, content_y, content_width, content_height = create_canvas(page_layout, calling_card_single_layout)
    
    header_height = load_and_paste_header(page_layout.CALLING_CARDS_HEADER_IMAGE_PATH, calling_card_single_layout, base_card, content_width, content_x, content_y)
    
    cell_width, cell_height, grid_x, grid_y = draw_grid(
        page_layout, calling_card_single_layout, base_card,
        content_x, content_y, content_width, content_height,
        header_height
    )
    
    loaded_images, _ = load_images_and_labels(page_layout, calling_card_single_layout, cell_height, cell_width)
    
    labels = list(loaded_images.keys())
    image_set = tuple(labels)
    
    card = base_card.copy()
    draw = ImageDraw.Draw(card)
    paste_single_card(
        page_layout, card, draw,
        loaded_images, 
        None,  
        image_set,
        cell_width,
        cell_height,
        grid_x,
        grid_y,
        calling_card_single_layout
    )
    
    save_as_pdf(page_layout, calling_card_single_layout, [card])
    
def generate_calling_cards_multi(page_layout: PageLayout, calling_card_multi_layout: CallingCardsMultiPageLayout):
    # generate white canvas and define print-safe area
    dpi = page_layout.DPI
    height = int(page_layout.HEIGHT_INCHES * dpi)
    width = int(page_layout.WIDTH_INCHES * dpi)
    top_margin = int(page_layout.MARGIN_TOP_INCHES * dpi)
    right_margin = int(page_layout.MARGIN_RIGHT_INCHES * dpi)
    bottom_margin = int(page_layout.MARGIN_BOTTOM_INCHES * dpi)
    left_margin = int(page_layout.MARGIN_LEFT_INCHES * dpi)
    base_page = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    usable_width = width - left_margin - right_margin
    usable_height = height - top_margin - bottom_margin

    # load and paste scissors icon
    scissors = Image.open(page_layout.SCISSORS_IMAGE_PATH).convert("RGBA")
    scissors_width, scissors_height = scissors.size
    scissors_width = int(usable_width * calling_card_multi_layout.SCISSORS_WIDTH_SCALE_FACTOR)
    scissors_height = int(usable_height * calling_card_multi_layout.SCISSORS_HEIGHT_SCALE_FACTOR)
    scissors = scissors.resize((scissors_width, scissors_height), Image.LANCZOS)
    flattened_scissors = Image.new("RGB", scissors.size, (255, 255, 255))
    flattened_scissors.paste(scissors, (0, 0), mask=scissors.getchannel("A"))
    base_page.paste(flattened_scissors, (left_margin, top_margin))

    # draw grid
    draw = ImageDraw.Draw(base_page)
    line_color = calling_card_multi_layout.GRID_LINE_COLOR
    line_thickness = int(calling_card_multi_layout.GRID_LINE_THICKNESS_INCHES * dpi)
    cols = calling_card_multi_layout.GRID_COLS
    rows = calling_card_multi_layout.GRID_ROWS
    grid_x = left_margin
    grid_y = top_margin + scissors_height + int(calling_card_multi_layout.GRID_MARGIN_TOP_INCHES * dpi)
    grid_height = usable_height - scissors_height - int(calling_card_multi_layout.GRID_MARGIN_TOP_INCHES * dpi)
    cell_width = usable_width // cols
    cell_height = grid_height // rows

    image_files = [
        f for f in os.listdir(page_layout.BINGO_IMAGES_PATH)
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
            num_dots = total_length // (dot_length + gap_length)
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

        font_size = int(label_height)
        font = ImageFont.truetype(page_layout.FONT_PATH, size=font_size)

        for row in range(row_iter):
            for col in range(col_iter):
                x0 = grid_x + col * cell_width
                y0 = grid_y + row * cell_height

                img_path = os.path.join(page_layout.BINGO_IMAGES_PATH, next(image_iter))
                img = Image.open(img_path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
                flattened_img = Image.new("RGB", img.size, (255, 255, 255))
                flattened_img.paste(img, (0, 0), mask=img.getchannel("A"))

                img_x = x0 + (cell_width - flattened_img.width) // 2
                img_y = y0 + padding_y
                page.paste(flattened_img, (img_x, img_y))

                label = os.path.splitext(os.path.basename(img_path))[0].replace("_", " ").upper()

                font_size = int(label_height)
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

    output_path = os.path.join(
        page_layout.OUTPUT_PATH,
        f"{calling_card_multi_layout.FILE_NAME}.pdf"
    )

    if pages:
        first_card = pages[0].convert("RGB")
        rest_cards = [card.convert("RGB") for card in pages[1:]]
        first_card.save(
            output_path,
            "PDF",
            resolution=page_layout.DPI,
            save_all=True,
            append_images=rest_cards
        )

def generate_tokens(page_layout: PageLayout, tokens_layout: TokensLayout):
    # generate white canvas and define print-safe area
    height = int(page_layout.HEIGHT_INCHES * page_layout.DPI)
    width = int(page_layout.WIDTH_INCHES * page_layout.DPI)
    margin_top = int(page_layout.MARGIN_TOP_INCHES * page_layout.DPI)
    margin_right = int(page_layout.MARGIN_RIGHT_INCHES * page_layout.DPI)
    margin_bottom = int(page_layout.MARGIN_BOTTOM_INCHES * page_layout.DPI)
    margin_left = int(page_layout.MARGIN_LEFT_INCHES * page_layout.DPI)
    page = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    usable_width = width - margin_left - margin_right
    usable_height = height - margin_top - margin_bottom

    # load and paste scissors icon
    scissors = Image.open(page_layout.SCISSORS_IMAGE_PATH).convert("RGBA")
    scissors_width, scissors_height = scissors.size
    scissors_width = int(usable_width * tokens_layout.SCISSORS_WIDTH_SCALE_FACTOR)
    scissors_height = int(usable_height * tokens_layout.SCISSORS_HEIGHT_SCALE_FACTOR)
    scissors = scissors.resize((scissors_width, scissors_height), Image.LANCZOS)
    flattened_scissors = Image.new("RGB", scissors.size, (255, 255, 255))
    flattened_scissors.paste(scissors, (0, 0), mask=scissors.getchannel("A"))
    page.paste(flattened_scissors, (margin_left, margin_top))

    # draw grid
    draw = ImageDraw.Draw(page)
    line_color = tokens_layout.GRID_LINE_COLOR
    line_thickness = int(tokens_layout.GRID_LINE_THICKNESS_INCHES * page_layout.DPI)
    cols = tokens_layout.GRID_COLS
    rows = tokens_layout.GRID_ROWS
    grid_x = margin_left
    grid_y = margin_top + scissors_height + int(tokens_layout.SCISSORS_BOTTOM_MARGIN_INCHES * page_layout.DPI)
    grid_height = usable_height - scissors_height - int(tokens_layout.SCISSORS_BOTTOM_MARGIN_INCHES * page_layout.DPI)
    cell_width = usable_width // cols
    cell_height = grid_height // rows

    for i in range(rows + 1):
        y_line = grid_y + i * cell_height
        x1, y1 = (grid_x, y_line)
        x2, y2 = (grid_x + cols * cell_width, y_line)
        total_length = int(hypot(x2 - x1, y2 - y1))
        dot_length = 5
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

    for j in range(cols + 1):
        x_line = grid_x + j * cell_width
        x1, y1 = (x_line, grid_y)
        x2, y2 = (x_line, grid_y + rows * cell_height)
        total_length = int(hypot(x2 - x1, y2 - y1))
        dot_length = 5
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

    padding_x = int(cell_width * tokens_layout.CELL_PADDING_X_RATIO)
    available_img_width = cell_width - 2 * padding_x
    token = Image.open(page_layout.TOKEN_IMAGE_PATH).convert("RGBA").resize((available_img_width, available_img_width), Image.LANCZOS)
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
    output_path = os.path.join(
        page_layout.OUTPUT_PATH,
        f"{tokens_layout.FILE_NAME}.pdf"
    )
    page.save(output_path, "PDF", dpi=(page_layout.DPI, page_layout.DPI))
