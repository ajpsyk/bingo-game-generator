from PIL import ImageDraw

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