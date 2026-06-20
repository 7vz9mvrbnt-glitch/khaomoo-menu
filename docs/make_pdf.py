#!/usr/bin/env python3
"""
Generate 3 E-book PDFs for QR Menu service packages.
Uses fpdf2 with Sarabun Thai fonts -- no HTML/weasyprint.
Fixes: (1) increased line heights for Thai tone marks, (2) accurate tip_box sizing.
"""

from fpdf import FPDF
from fpdf.enums import RenderStyle

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
SAGE   = (135, 160, 128)
SAGE_L = (236, 242, 235)
SAGE_D = (85,  114,  82)
CREAM  = (248, 245, 239)
WHITE  = (255, 255, 255)
DARK   = (42,   42,  42)
MID    = (94,   94,  94)
BORDER = (212, 226, 210)

FONT_REG  = '/tmp/fonts/Sarabun-Regular.ttf'
FONT_BOLD = '/tmp/fonts/Sarabun-Bold.ttf'


class EbookPDF(FPDF):
    """fpdf2 subclass with helpers for the QR Menu e-book series."""

    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.add_font('SB', '',  FONT_REG)
        self.add_font('SB', 'B', FONT_BOLD)
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(18, 18, 18)

    # ------------------------------------------------------------------
    # Cover page
    # ------------------------------------------------------------------
    def cover(self, badge, title1, title2, subtitle, line2, price, days):
        self.add_page()
        self.set_auto_page_break(False)

        # Full sage green background rect
        self.set_fill_color(*SAGE)
        self.rect(0, 0, 210, 260, 'F')

        # White footer
        self.set_fill_color(*WHITE)
        self.rect(0, 260, 210, 37, 'F')

        # Badge -- y=30
        self.set_text_color(*WHITE)
        self.set_font('SB', '', 11)
        self.set_xy(0, 30)
        self.cell(210, 8, badge, align='C')

        # Title1 -- y=55
        self.set_font('SB', 'B', 36)
        self.set_xy(0, 55)
        self.cell(210, 12, title1, align='C')

        # Title2 -- y=78
        self.set_xy(0, 78)
        self.cell(210, 12, title2, align='C')

        # Subtitle -- y=105
        self.set_font('SB', '', 15)
        self.set_xy(0, 105)
        self.cell(210, 8, subtitle, align='C')

        # Line2 -- y=118
        self.set_font('SB', '', 13)
        self.set_xy(0, 118)
        self.cell(210, 8, line2, align='C')

        # White pill for price -- x=60, y=150, w=90, h=18, r=9
        self.set_fill_color(*WHITE)
        self.set_draw_color(*WHITE)
        self._draw_rounded_rect(60, 150, 90, 18, RenderStyle.DF, round_corners=True, r=9)

        # Price text centered in pill -- y=155
        self.set_text_color(*SAGE_D)
        self.set_font('SB', 'B', 20)
        self.set_xy(0, 155)
        self.cell(210, 8, price, align='C')

        # Days -- y=175
        self.set_text_color(*WHITE)
        self.set_font('SB', '', 12)
        self.set_xy(0, 175)
        self.cell(210, 8, days, align='C')

        # Footer disclaimer -- y=265
        self.set_text_color(*MID)
        self.set_font('SB', '', 11)
        self.set_xy(0, 265)
        self.cell(210, 8, 'คู่มือนี้จัดทำขึ้นสำหรับลูกค้าเท่านั้น', align='C')

        # Reset for next pages
        self.set_auto_page_break(auto=True, margin=20)

    # ------------------------------------------------------------------
    # TOC page
    # ------------------------------------------------------------------
    def toc_page(self, chapters):
        """chapters = list of (num_str, title, subtitle)"""
        self.add_page()
        # CREAM background
        self.set_fill_color(*CREAM)
        self.rect(0, 0, 210, 297, 'F')

        self.set_text_color(*DARK)
        self.set_font('SB', 'B', 22)
        self.set_xy(18, 20)
        self.cell(174, 12, 'สารบัญ', align='L')

        # Divider
        self.set_draw_color(*BORDER)
        self.line(18, 34, 192, 34)

        y = 42
        for num, title, subtitle in chapters:
            # Sage circle for number
            self.set_fill_color(*SAGE)
            self.ellipse(18, y, 10, 10, 'F')

            self.set_text_color(*WHITE)
            self.set_font('SB', 'B', 10)
            self.set_xy(18, y + 1)
            self.cell(10, 8, num, align='C')

            # Chapter title
            self.set_text_color(*DARK)
            self.set_font('SB', 'B', 13)
            self.set_xy(32, y)
            self.cell(160, 6, title, align='L')

            # Chapter subtitle
            self.set_text_color(*MID)
            self.set_font('SB', '', 11)
            self.set_xy(32, y + 6)
            self.cell(160, 6, subtitle, align='L')

            # Light divider
            self.set_draw_color(*BORDER)
            self.line(18, y + 15, 192, y + 15)

            y += 20

    # ------------------------------------------------------------------
    # Chapter header
    # ------------------------------------------------------------------
    def ch_header(self, num, title, subtitle):
        """New page with sage green header band, content starts at y=85."""
        self.add_page()

        # Sage green header band -- 72mm tall
        self.set_fill_color(*SAGE)
        self.rect(0, 0, 210, 72, 'F')

        # Chapter number
        self.set_text_color(*WHITE)
        self.set_font('SB', '', 11)
        self.set_xy(18, 14)
        self.cell(174, 8, num, align='L')

        # Title
        self.set_font('SB', 'B', 26)
        self.set_xy(18, 26)
        self.cell(174, 12, title, align='L')

        # Subtitle (9mm line height for Thai tone marks)
        self.set_font('SB', '', 13)
        self.set_xy(18, 50)
        self.set_auto_page_break(False)
        self.multi_cell(174, 9, subtitle, align='L')
        self.set_auto_page_break(True, margin=20)

        # Move to content area
        self.set_xy(18, 85)
        self.set_text_color(*DARK)

    # ------------------------------------------------------------------
    # Section heading
    # ------------------------------------------------------------------
    def section_heading(self, text):
        self.ln(3)
        self.set_text_color(*SAGE_D)
        self.set_font('SB', 'B', 14)
        self.set_x(18)
        self.cell(174, 8, text, align='L', new_x='LMARGIN', new_y='NEXT')
        # Small underline
        y = self.get_y()
        self.set_draw_color(*SAGE)
        self.line(18, y, 192, y)
        self.ln(3)
        self.set_text_color(*DARK)

    # ------------------------------------------------------------------
    # Body text  (8.5mm line height prevents Thai tone mark overlap)
    # ------------------------------------------------------------------
    def body(self, text):
        self.set_text_color(*DARK)
        self.set_font('SB', '', 12)
        self.set_x(18)
        self.multi_cell(174, 8.5, text, align='L')
        self.ln(2)

    # ------------------------------------------------------------------
    # Feature bullet item
    # ------------------------------------------------------------------
    def feature(self, title, desc):
        y = self.get_y()
        # Bullet dot
        self.set_fill_color(*SAGE)
        self.ellipse(18, y + 3, 4, 4, 'F')

        # Title (8.5mm line height)
        self.set_text_color(*DARK)
        self.set_font('SB', 'B', 12)
        self.set_xy(25, y)
        self.multi_cell(167, 8.5, title, align='L')

        # Description (7.5mm line height)
        if desc:
            self.set_text_color(*MID)
            self.set_font('SB', '', 11)
            self.set_x(25)
            self.multi_cell(167, 7.5, desc, align='L')

        self.ln(2)

    # ------------------------------------------------------------------
    # Numbered step
    # ------------------------------------------------------------------
    def step(self, num, title, desc):
        y = self.get_y()

        # Circle with number
        self.set_fill_color(*SAGE_D)
        self.ellipse(18, y, 8, 8, 'F')
        self.set_text_color(*WHITE)
        self.set_font('SB', 'B', 9)
        self.set_xy(18, y + 0.5)
        self.cell(8, 7, str(num), align='C')

        # Title (8.5mm line height)
        self.set_text_color(*DARK)
        self.set_font('SB', 'B', 12)
        self.set_xy(29, y)
        self.multi_cell(163, 8.5, title, align='L')

        # Description (7.5mm line height)
        if desc:
            self.set_text_color(*MID)
            self.set_font('SB', '', 11)
            self.set_x(29)
            self.multi_cell(163, 7.5, desc, align='L')

        self.ln(2)

    # ------------------------------------------------------------------
    # Checklist item
    # ------------------------------------------------------------------
    def checklist_item(self, label, desc):
        y = self.get_y()

        # Checkbox square
        self.set_draw_color(*SAGE)
        self.set_fill_color(*SAGE_L)
        self.rect(18, y + 1, 6, 6, 'FD')

        # Checkmark inside
        self.set_text_color(*SAGE_D)
        self.set_font('SB', 'B', 9)
        self.set_xy(18, y)
        self.cell(6, 8, 'v', align='C')

        # Label (8.5mm line height)
        self.set_text_color(*DARK)
        self.set_font('SB', 'B', 12)
        self.set_xy(27, y)
        self.multi_cell(165, 8.5, label, align='L')

        # Description (7.5mm line height)
        if desc:
            self.set_text_color(*MID)
            self.set_font('SB', '', 11)
            self.set_x(27)
            self.multi_cell(165, 7.5, desc, align='L')

        self.ln(2)

    # ------------------------------------------------------------------
    # FAQ item
    # ------------------------------------------------------------------
    def faq(self, q, a):
        # Question
        self.set_text_color(*SAGE_D)
        self.set_font('SB', 'B', 12)
        self.set_x(18)
        self.multi_cell(174, 8.5, 'Q: ' + q, align='L')

        # Answer
        self.set_text_color(*DARK)
        self.set_font('SB', '', 12)
        self.set_x(18)
        self.multi_cell(174, 8.5, 'A: ' + a, align='L')
        self.ln(3)

    # ------------------------------------------------------------------
    # Tip box (SAGE_L background) — dry_run for accurate height
    # ------------------------------------------------------------------
    def tip_box(self, text):
        LH = 8.0       # line height for tip text (11pt)
        inner_w = 160  # text width inside left bar
        PAD = 5        # mm padding top and bottom

        self.set_font('SB', '', 11)

        # Measure exact line count without rendering
        try:
            lines = self.multi_cell(inner_w, LH, text, dry_run=True, output='LINES')
            n_lines = len(lines) if isinstance(lines, list) else text.count('\n') + 2
        except Exception:
            n_lines = max(2, text.count('\n') + 1 + len(text) // 60)

        box_h = n_lines * LH + PAD * 2

        y = self.get_y()
        if y + box_h > 270:
            self.add_page()
            y = self.get_y()

        # Draw rounded rect background
        self.set_fill_color(*SAGE_L)
        self.set_draw_color(*BORDER)
        self._draw_rounded_rect(18, y, 174, box_h, RenderStyle.DF, round_corners=True, r=4)

        # Left accent bar
        self.set_fill_color(*SAGE)
        self.rect(18, y, 4, box_h, 'F')

        # Write text — disable auto page break to keep within drawn box
        self.set_auto_page_break(False)
        self.set_text_color(*DARK)
        self.set_font('SB', '', 11)
        self.set_xy(26, y + PAD)
        self.multi_cell(inner_w, LH, text, align='L')
        self.set_auto_page_break(True, margin=20)

        # Advance past box
        self.set_xy(18, y + box_h + 4)

    # ------------------------------------------------------------------
    # Code box (CREAM background)
    # ------------------------------------------------------------------
    def code_box(self, text):
        LH = 6.5
        inner_w = 160
        lines_count = text.count('\n') + 1
        box_h = lines_count * LH + 10

        y = self.get_y()
        if y + box_h > 270:
            self.add_page()
            y = self.get_y()

        # Draw rounded rect
        self.set_fill_color(*CREAM)
        self.set_draw_color(*BORDER)
        self._draw_rounded_rect(18, y, 174, box_h, RenderStyle.DF, round_corners=True, r=4)

        # Left accent bar (dark)
        self.set_fill_color(*SAGE_D)
        self.rect(18, y, 4, box_h, 'F')

        # Write text — disable auto page break to keep within drawn box
        self.set_auto_page_break(False)
        self.set_text_color(*DARK)
        self.set_font('SB', '', 10)
        self.set_xy(26, y + 5)
        self.multi_cell(inner_w, LH, text, align='L')
        self.set_auto_page_break(True, margin=20)

        # Advance past box
        self.set_xy(18, y + box_h + 4)
        self.ln(1)

    # ------------------------------------------------------------------
    # Thank-you page
    # ------------------------------------------------------------------
    def thanks_page(self, line1, line2, line3, upgrade=None):
        self.add_page()
        self.set_auto_page_break(False)

        # Full sage background
        self.set_fill_color(*SAGE)
        self.rect(0, 0, 210, 297, 'F')

        # Star symbol
        self.set_text_color(*WHITE)
        self.set_font('SB', 'B', 48)
        self.set_xy(0, 80)
        self.cell(210, 20, '*', align='C')

        # line1
        self.set_font('SB', 'B', 24)
        self.set_xy(0, 112)
        self.cell(210, 12, line1, align='C')

        # line2
        self.set_font('SB', '', 15)
        self.set_xy(0, 130)
        self.cell(210, 9, line2, align='C')

        # line3
        self.set_xy(0, 143)
        self.cell(210, 9, line3, align='C')

        # Upgrade box if provided
        if upgrade:
            self.set_fill_color(*WHITE)
            self.set_draw_color(*WHITE)
            self._draw_rounded_rect(25, 168, 160, 32, RenderStyle.DF, round_corners=True, r=6)
            self.set_text_color(*SAGE_D)
            self.set_font('SB', '', 11)
            self.set_xy(28, 172)
            self.multi_cell(154, 8, upgrade, align='C')

        # Footer
        self.set_text_color(*WHITE)
        self.set_font('SB', '', 10)
        self.set_xy(0, 270)
        self.cell(210, 8, 'khaomoo-menu.com  |  LINE: @khaomoo', align='C')

        self.set_auto_page_break(auto=True, margin=20)


# ===========================================================================
# Book 1 -- Basic
# ===========================================================================
def build_basic():
    pdf = EbookPDF()

    pdf.cover(
        badge='E-Book · แพ็ก 1 · Basic',
        title1='คู่มือการใช้งาน',
        title2='เมนู QR Code',
        subtitle='เมนูออนไลน์สำหรับร้านอาหาร',
        line2='สวยงาม · พิมพ์ได้ · ใช้ง่าย',
        price='990 บาท',
        days='ได้งานภายใน 2 วัน · แก้ไขฟรี 1 ครั้ง',
    )

    pdf.toc_page([
        ('1', 'ยินดีต้อนรับ! คุณได้อะไรบ้าง?', 'ภาพรวมสิ่งที่ได้รับในแพ็กนี้'),
        ('2', 'ข้อมูลที่ต้องเตรียมส่งให้เรา', 'Checklist ครบชุด ก่อนเริ่มงาน'),
        ('3', 'วิธีใช้ QR Code ที่ร้าน', 'ติดโต๊ะ -> ลูกค้าสแกน -> ดูเมนู'),
        ('4', 'คำถามที่พบบ่อย', 'ปัญหาที่มักเจอ และวิธีแก้ไข'),
    ])

    # Chapter 1
    pdf.ch_header('01 · บทที่หนึ่ง', 'ยินดีต้อนรับ!', 'คุณได้อะไรบ้าง?')
    pdf.body('ขอบคุณที่เลือกใช้บริการครับ ในแพ็กนี้คุณจะได้รับ เมนูอาหารออนไลน์พร้อมใช้งาน ที่ลูกค้าสแกน QR Code แล้วดูเมนูได้ทันทีบนมือถือ โดยไม่ต้องดาวน์โหลดแอปใด ๆ')
    pdf.section_heading('สิ่งที่คุณได้รับในแพ็กนี้')
    pdf.feature('เมนูออนไลน์สูงสุด 20 รายการ พร้อมรูปภาพ', 'แสดงรูปอาหาร ชื่อ ราคา และคำอธิบาย ดูสวยงามบนมือถือทุกรุ่น')
    pdf.feature('แยกหมวดหมู่ กรองเมนูได้', 'ลูกค้ากดเลือกหมวดได้ทันที เช่น ของทานเล่น เครื่องดื่ม หาเมนูเจอเร็วขึ้น')
    pdf.feature('QR Code ความละเอียดสูง พิมพ์ได้ทุกขนาด', 'ไฟล์ PNG ขนาดใหญ่ พิมพ์บนกระดาษ สติกเกอร์ อคริลิค หรือกรอบได้เลย')
    pdf.feature('ลิงก์เมนูออนไลน์', 'ส่งลิงก์ผ่าน LINE / Facebook ให้ลูกค้าเปิดดูได้โดยไม่ต้องสแกน QR')
    pdf.feature('แก้ไขฟรี 1 ครั้ง (ภายใน 30 วัน)', 'ขอแก้ชื่อเมนู ราคา หรือรูปภาพได้ 1 รอบ หลังจากนั้นคิดเพิ่มตามงาน')
    pdf.ln(2)
    pdf.tip_box('เมนูสวยงาม ดูมืออาชีพ ลูกค้าดูรูปก่อนสั่ง ตัดสินใจเร็วขึ้น ยอดขายดีขึ้น')
    pdf.tip_box('เปรียบเทียบ: เมนูกระดาษพอราคาเปลี่ยน ต้องพิมพ์ใหม่ทั้งเล่ม แต่เมนู QR Code ส่งข้อมูลให้เราแก้ ราคาใหม่ขึ้นทันที ไม่ต้องพิมพ์ซ้ำ ประหยัดค่าพิมพ์ระยะยาว')

    # Chapter 2
    pdf.ch_header('02 · บทที่สอง', 'ข้อมูลที่ต้องเตรียม ส่งให้เรา', 'รวบรวมสิ่งเหล่านี้ก่อน แล้วส่งให้เราทาง LINE')
    pdf.body('ก่อนเราเริ่มทำงาน คุณต้องส่งข้อมูลเหล่านี้มาให้ก่อนนะครับ ยิ่งข้อมูลครบ งานยิ่งเสร็จเร็ว')
    pdf.section_heading('Checklist ข้อมูลที่ต้องส่ง')
    pdf.checklist_item('ชื่อร้าน', 'ชื่อที่ต้องการแสดงในเมนู เช่น ร้านข้าวขาหมูต้นตำรับ')
    pdf.checklist_item('รายการเมนูทั้งหมด (สูงสุด 20 รายการ)', 'ชื่อเมนู + ราคา + หมวดหมู่ ส่งเป็น Excel, Note, หรือถ่ายรูปเมนูเดิมมาได้เลย')
    pdf.checklist_item('รูปอาหาร (ถ้ามี)', 'รูปละเอียด สว่าง พื้นหลังสะอาด ส่งเป็น JPG/PNG ถ่ายจากมือถือได้เลย')
    pdf.checklist_item('โลโก้ร้าน (ถ้ามี)', 'ไฟล์ PNG หรือ JPG โลโก้หน้าร้าน หรือตราสินค้า')
    pdf.checklist_item('สีหลักของร้าน', 'เช่น แดงเลือดหมู น้ำตาลโกโก้ หรือ code สี #XXXXXX ก็ได้')
    pdf.ln(2)
    pdf.tip_box('เคล็ดลับถ่ายรูปอาหาร: ถ่ายในที่แสงสว่าง ไม่ต้องมีกล้องแพง ใส่ในจาน/ชาม ให้เห็นหน้าอาหาร พื้นหลังสีเรียบหรือโต๊ะไม้ดูดีมาก')
    pdf.tip_box('ยังไม่มีรูปก็ส่งได้: ส่งข้อมูลอื่นมาก่อนได้เลยครับ เราจะใส่รูป placeholder ไว้ก่อน แล้วค่อยส่งรูปจริงมาทีหลัง (นับเป็น 1 ครั้งของสิทธิ์แก้ไขฟรี)')

    # Chapter 3
    pdf.ch_header('03 · บทที่สาม', 'วิธีใช้ QR Code ที่ร้าน', 'ตั้งแต่พิมพ์ QR Code ไปจนถึงลูกค้าสแกนดูเมนู')
    pdf.section_heading('ขั้นตอนฝั่งร้าน -- ติดตั้ง QR Code')
    pdf.step(1, 'รับไฟล์ QR Code จากเราทาง LINE', 'เราส่งไฟล์ PNG ให้ทาง LINE พร้อมลิงก์เมนูด้วย')
    pdf.step(2, 'พิมพ์ QR Code ออกมา', 'พิมพ์บนกระดาษธรรมดา สติกเกอร์ หรืออคริลิคก็ได้ ขนาดแนะนำ 8x8 ซม. ขึ้นไป')
    pdf.step(3, 'ติดที่โต๊ะหรือเคาน์เตอร์', 'วางให้ลูกค้าเห็นชัดเจน ไม่อยู่ในที่มืด ใส่กรอบอคริลิคดูดีและทนทาน')
    pdf.ln(2)
    pdf.tip_box('แนะนำติดทุกโต๊ะ: ถ้ามีหลายโต๊ะ พิมพ์หลายแผ่นได้เลย ใช้ QR Code ไฟล์เดิมทั้งหมด ลิงก์เดียวกัน')
    pdf.section_heading('ขั้นตอนฝั่งลูกค้า -- สแกนดูเมนู')
    pdf.step(1, 'เปิดกล้องมือถือปกติ (ไม่ต้องโหลดแอปพิเศษ)', 'ทั้ง iPhone และ Android ใช้กล้องธรรมดาได้เลย')
    pdf.step(2, 'ชี้กล้องไปที่ QR Code บนโต๊ะ', 'กล้องจะจับ QR Code อัตโนมัติ ไม่ต้องกดอะไร')
    pdf.step(3, 'กดลิงก์ที่ขึ้นมาบนหน้าจอ', 'กด Open / เปิดลิงก์ เมนูเปิดในเบราว์เซอร์ทันที')
    pdf.step(4, 'ดูเมนู เลือกรายการ แจ้งพนักงาน', 'ดูรูปอาหาร ราคา อ่านคำอธิบาย แล้วแจ้งพนักงานสั่ง')
    pdf.ln(2)
    pdf.tip_box('ถ้าลูกค้าสแกนแล้วไม่ขึ้น: ลองกดค้างที่ QR Code เปิดลิงก์ หรือใช้แอป LINE สแกนก็ได้ ตรวจสอบว่า QR Code ไม่เปื้อน ไม่ย่น และอยู่ในที่แสงสว่างพอ')

    # Chapter 4
    pdf.ch_header('04 · บทที่สี่', 'คำถามที่พบบ่อย', 'ปัญหาที่มักเจอ และวิธีแก้ไขเบื้องต้น')
    pdf.faq('ลูกค้าสแกน QR แล้วไม่เปิด?',
            'ใช้กล้องมือถือปกติ (ไม่ต้องโหลดแอปพิเศษ) ถ้ายังไม่ขึ้น ลองกดค้างที่ QR แล้วเลือก เปิดลิงก์ หรือใช้กล้องใน LINE สแกนแทนได้')
    pdf.faq('อยากแก้ราคาเมนู ทำได้ไหม?',
            'ได้ครับ ส่งรายการที่ต้องการแก้ให้เราทาง LINE เราจะอัปเดตให้ภายใน 1 วันทำการ (นับเป็น 1 ครั้งของสิทธิ์แก้ไขฟรี) ถ้าต้องการแก้ราคาเองได้ตลอดเวลา แนะนำอัปเกรดเป็นแพ็ก Standard')
    pdf.faq('อยากเพิ่มเมนูใหม่ ทำอย่างไร?',
            'ส่งชื่อเมนู ราคา และรูปภาพมาให้เรา เราจะเพิ่มให้ (ถ้ายังมีสิทธิ์แก้ไขฟรีอยู่ จะใช้สิทธิ์นั้น ถ้าหมดแล้วคิดตามงาน)')
    pdf.faq('ใช้สิทธิ์แก้ไขฟรีหมดแล้ว ครั้งต่อไปเสียเท่าไร?',
            'แก้ข้อความ / ราคา 150 บาท/ครั้ง · เพิ่มเมนูพร้อมรูป 200 บาท/รายการ ทักมาได้เลย เราจะ quote ราคาให้ก่อนเสมอ')
    pdf.faq('ต้องการลิงก์เป็นชื่อร้านเอง ทำได้ไหม?',
            'ได้ครับ ต้องซื้อ domain ก่อน (ประมาณ 500-800 บาท/ปี) แจ้งเราแล้วจะตั้งค่าให้ มีค่าบริการเพิ่มเติม ทักมาสอบถามราคาได้เลย')
    pdf.body('ติดต่อเรา: มีคำถามหรือปัญหาที่ไม่พบใน FAQ ทักเราทาง LINE ได้เลย ตอบกลับภายใน 24 ชั่วโมงในวันทำการ (จันทร์-เสาร์)')

    pdf.thanks_page(
        line1='ขอบคุณที่ไว้วางใจ',
        line2='หวังว่าระบบเมนู QR Code จะช่วยให้ร้านของคุณ',
        line3='ดูมืออาชีพและให้บริการลูกค้าได้ดียิ่งขึ้นครับ',
        upgrade='ต้องการอัปเกรดเป็นแพ็ก Standard หรือ Premium? ทักเราได้เลย มีส่วนลดพิเศษสำหรับลูกค้าเดิม',
    )

    pdf.output('/home/user/khaomoo-menu/docs/ebook-basic.pdf')
    print('  [OK] ebook-basic.pdf')


# ===========================================================================
# Book 2 -- Standard
# ===========================================================================
def build_standard():
    pdf = EbookPDF()

    pdf.cover(
        badge='E-Book · แพ็ก 2 · Standard - แนะนำ',
        title1='คู่มือการใช้งาน',
        title2='เมนู QR Code',
        subtitle='2 ภาษา ไทย / อังกฤษ',
        line2='แก้ราคา · เพิ่มเมนู · ซ่อนเมนูได้เอง',
        price='2,500 บาท',
        days='ได้งานภายใน 4 วัน · แก้ไขฟรี 3 ครั้ง',
    )

    pdf.toc_page([
        ('1', 'ยินดีต้อนรับ! คุณได้อะไรบ้าง?', 'ภาพรวมฟีเจอร์ทั้งหมดในแพ็ก Standard'),
        ('2', 'ข้อมูลที่ต้องเตรียมส่งให้เรา', 'Checklist ก่อนเริ่มงาน'),
        ('3', 'วิธีสลับภาษา ไทย / อังกฤษ', 'ปุ่ม ไทย/EN อยู่ที่ไหน และทำงานอย่างไร'),
        ('4', 'วิธีแก้ราคาและเพิ่มเมนูด้วยตัวเอง', 'เข้า Supabase แก้ราคา เพิ่มเมนูใหม่ ทีละขั้น'),
        ('5', 'วิธีซ่อน / แสดงเมนูชั่วคราว + FAQ', 'เมนูหมด ปิดชั่วคราวโดยไม่ต้องลบ'),
    ])

    # Chapter 1
    pdf.ch_header('01', 'ยินดีต้อนรับ! คุณได้อะไรบ้าง?', 'สิ่งที่ได้รับเพิ่มเติมจากแพ็ก Basic ในแพ็ก Standard')
    pdf.body('แพ็ก Standard เหมาะกับร้านที่อยากให้ลูกค้าต่างชาติดูเมนูได้ และต้องการแก้ราคาหรือเพิ่มเมนูได้ด้วยตัวเอง โดยไม่ต้องรอเรา')
    pdf.section_heading('สิ่งที่คุณได้รับในแพ็ก Standard')
    pdf.feature('เมนูสูงสุด 60 รายการ พร้อมรูปภาพ', 'รองรับร้านที่มีเมนูหลากหลาย ดูสวยงามบนมือถือทุกรุ่น')
    pdf.feature('2 ภาษา ไทย / อังกฤษ -- สลับได้ทันที', 'กดปุ่ม EN ที่มุมขวาบน ชื่อเมนู หมวด คำอธิบาย เปลี่ยนเป็นอังกฤษทั้งหมด')
    pdf.feature('ปรับสีและโลโก้ตามแบรนด์ร้าน', 'สีหัวข้อ ปุ่ม และโลโก้ตรงตามแบรนด์ของคุณ')
    pdf.feature('แก้ราคา ชื่อ คำอธิบาย ด้วยตัวเองผ่านเว็บ', 'ผ่านเว็บ Supabase คลิก แก้ กด Enter เสร็จ ไม่ต้องรู้โค้ด')
    pdf.feature('ซ่อน / แสดงเมนูชั่วคราวได้เอง', 'เมนูหมดสต็อก ซ่อนได้ 1 คลิก โดยไม่ต้องลบออกถาวร')
    pdf.feature('QR Code + ไฟล์พิมพ์ PNG', 'ทั้ง QR Code และไฟล์ภาพพร้อมพิมพ์ใส่กรอบ')
    pdf.feature('แก้ไขฟรี 3 ครั้ง (ภายใน 60 วัน)', 'ขอแก้งานที่เราทำให้ได้ 3 รอบ เช่น เปลี่ยนสีใหม่ เพิ่มรูป ปรับดีไซน์')
    pdf.ln(2)
    pdf.tip_box('แก้ราคาเองได้ทันที ไม่ต้องรอเรา ไม่ต้องรู้โค้ด ลูกค้าต่างชาติก็สั่งได้สบาย')

    # Chapter 2
    pdf.ch_header('02', 'ข้อมูลที่ต้องเตรียม ส่งให้เรา', 'รวบรวมสิ่งเหล่านี้ก่อน แล้วส่งให้เราทาง LINE')
    pdf.body('แพ็ก Standard รองรับ 2 ภาษา ถ้ามีชื่อเมนูภาษาอังกฤษอยู่แล้วก็ยิ่งดี ถ้าไม่มีเราจะแปลให้ครับ')
    pdf.section_heading('Checklist ข้อมูลที่ต้องส่ง')
    pdf.checklist_item('ชื่อร้าน (ไทย + อังกฤษถ้ามี)', 'เช่น ร้านข้าวขาหมู / Khao Kha Moo Restaurant')
    pdf.checklist_item('รายการเมนูสูงสุด 60 รายการ', 'ชื่อไทย + ราคา + หมวดหมู่ ไม่มีชื่ออังกฤษก็ได้ เราจะแปลให้')
    pdf.checklist_item('รูปอาหารทุกรายการ (ถ้ามี)', 'ยิ่งครบยิ่งดี ถ่ายจากมือถือแสงสว่างได้เลย')
    pdf.checklist_item('โลโก้ร้าน (PNG หรือ JPG)', 'โลโก้จะแสดงในหัวเมนู')
    pdf.checklist_item('สีหลักและสีรองของร้าน', 'เช่น แดงเลือดหมู หรือ hex code เช่น #8B2635')
    pdf.checklist_item('อีเมลสำหรับสร้างบัญชี Supabase', 'ใช้บัญชีนี้เข้าแก้ราคาเองในภายหลัง เราจะส่งคำเชิญให้')
    pdf.ln(2)
    pdf.tip_box('Supabase คืออะไร? Supabase คือเว็บสำหรับจัดการข้อมูลเมนูร้านของคุณ เหมือน Google Sheets แต่เชื่อมกับแอปเมนูโดยตรง แก้ราคาในนั้น เมนูในแอปอัปเดตทันที ใช้ผ่านเบราว์เซอร์ปกติ ไม่ต้องติดตั้งโปรแกรม')

    # Chapter 3
    pdf.ch_header('03', 'วิธีสลับภาษา ไทย / อังกฤษ', 'ลูกค้าต่างชาติสั่งได้เอง ไม่ต้องรอพนักงานแปล')
    pdf.body('มุมขวาบนของหน้าเลือกโต๊ะ จะเห็นปุ่ม [ไทย | EN] กดสลับได้ทันที')
    pdf.body('กด EN เปลี่ยนทั้งหมดทุกหน้า: ชื่อเมนู หมวดหมู่ คำอธิบาย ตัวเลือก ทุกหน้าในแอปเปลี่ยนเป็นอังกฤษพร้อมกัน กด ไทย กลับมาภาษาไทยทันที ราคายังถูกต้องเสมอ')
    pdf.tip_box('ตัวอย่างภาษาไทย: ขาหมูพะโล้เตาถ่าน / หมวด: ขาหมู / 180 บาท\n---\nตัวอย่างภาษาอังกฤษ (กด EN): Charcoal Pork Knuckle / Category: Pork Knuckle / 180 Baht')
    pdf.body('ราคาแสดงในหน่วยบาท (THB) ทุกภาษา ไม่มีการแปลงสกุลเงิน')

    # Chapter 4
    pdf.ch_header('04', 'วิธีแก้ราคาและเพิ่มเมนูด้วยตัวเอง', 'ผ่านเว็บ Supabase ง่าย ไม่ต้องรู้โค้ด ทำเสร็จภายใน 1 นาที')
    pdf.body('ก่อนเริ่ม เตรียม 3 อย่าง: 1. เบราว์เซอร์บนมือถือหรือคอม  2. อีเมลและรหัสผ่าน Supabase (เราส่งให้ทาง LINE)  3. รายการที่ต้องการแก้ไข')
    pdf.section_heading('วิธีแก้ราคาเมนู')
    pdf.step(1, 'เปิดเบราว์เซอร์ พิมพ์ supabase.com กด Sign in', 'กรอก email + password ที่เราส่งให้ กด Log in')
    pdf.step(2, 'เลือกโปรเจกต์ร้านของคุณ', 'จะเห็นชื่อโปรเจกต์ (ชื่อร้าน) อยู่หน้าแรก กดคลิกเข้าไป')
    pdf.step(3, 'เมนูซ้ายมือ กด Table Editor', 'จะเห็นรายการตาราง คลิกตาราง menu')
    pdf.step(4, 'หาเมนูที่ต้องการแก้ คลิกเซลล์ price พิมพ์ราคาใหม่ กด Enter', 'บันทึกทันที อัปเดตในแอปภายใน 1-2 วินาที')
    pdf.ln(2)
    pdf.tip_box('กด Enter แล้ว แอปเมนูอัปเดตราคาใหม่ภายใน 1-2 วินาที ลูกค้าโหลดหน้าใหม่จะเห็นราคาใหม่ทันที ไม่ต้อง deploy ใหม่ ไม่ต้องแจ้งเรา')
    pdf.section_heading('วิธีเพิ่มเมนูใหม่')
    pdf.step(1, 'Table Editor menu กดปุ่ม Insert row (สีเขียว)', 'หน้าต่าง New row เปิดขึ้น')
    pdf.step(2, 'กรอกข้อมูลเมนูใหม่', 'id (เลขไม่ซ้ำ)  cat (หมวด)  name (ชื่อ)  price (ราคา)  description (คำอธิบาย)')
    pdf.step(3, 'กด Save เมนูขึ้นในแอปทันที', 'รูปภาพต้องให้เราใส่ให้ (นับเป็น 1 ครั้งของสิทธิ์แก้ไขฟรี)')
    pdf.ln(2)
    pdf.code_box("แก้หลายรายการพร้อมกันด้วย SQL:\nUPDATE public.menu SET price = 80 WHERE id = 4;\nUPDATE public.menu SET price = 70 WHERE id IN (4, 5, 6);\nUPDATE public.menu SET name = 'ขาหมูพะโล้สูตรใหม่' WHERE id = 1;")
    pdf.tip_box('ถ้า Supabase ขึ้น Paused: เข้า supabase.com คลิกโปรเจกต์ กด Resume project รอ 1-2 นาที ใช้งานได้ปกติ')

    # Chapter 5
    pdf.ch_header('05', 'ซ่อน / แสดงเมนู + คำถามที่พบบ่อย', 'เมนูหมดชั่วคราว ปิดได้ 1 คลิก โดยไม่ต้องลบ')
    pdf.body('เมื่อวัตถุดิบหมด หรืออยากปิดเมนูบางอย่างในวันนั้น ทำได้ง่ายมากครับ ไม่ต้องลบ กลับมาเปิดเมื่อไรก็ได้')
    pdf.section_heading('วิธีซ่อนเมนูชั่วคราว')
    pdf.step(1, 'Supabase Table Editor ตาราง menu หาเมนูที่ต้องการซ่อน', '')
    pdf.step(2, 'มองหาคอลัมน์ is_available ค่าปัจจุบัน = true (แสดงอยู่)', '')
    pdf.step(3, 'คลิกเซลล์ เปลี่ยนเป็น false กด Enter เมนูหายจากแอปทันที', 'ลูกค้าจะไม่เห็น')
    pdf.step(4, 'อยากเปิดอีกครั้ง เปลี่ยนกลับเป็น true กด Enter', 'เมนูกลับมาแสดงทันที')
    pdf.ln(2)
    pdf.tip_box('การซ่อน (false) ไม่ได้ลบข้อมูลออก แค่ซ่อนจากหน้าแอปเท่านั้น เปลี่ยนกลับ true ได้ตลอดเวลา')
    pdf.section_heading('คำถามที่พบบ่อย')
    pdf.faq('ลืมรหัสผ่าน Supabase ทำอย่างไร?',
            'เข้า supabase.com กด Forgot password ระบบส่งลิงก์ reset ให้ทางอีเมล หรือทักมาให้เรารีเซ็ตให้ก็ได้')
    pdf.faq('แก้ราคาแล้วแต่แอปยังแสดงราคาเดิม?',
            'ลองรีเฟรชหน้าแอปบนมือถือ หรือปิดแล้วเปิดใหม่ ถ้ายังไม่อัปเดต ทักแจ้งเราได้เลย')
    pdf.faq('เพิ่มรูปภาพใหม่ได้เองไหม?',
            'รูปภาพต้องให้เราอัปโหลดขึ้น server ให้ครับ ส่งรูปมาทาง LINE แล้วเราจะอัปเดตให้ (นับเป็น 1 ครั้งของสิทธิ์แก้ไขฟรี)')
    pdf.faq('Supabase ขึ้น error หรือใช้งานไม่ได้?',
            'ถ้าโปรเจกต์ถูก pause ให้เข้าไป Resume ก่อน ถ้ายังมีปัญหาทักเราได้เลย จะช่วยแก้ให้')
    pdf.body('ติดต่อเรา: มีคำถามหรือปัญหาอื่น ทักเราทาง LINE ได้เลย ตอบกลับภายใน 24 ชั่วโมงในวันทำการ (จันทร์-เสาร์)')

    pdf.thanks_page(
        line1='ขอบคุณที่ไว้วางใจ',
        line2='ต้องการออเดอร์เข้า LINE OA อัตโนมัติ?',
        line3='อัปเกรดเป็นแพ็ก Premium ได้เลย มีส่วนลดสำหรับลูกค้าเดิม',
    )

    pdf.output('/home/user/khaomoo-menu/docs/ebook-standard.pdf')
    print('  [OK] ebook-standard.pdf')


# ===========================================================================
# Book 3 -- Premium
# ===========================================================================
def build_premium():
    pdf = EbookPDF()

    pdf.cover(
        badge='E-Book · แพ็ก 3 · Premium',
        title1='คู่มือการใช้งาน',
        title2='เมนู QR Code',
        subtitle='สั่งผ่าน LINE OA อัตโนมัติ',
        line2='รองรับ Delivery · ตัวเลือกเมนูครบ · 2 ภาษา',
        price='5,900 บาท',
        days='ได้งานภายใน 7 วัน · แก้ไขฟรี 5 ครั้ง · สอน Zoom 30 นาที',
    )

    pdf.toc_page([
        ('1', 'ยินดีต้อนรับ! คุณได้อะไรบ้าง?', 'ภาพรวมฟีเจอร์ทั้งหมดในแพ็ก Premium'),
        ('2', 'ข้อมูลที่ต้องเตรียมส่งให้เรา', 'Checklist ก่อนเริ่มงาน -- ครบกว่าแพ็กอื่น'),
        ('3', 'วิธีรับออเดอร์ผ่าน LINE OA (Dine-in)', 'ลูกค้าสั่ง ออเดอร์เข้า LINE OA ร้านทันที'),
        ('4', 'วิธีรับออเดอร์ Delivery', 'ลูกค้ากรอกที่อยู่ ออเดอร์เข้าพร้อมข้อมูลจัดส่ง'),
        ('5', 'วิธีจัดการเมนูผ่าน Supabase', 'แก้ราคา เพิ่มเมนู ซ่อนเมนู ทุกอย่างด้วยตัวเอง'),
        ('6', 'Zoom Training + คำถามที่พบบ่อย', 'สอนการใช้งานแบบ 1-on-1 ทาง Zoom 30 นาที'),
    ])

    # Chapter 1
    pdf.ch_header('01', 'ยินดีต้อนรับ! คุณได้อะไรบ้าง?', 'ภาพรวมฟีเจอร์ Premium -- ครบที่สุด')
    pdf.body('แพ็ก Premium คือระบบเมนูออนไลน์เต็มรูปแบบ ที่ลูกค้าสั่งอาหารได้ผ่านแอป แล้วออเดอร์ส่งตรงเข้า LINE OA ร้านทันที ไม่ว่าจะเป็น Dine-in หรือ Delivery')
    pdf.section_heading('สิ่งที่คุณได้รับในแพ็ก Premium')
    pdf.feature('เมนูไม่จำกัดจำนวน พร้อมรูปภาพ', 'รองรับร้านขนาดใหญ่ที่มีเมนูหลักร้อยรายการ')
    pdf.feature('2 ภาษา ไทย / อังกฤษ -- สลับได้ทันที', 'ลูกค้าต่างชาติสั่งได้เองโดยไม่ต้องรอพนักงาน')
    pdf.feature('ตัวเลือกเมนูครบ (Options & Add-ons)', 'เลือกไซส์ ระดับความเผ็ด ท็อปปิ้ง เพิ่ม/ลดราคาอัตโนมัติ')
    pdf.feature('ระบบสั่งอาหาร Dine-in ออเดอร์เข้า LINE OA', 'ลูกค้าสแกน QR โต๊ะ สั่งอาหาร กด confirm ออเดอร์เข้า LINE OA ทันที')
    pdf.feature('รองรับ Delivery -- ลูกค้ากรอกที่อยู่จัดส่ง', 'ออเดอร์ Delivery มีข้อมูลชื่อ เบอร์โทร ที่อยู่ครบถ้วน')
    pdf.feature('แก้ราคา เพิ่มเมนู ซ่อนเมนูด้วยตัวเองผ่าน Supabase', 'เหมือนแพ็ก Standard แต่ทำได้กับเมนูไม่จำกัด')
    pdf.feature('QR Code แยกต่อโต๊ะ (สูงสุด 30 โต๊ะ)', 'QR แต่ละโต๊ะระบุเลขโต๊ะในออเดอร์อัตโนมัติ')
    pdf.feature('แก้ไขฟรี 5 ครั้ง (ภายใน 90 วัน)', 'แก้งานที่เราทำให้ได้ 5 รอบ ในช่วง 3 เดือนแรก')
    pdf.feature('สอนการใช้งาน Zoom 1-on-1 30 นาที', 'นัด Zoom หลังงานเสร็จ เราสอนวิธีแก้เมนู รับออเดอร์ และจัดการระบบ')
    pdf.ln(2)
    pdf.tip_box('ออเดอร์เข้า LINE ที่คุณใช้อยู่แล้ว ไม่ต้องเปิดแอปใหม่ ไม่ต้องมีพนักงานรับออเดอร์แยก')

    # Chapter 2
    pdf.ch_header('02', 'ข้อมูลที่ต้องเตรียม ส่งให้เรา', 'ครบกว่าแพ็กอื่น เพราะระบบซับซ้อนกว่า')
    pdf.body('แพ็ก Premium มีฟีเจอร์เพิ่มขึ้นมาก ข้อมูลที่ต้องเตรียมก็มากกว่าเล็กน้อย แต่เราจะช่วย guide ทีละขั้น')
    pdf.section_heading('Checklist ข้อมูลที่ต้องส่ง')
    pdf.checklist_item('ชื่อร้าน (ไทย + อังกฤษ)', 'เช่น ร้านข้าวขาหมู / Khao Kha Moo Restaurant')
    pdf.checklist_item('รายการเมนูทั้งหมด พร้อมราคาและหมวดหมู่', 'ไม่จำกัดจำนวน ส่งเป็น Excel หรือ Google Sheets ได้เลย')
    pdf.checklist_item('ตัวเลือกแต่ละเมนู (Options)', 'เช่น ไซส์ S/M/L ระดับความเผ็ด ท็อปปิ้ง พร้อมราคาเพิ่ม/ลด')
    pdf.checklist_item('รูปอาหารทุกรายการ', 'ยิ่งครบยิ่งดี ถ่ายในแสงสว่าง พื้นหลังสะอาด')
    pdf.checklist_item('โลโก้ร้าน (PNG พื้นใสหรือ JPG)', 'โลโก้แสดงในหัวเมนูและในออเดอร์ที่ส่งเข้า LINE')
    pdf.checklist_item('สีหลักและสีรองของร้าน', 'hex code เช่น #8B2635 หรืออธิบายสีได้เลย')
    pdf.checklist_item('LINE OA ที่ต้องการให้ออเดอร์เข้า', 'เราจะตั้งค่า webhook ให้ออเดอร์เข้า LINE OA ของคุณ')
    pdf.checklist_item('จำนวนโต๊ะ (สำหรับ Dine-in) และต้องการ Delivery ด้วยไหม', 'บอกจำนวนโต๊ะที่ต้องการ QR และเปิดใช้ Delivery หรือเปล่า')
    pdf.ln(2)
    pdf.tip_box('ยังไม่มีข้อมูลทุกอย่างก็ส่งได้ครับ ส่งที่มีก่อน แล้วทยอยส่งที่เหลือ เราจะ hold งานส่วนนั้นไว้ก่อน')

    # Chapter 3
    pdf.ch_header('03', 'วิธีรับออเดอร์ผ่าน LINE OA (Dine-in)', 'ลูกค้าสั่ง ออเดอร์เข้า LINE OA ร้านทันที ไม่ต้องรับออเดอร์ด้วยมือ')
    pdf.section_heading('ขั้นตอนฝั่งลูกค้า')
    pdf.step(1, 'ลูกค้านั่งโต๊ะ สแกน QR Code บนโต๊ะ', 'QR แต่ละโต๊ะต่างกัน ระบบจะรู้ว่าโต๊ะอะไร')
    pdf.step(2, 'เลือกเมนู ปรับตัวเลือก (ถ้ามี)', 'เช่น ไซส์ L ความเผ็ดน้อย ไม่ใส่ผัก เลือกได้ในแอป')
    pdf.step(3, 'กด เพิ่มไปยังตะกร้า ทำซ้ำจนครบ', 'ดูสรุปในตะกร้าก่อนสั่ง')
    pdf.step(4, 'กด ยืนยันออเดอร์ ระบบส่งออเดอร์ทันที', 'ไม่ต้องรอพนักงาน ออเดอร์เข้าครัวและ LINE OA พร้อมกัน')
    pdf.step(5, 'รอพนักงานนำอาหารมาเสิร์ฟ', 'พนักงานเห็นออเดอร์ใน LINE OA และจัดเตรียมอาหาร')
    pdf.ln(2)
    pdf.section_heading('ตัวอย่างออเดอร์ที่เข้า LINE OA')
    pdf.tip_box('[ORDER] โต๊ะ 3 | 14:35\nขาหมูพะโล้เตาถ่าน x1 (ชุดใหญ่) = 280 บาท\nข้าวสวย x2 = 20 บาท\nน้ำเปล่า x1 = 15 บาท\nรวม: 315 บาท\nหมายเหตุ: ไม่ใส่ผักชี')
    pdf.tip_box('ออเดอร์เข้า LINE OA ที่คุณใช้อยู่แล้ว ไม่ต้องเปิดแอปใหม่ ดูได้ทั้งในมือถือและคอม')

    # Chapter 4
    pdf.ch_header('04', 'วิธีรับออเดอร์ Delivery', 'ลูกค้ากรอกที่อยู่จัดส่ง ออเดอร์เข้า LINE พร้อมข้อมูลครบ')
    pdf.body('ถ้าเปิดใช้ฟีเจอร์ Delivery ลูกค้าสามารถสั่งอาหารแบบจัดส่งได้โดยตรงจากเมนูออนไลน์')
    pdf.section_heading('ขั้นตอนฝั่งลูกค้า -- สั่ง Delivery')
    pdf.step(1, 'เปิดลิงก์เมนูหรือสแกน QR Code ของร้าน', 'ลิงก์เดียวกับ Dine-in แต่เลือก Delivery ที่หน้าแรก')
    pdf.step(2, 'เลือกเมนูที่ต้องการ ใส่ตะกร้า', 'เหมือนกับ Dine-in เลือกตัวเลือกได้ครบ')
    pdf.step(3, 'กรอกข้อมูลจัดส่ง: ชื่อ เบอร์โทร ที่อยู่', 'กรอกผ่านแบบฟอร์มในแอป ไม่ต้องโทรมาบอก')
    pdf.step(4, 'กด ยืนยันออเดอร์ Delivery', 'ระบบส่งออเดอร์พร้อมข้อมูลจัดส่งเข้า LINE OA ทันที')
    pdf.step(5, 'รอการยืนยันจากร้านทาง LINE', 'ร้านยืนยัน แจ้งเวลาส่ง และติดต่อกลับได้ทาง LINE')
    pdf.ln(2)
    pdf.section_heading('ตัวอย่างออเดอร์ Delivery ใน LINE')
    pdf.tip_box('[DELIVERY] 14:42\nชื่อ: คุณสมชาย โทร: 081-234-5678\nที่อยู่: 123/45 ถ.รัชดา แขวงดินแดง กรุงเทพ\nขาหมูพะโล้เตาถ่าน x1 = 280 บาท\nข้าวสวย x2 = 20 บาท\nรวม: 300 บาท (ยังไม่รวมค่าส่ง)\nหมายเหตุ: ขอเพิ่มซอสพริก')
    pdf.tip_box('ค่าจัดส่ง: ระบบไม่คำนวณค่าส่งอัตโนมัติ ให้ร้านแจ้งค่าส่งกับลูกค้าทาง LINE ก่อนยืนยัน (สามารถเพิ่มฟีเจอร์คำนวณค่าส่งอัตโนมัติได้ในอนาคต)')

    # Chapter 5
    pdf.ch_header('05', 'วิธีจัดการเมนูผ่าน Supabase', 'แก้ราคา เพิ่มเมนู ซ่อนเมนู ทำได้ด้วยตัวเองทั้งหมด')
    pdf.body('เหมือนแพ็ก Standard ทุกอย่าง แต่รองรับเมนูไม่จำกัด และมีคอลัมน์เพิ่มเติมสำหรับตัวเลือก (options)')
    pdf.section_heading('การจัดการพื้นฐาน (เหมือนแพ็ก Standard)')
    pdf.feature('แก้ราคา', 'Table Editor menu คลิก price พิมพ์ราคาใหม่ กด Enter')
    pdf.feature('เพิ่มเมนู', 'Insert row กรอกข้อมูล กด Save')
    pdf.feature('ซ่อนเมนู', 'คอลัมน์ is_available เปลี่ยน true/false')
    pdf.ln(2)
    pdf.section_heading('การจัดการตัวเลือก (Options) -- เฉพาะแพ็ก Premium')
    pdf.body('ตัวเลือกเมนู เช่น ไซส์ ความเผ็ด ท็อปปิ้ง เก็บในตาราง menu_options แยกต่างหาก')
    pdf.step(1, 'Table Editor เลือกตาราง menu_options', 'จะเห็นตัวเลือกทั้งหมดของทุกเมนู')
    pdf.step(2, 'แก้ชื่อหรือราคาตัวเลือก', 'คลิกเซลล์ แก้ กด Enter เหมือนกับตาราง menu')
    pdf.step(3, 'เพิ่มตัวเลือกใหม่', 'Insert row ระบุ menu_id ที่เชื่อมกับเมนูหลัก พร้อม name และ price_delta')
    pdf.ln(2)
    pdf.tip_box('price_delta คือราคาเพิ่มหรือลด\nเช่น ไซส์ L +20 บาท = price_delta: 20\nไม่เพิ่มลด = price_delta: 0\nลดราคา = price_delta: -10')

    # Chapter 6
    pdf.ch_header('06', 'Zoom Training + คำถามที่พบบ่อย', 'สอน 1-on-1 ทาง Zoom 30 นาที หลังจากงานส่งมอบแล้ว')
    pdf.body('หลังจากเราส่งมอบงานเรียบร้อยแล้ว เราจะนัด Zoom กับคุณ 1 ครั้ง ระยะเวลา 30 นาที')
    pdf.section_heading('หัวข้อที่จะสอนใน Zoom')
    pdf.feature('วิธีดูและจัดการออเดอร์ใน LINE OA', 'ดูออเดอร์ ตอบกลับลูกค้า mark ว่าเสร็จแล้ว')
    pdf.feature('วิธีแก้ราคาและจัดการเมนูใน Supabase', 'ทำ live demo ให้ดู แล้วให้ลองทำเอง')
    pdf.feature('วิธีซ่อน/แสดงเมนูและตัวเลือก', 'กรณีของหมด หรืออยากเพิ่มตัวเลือกใหม่')
    pdf.feature('ถามตอบปัญหาที่สงสัย', 'ตอบทุกคำถามที่มีในช่วง Zoom')
    pdf.ln(2)
    pdf.body('วิธีนัด Zoom: หลังรับงานแล้ว ทักเราทาง LINE แจ้งวันเวลาที่สะดวก เราจะส่งลิงก์ Zoom ให้ก่อนเวลานัด 1 ชั่วโมง')
    pdf.section_heading('คำถามที่พบบ่อย')
    pdf.faq('ออเดอร์ไม่เข้า LINE OA ทำอย่างไร?',
            'ตรวจสอบว่า LINE OA ไม่ได้ปิด notification ถ้ายังไม่เข้า ทักเราทันที เราจะตรวจ webhook ให้')
    pdf.faq('ลูกค้าสั่งแล้วแต่ร้านไม่เห็นออเดอร์?',
            'เช็คที่ LINE OA ก่อน (บางครั้ง notification ปิดอยู่) ถ้าไม่มีจริง ทักเราให้ตรวจ log ระบบ')
    pdf.faq('อยากเพิ่มโต๊ะเพิ่ม ทำได้ไหม?',
            'ได้ครับ แจ้งจำนวนโต๊ะที่ต้องการเพิ่ม เราจะสร้าง QR Code ใหม่ให้ มีค่าบริการเพิ่มเติมตามจำนวน')
    pdf.faq('อยากเพิ่มฟีเจอร์ใหม่ เช่น โชว์ยอดขาย หรือระบบ loyalty?',
            'ได้ครับ แต่เป็นงาน custom development ราคาขึ้นอยู่กับ scope งาน ทักมาเล่าให้ฟังก่อนได้เลย')
    pdf.faq('สิทธิ์แก้ไขฟรี 5 ครั้งหมดแล้ว ราคาครั้งต่อไป?',
            'แก้ข้อความ/ราคา 150 บาท | เพิ่มเมนูพร้อมรูป 200 บาท | แก้ตัวเลือก options 100 บาท/รายการ | งาน design ใหม่ quote ตามงาน')
    pdf.body('ติดต่อเรา: ปัญหาเร่งด่วน ทักเราทาง LINE ได้เลย ตอบกลับภายใน 24 ชั่วโมงในวันทำการ สำหรับ Premium ลูกค้า เราให้ความสำคัญเป็นพิเศษ')

    pdf.thanks_page(
        line1='ขอบคุณที่ไว้วางใจแพ็ก Premium',
        line2='ระบบออเดอร์อัตโนมัติจะช่วยให้ร้านของคุณ',
        line3='รับออเดอร์ได้เร็วขึ้น ไม่พลาด และดูมืออาชีพครับ',
    )

    pdf.output('/home/user/khaomoo-menu/docs/ebook-premium.pdf')
    print('  [OK] ebook-premium.pdf')


# ===========================================================================
# Main
# ===========================================================================
if __name__ == '__main__':
    print('Generating PDFs...')
    build_basic()
    build_standard()
    build_premium()
    print('Done.')
