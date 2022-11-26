from fpdf import FPDF
import re
from typing import Tuple

DOCUMENT_TITLE = 'My Document'

TOP_MARGIN = 10
SIDE_MARGIN = 20
RECT_SIZE = 20
NUM_RECTS_PER_ROW = 10
LINE_WIDTH = 0.5
ROW_GAP = 10
NUM_ROWS_PER_PAGE = 10

pdf = FPDF('portrait', 'mm', (SIDE_MARGIN * 2 + NUM_RECTS_PER_ROW *
           RECT_SIZE, TOP_MARGIN * 2 + NUM_ROWS_PER_PAGE * (RECT_SIZE + ROW_GAP)))

pdf.set_title(DOCUMENT_TITLE)
# make pdf chinese friendly
# add font support chinese
pdf.add_font('Noto Sans SC', '', 'AR PL UKai CN, Regular.ttf', uni=True)
pdf.set_font('Noto Sans SC', '', 50)


def add_rect(row_num):
    # there will be 10 rectangles in 1 row

    y = TOP_MARGIN + row_num * (RECT_SIZE + ROW_GAP)
    for i in range(10):
        pdf.set_line_width(LINE_WIDTH)
        pdf.rect(SIDE_MARGIN + i * RECT_SIZE, y, RECT_SIZE, RECT_SIZE, 'D')
        # draw an X inside the rectangle
        # set line type to dashed
        pdf.set_line_width(LINE_WIDTH / 3)
        pdf.dashed_line(SIDE_MARGIN + i * RECT_SIZE, y, SIDE_MARGIN + (i + 1)
                        * RECT_SIZE, y + RECT_SIZE, space_length=3, dash_length=1)
        pdf.dashed_line(SIDE_MARGIN + i * RECT_SIZE, y + RECT_SIZE, SIDE_MARGIN +
                        (i + 1) * RECT_SIZE, y, space_length=3, dash_length=1)


def parse(txt):
    # remove all characters that are not chinese
    txt = re.sub(r'[^\u4e00-\u9fff]', '', txt)
    # split into characters
    return list(txt)


def process(txt):
    characters = ''.join(list(set(parse(txt))))[:100]
    
    for i, char in enumerate(characters):
        if (i % NUM_ROWS_PER_PAGE == 0):
            pdf.add_page()
        add_rect(i % NUM_ROWS_PER_PAGE)
        # add the character
        pdf.set_xy(SIDE_MARGIN + RECT_SIZE / 2 - 5,
                   TOP_MARGIN + (i % NUM_ROWS_PER_PAGE) * (RECT_SIZE + ROW_GAP) + RECT_SIZE / 2 - 4)
        # set text color to black
        pdf.set_text_color(0, 0, 0)
        pdf.cell(10, 10, char, 0, 0, 'C')

        for j in range(1, 3):
            pdf.set_xy(SIDE_MARGIN + (j % NUM_RECTS_PER_ROW) * RECT_SIZE + RECT_SIZE / 2 - 5,
                       TOP_MARGIN + (i % NUM_ROWS_PER_PAGE) * (RECT_SIZE + ROW_GAP) + RECT_SIZE / 2 - 4)
            # set text color light grey
            pdf.set_text_color(190, 190, 190)
            pdf.cell(10, 10, char, 0, 0, 'C')

    return pdf.output(dest='S')  # type: ignore

# Health check
if __name__ == "__main__":
    from io import BytesIO

    pdf = process('你好')
    pdf_io = BytesIO(pdf.encode('latin-1'))
    pdf_io.seek(0)

    with open('./static/pdf/test.pdf', 'wb') as f:
        f.write(pdf_io.read())
