#dotted linee code
'''
def draw_dashed_line(draw, start, end, dash_length=10, gap_length=5, fill="black", width=1):
    from math import hypot

    # Distance between start and end
    total_length = hypot(end[0] - start[0], end[1] - start[1])

    # Direction vector
    dx = (end[0] - start[0]) / total_length
    dy = (end[1] - start[1]) / total_length

    pos = 0
    while pos < total_length:
        dash_start = (
            int(start[0] + dx * pos),
            int(start[1] + dy * pos)
        )
        pos += dash_length
        dash_end = (
            int(start[0] + dx * min(pos, total_length)),
            int(start[1] + dy * min(pos, total_length))
        )
        draw.line([dash_start, dash_end], fill=fill, width=width)
        pos += gap_length
'''


#draw_dashed_line(draw, (GRID_X, y), (GRID_X + GRID_WIDTH, y), 
                     #dash_length=15, gap_length=7, fill=GRID_LINE_COLOR, width=GRID_LINE_THICKNESS)

#draw_dashed_line(draw, (x, GRID_Y), (x, GRID_Y + GRID_HEIGHT),
                     #dash_length=15, gap_length=7, fill=GRID_LINE_COLOR, width=GRID_LINE_THICKNESS)