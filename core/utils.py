from config.layouts import PageLayout
from PIL import Image, ImageDraw, ImageFont
import os
import random
from math import ceil
from pypdf import PdfWriter, PdfReader

def create_canvas(page_layout: PageLayout, layout):
    # generate blank canvas and define print-safe area
    if type(layout).__name__ == "BingoCardMultiLayout":
        height = int(page_layout.WIDTH_INCHES * page_layout.DPI)
        width = int(page_layout.HEIGHT_INCHES * page_layout.DPI)

        top_margin = int(page_layout.MARGIN_TOP_INCHES * page_layout.DPI * 2.5)
        right_margin = int(page_layout.MARGIN_RIGHT_INCHES * page_layout.DPI)
        bottom_margin = int(page_layout.MARGIN_TOP_INCHES * page_layout.DPI * 2.5)
        left_margin = int(page_layout.MARGIN_LEFT_INCHES * page_layout.DPI)

        base_card = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        usable_width = (width - 2 * left_margin - 2 * right_margin) // 2
        usable_height = height - top_margin - bottom_margin
        x_offset = 2 * left_margin + right_margin + usable_width

        # load and paste frame
        if layout.FRAME_ENABLED:
            frame = Image.open(page_layout.FRAME_IMAGE_PATH).convert("RGBA").resize((usable_width, usable_height), Image.LANCZOS)
            flattened_frame = Image.new("RGB", frame.size, (255, 255, 255))
            flattened_frame.paste(frame, (0,0), mask=frame.getchannel("A"))
            base_card.paste(flattened_frame, (left_margin, top_margin))
            base_card.paste(flattened_frame,  (x_offset,  top_margin))
            frame_padding = {
                "top": int(layout.FRAME_PADDING_TOP_INCHES * page_layout.DPI),
                "right": int(layout.FRAME_PADDING_RIGHT_INCHES * page_layout.DPI),
                "bottom": int(layout.FRAME_PADDING_BOTTOM_INCHES * page_layout.DPI),
                "left": int(layout.FRAME_PADDING_LEFT_INCHES * page_layout.DPI)
            }
        else:
            frame_padding = {"top": 0, "right": 0, "bottom": 0, "left": 0}


        # define content area
        content_x = left_margin + frame_padding["left"]
        content_2x = x_offset + frame_padding["left"]
        content_y = top_margin + frame_padding["top"]
        content_width = usable_width - frame_padding["left"] - frame_padding["right"]
        content_height = usable_height - frame_padding["top"] - frame_padding["bottom"]

        return  base_card, content_x, content_y, content_2x, content_width, content_height

    else:
        height = int(page_layout.HEIGHT_INCHES * page_layout.DPI)
        width = int(page_layout.WIDTH_INCHES * page_layout.DPI)
        top_margin = int(page_layout.MARGIN_TOP_INCHES * page_layout.DPI)
        right_margin = int(page_layout.MARGIN_RIGHT_INCHES * page_layout.DPI)
        bottom_margin = int(page_layout.MARGIN_BOTTOM_INCHES * page_layout.DPI)
        left_margin = int(page_layout.MARGIN_LEFT_INCHES * page_layout.DPI)

        base_card = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        
        usable_width = width - left_margin - right_margin
        usable_height = height - top_margin - bottom_margin

        # load and paste frame (optional)
        if layout.FRAME_ENABLED:
            frame = Image.open(page_layout.FRAME_IMAGE_PATH).convert("RGBA").resize((usable_width, usable_height), Image.LANCZOS)
            flattened_frame = Image.new("RGB", frame.size, (255, 255, 255))
            flattened_frame.paste(frame, (0,0), mask=frame.getchannel("A"))
            base_card.paste(flattened_frame, (left_margin, top_margin))
            frame_padding = {
                "top": int(layout.FRAME_PADDING_TOP_INCHES * page_layout.DPI),
                "right": int(layout.FRAME_PADDING_RIGHT_INCHES * page_layout.DPI),
                "bottom": int(layout.FRAME_PADDING_BOTTOM_INCHES * page_layout.DPI),
                "left": int(layout.FRAME_PADDING_LEFT_INCHES * page_layout.DPI)
            }
        else:
            frame_padding = {"top": 0, "right": 0, "bottom": 0, "left": 0}
        
        # define content area
        content_x = left_margin + frame_padding["left"]
        content_y = top_margin + frame_padding["top"]
        content_width = usable_width - frame_padding["left"] - frame_padding["right"]
        content_height = usable_height - frame_padding["top"] - frame_padding["bottom"]
        
        return base_card, content_x, content_y, content_width, content_height

def load_and_paste_header(header_path, layout, canvas, usable_width, x, y):
    # load and paste header
    header = Image.open(header_path).convert("RGBA")
    header_width, header_height = header.size
    if header_width != usable_width:
        scale_factor = usable_width / header_width
        header_width = int(header_width * scale_factor)
        header_height = int(header_height * scale_factor)
        header = header.resize((header_width, header_height), Image.LANCZOS)
    flattened_header = Image.new("RGB", header.size, (255, 255, 255))
    flattened_header.paste(header, (0, 0), mask=header.getchannel("A"))
    canvas.paste(flattened_header, (x, y))
    return header_height

def draw_grid(page_layout, layout, base_card, content_x, content_y, content_width, content_height, header_height):
    # draw grid
    draw = ImageDraw.Draw(base_card)
    line_color = layout.GRID_LINE_COLOR
    line_thickness = int(layout.GRID_LINE_THICKNESS_INCHES * page_layout.DPI)
    grid_top_margin = int(layout.GRID_MARGIN_TOP_INCHES * page_layout.DPI)
    cols = layout.GRID_COLS
    rows = layout.GRID_ROWS
    grid_x = content_x
    grid_y = content_y + header_height + grid_top_margin
    grid_height = content_height - header_height - grid_top_margin
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
    return cell_width, cell_height, grid_x, grid_y

def load_images_and_labels(page_layout, layout, cell_height, cell_width):
    # load images and labels
    padding_y = int(cell_height * layout.CELL_PADDING_Y_RATIO)
    padding_x = int(cell_width * layout.CELL_PADDING_X_RATIO)
    label_height = int(cell_height * layout.LABEL_HEIGHT_RATIO)
    gap = int(label_height * layout.LABEL_GAP_RATIO)
    available_img_height = cell_height - 2 * padding_y - gap - label_height
    available_img_width = cell_width - 2 * padding_x


    flattened_fs = None
    if layout.HAS_FREE_SPACE and page_layout.FREE_SPACE_IMAGE_PATH:
        free_space_path = page_layout.FREE_SPACE_IMAGE_PATH
        free_space_img = Image.open(free_space_path).convert("RGBA").resize(
            (available_img_width, available_img_height), Image.LANCZOS
        )
        flattened_fs = Image.new("RGB", free_space_img.size, (255, 255, 255))
        flattened_fs.paste(free_space_img, (0, 0), mask=free_space_img.getchannel("A"))
    
    loaded_images = {}
    image_directory = page_layout.BINGO_IMAGES_PATH
    image_files = os.listdir(image_directory)

    for file in image_files:
        path = os.path.join(image_directory, file)
        img = Image.open(path).convert("RGBA").resize((available_img_width, available_img_height), Image.LANCZOS)
        flattened_img = Image.new("RGB", img.size, (255, 255, 255))
        flattened_img.paste(img, (0,0), mask=img.getchannel("A"))
        label = os.path.splitext(os.path.basename(path))[0].replace("_", " ").upper()
        loaded_images[label] = flattened_img
    return loaded_images, flattened_fs

def shuffle_images(layout, loaded_images):
    # shuffle images and labels
    seen_permutations = set()
    labels = list(loaded_images.keys())
    num_cells = layout.GRID_ROWS * layout.GRID_COLS - 1 # subtract 1 for free space
    while len(seen_permutations) < layout.CARD_AMOUNT:
        selected = tuple(random.sample(labels, num_cells))
        if selected not in seen_permutations:
            seen_permutations.add(selected)
    return seen_permutations

def paste_single_card(page_layout, card, draw, loaded_images, free_space_img, image_set, cell_width, cell_height, grid_x, grid_y, layout):
    cols = layout.GRID_COLS
    rows = layout.GRID_ROWS
    label_height = cell_height * layout.LABEL_HEIGHT_RATIO
    padding_y = int(cell_height * layout.CELL_PADDING_Y_RATIO)
    padding_x = int(cell_width * layout.CELL_PADDING_X_RATIO)
    gap = int(label_height * layout.LABEL_GAP_RATIO)
    image_iter = iter(image_set)

    center_x = grid_x + 2 * cell_width
    center_y = grid_y + 2 * cell_height
    if free_space_img:
        fs_x = center_x + (cell_width - free_space_img.width) // 2
        fs_y = center_y + (cell_height - free_space_img.height) // 2

    font = ImageFont.truetype(page_layout.FONT_PATH, label_height)

    for row in range(rows):
        for col in range(cols):
            if free_space_img and row == 2 and col == 2:
                card.paste(free_space_img, (fs_x, fs_y))
            else:
                label = next(image_iter)
                image = loaded_images[label]

                x0 = grid_x + col * cell_width
                y0 = grid_y + row * cell_height
                img_x = x0 + (cell_width - image.width) // 2
                img_y = y0 + padding_y

                card.paste(image, (img_x, img_y))

                available_width = cell_width - 2 * padding_x
                text_width = font.getlength(label)
                text_y = img_y + image.height + gap

                if text_width > available_width:
                    spacing = available_width / len(label)
                    start_x = x0 + (cell_width - available_width) / 2

                    for i, char in enumerate(label):
                        char_width = font.getlength(char)
                        char_x = start_x + (i + 0.5) * spacing - char_width / 2
                        draw.text((char_x, text_y), char, font=font, fill=layout.LABEL_COLOR)
                else:
                    text_x = x0 + (cell_width - text_width) / 2
                    draw.text((text_x, text_y), label, font=font, fill=layout.LABEL_COLOR)


def paste_images(page_layout, layout, base_card, loaded_images, free_space_img, image_sets, cell_width, cell_height, grid_x, grid_y):
    bingo_cards = []
    for image_set in image_sets:
        card = base_card.copy()
        draw = ImageDraw.Draw(card)
        paste_single_card(page_layout, card, draw, loaded_images, free_space_img, image_set, cell_width, cell_height, grid_x, grid_y, layout)
        bingo_cards.append(card)
    return bingo_cards

def save_as_pdf(page_layout: PageLayout, layout, cards):
    cards_per_pdf = ceil(len(cards) / layout.NUM_PDFS)
    chunks = [cards[i:i+cards_per_pdf] for i in range(0, len(cards), cards_per_pdf)]

    dir_path = page_layout.OUTPUT_PATH if page_layout.OUTPUT_PATH else os.getcwd()
    base_filename = f"{page_layout.THEME}_{layout.FILE_NAME}.pdf"
    base_output_path = os.path.join(dir_path, base_filename)

    for i, chunk in enumerate(chunks, start=1):
        first_card = chunk[0].convert("RGB")
        rest_cards = [card.convert("RGB") for card in chunk[1:]]

        if layout.NUM_PDFS > 1:
            base, ext = os.path.splitext(base_output_path)
            output_path = f"{base}_Part{i}{ext}"
        else:
            # If only 1 PDF, don't add _Part1 suffix, use base filename directly
            output_path = base_output_path

        first_card.save(
            output_path,
            "PDF",
            resolution=page_layout.DPI,
            save_all=True,
            append_images=rest_cards
        )



def draw_debug_box(draw, x0, y0, x1, y1, color="red", thickness=1):
    """
    Draws a rectangle outline for visual debugging.

    Args:
        draw: PIL.ImageDraw.Draw object.
        x0, y0, x1, y1: Rectangle coordinates (top-left to bottom-right).
        color: Outline color.
        thickness: Outline thickness in pixels.
    """
    draw.rectangle([(x0, y0), (x1, y1)], outline=color, width=thickness)

def fit_text_to_width(text, font_loader, max_width, initial_size, min_size=8):
    """
    Dynamically adjusts font size to fit text within max_width.
    
    Parameters:
        text (str): The text string to measure.
        font_loader (callable): A function like lambda size: ImageFont.truetype(path, size).
        max_width (int): The maximum allowed pixel width.
        initial_size (int): Starting font size.
        min_size (int): Minimum font size allowed.

    Returns:
        font (ImageFont.FreeTypeFont): A font instance that fits within max_width.
    """
    size = initial_size
    font = font_loader(size)
    text_width = font.getbbox(text)[2] - font.getbbox(text)[0]

    while text_width > max_width and size > min_size:
        size -= 1
        font = font_loader(size)
        text_width = font.getbbox(text)[2] - font.getbbox(text)[0]

    return font

def merge_howto_tokens_callingcards(page_layout, single_layout, multi_layout, tokens_layout):
    output_path = page_layout.OUTPUT_PATH
    theme = page_layout.THEME.strip()
    merged_filename = "Calling Cards, Tokens, and How To's.pdf"
    full_output_path = os.path.join(output_path, merged_filename)

    pdf_paths = [
        page_layout.INSTRUCTIONS_PATH,
        os.path.join(output_path, f"{tokens_layout.FILE_NAME}.pdf"),  # no theme prefix
        os.path.join(output_path, f"{theme}_{single_layout.FILE_NAME}.pdf"),  # theme prefix here only
        os.path.join(output_path, f"{multi_layout.FILE_NAME}.pdf"),  # no theme prefix
    ]

    writer = PdfWriter()
    print("Merging these files:")
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        else:
            print(f"Warning: PDF not found for merging: {pdf_path}")

    with open(full_output_path, "wb") as f_out:
        writer.write(f_out)
    print(f"Merged PDF saved to: {full_output_path}")

    # Clean up generated PDFs except instructions/how-to
    files_to_cleanup = [
        os.path.join(output_path, f"{tokens_layout.FILE_NAME}.pdf"),
        os.path.join(output_path, f"{theme}_{single_layout.FILE_NAME}.pdf"),
        os.path.join(output_path, f"{multi_layout.FILE_NAME}.pdf"),
    ]

    for file_path in files_to_cleanup:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted temporary file: {file_path}")
