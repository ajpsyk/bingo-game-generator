from PIL import ImageDraw

def draw_margin_box(draw, layout, color="#FF0000", thickness=1):
    """
    Draws a debug rectangle showing the printable margin area.
    """
    x0 = layout.MARGIN
    y0 = layout.MARGIN
    x1 = layout.WIDTH_PIXELS - layout.MARGIN
    y1 = layout.HEIGHT_PIXELS - layout.MARGIN

    draw.line([(x0, y0), (x1, y0)], fill=color, width=thickness)
    draw.line([(x0, y1), (x1, y1)], fill=color, width=thickness)
    draw.line([(x0, y0), (x0, y1)], fill=color, width=thickness)
    draw.line([(x1, y0), (x1, y1)], fill=color, width=thickness)