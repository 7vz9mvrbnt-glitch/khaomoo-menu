"""
Generate E-book PDFs directly with fpdf2 (no HTML/weasyprint).
Produces clean Thai-language PDFs with no text overlap.
"""
from fpdf import FPDF
from fpdf.enums import RenderStyle
import os

FONTS = "/tmp/fonts"
OUT   = os.path.dirname(os.path.abspath(__file__))

# Colors (R,G,B)
SAGE   = (135, 160, 128)
SAGE_L = (236, 242, 235)
SAGE_D = (85,  114,  82)
CREAM  = (248, 245, 239)
WHITE  = (255, 255, 255)
DARK   = (42,  42,   42)
MID    = (94,  94,   94)
BORDER = (212, 226, 210)
CODE_BG= (240, 244, 240)

M = 18          # left/right margin mm
CW = 174        # content width mm (210 - 2*18)


class EbookPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        self.add_font("SB",  "",  f"{FONTS}/Sarabun-Regular.ttf")
        self.add_font("SB",  "B", f"{FONTS}/Sarabun-Bold.ttf")
        self.set_auto_page_break(auto=True, margin=20)

    # ── helpers ──────────────────────────────────────────────────

    def _fg(self, c): self.set_text_color(*c)
    def _fill(self, c): self.set_fill_color(*c)
    def _draw(self, c): self.set_draw_color(*c)

    def _line(self, x1, y1, x2, y2, c=BORDER):
        self._draw(c)
        self.line(x1, y1, x2, y2)

    def _rect(self, x, y, w, h, c, style="F"):
        self._fill(c)
        self._draw(c)
        self.rect(x, y, w, h, style)

    def body(self, txt, size=13, bold=False, color=DARK, align="L", lh=7.5):
        self.set_font("SB", "B" if bold else "", size)
        self._fg(color)
        self.set_x(M)
        self.multi_cell(CW, lh, txt, align=align)

    def gap(self, h=4): self.ln(h)

    def h2(self, txt, color=DARK):
        self.gap(6)
        self.body(txt, size=17, bold=True, color=color)
        self.gap(3)

    def feature_item(self, title, desc):
        # Green dot + bold title
        y = self.get_y()
        self._rect(M, y + 2.5, 4, 4, SAGE_D)
        self.set_font("SB", "B", 13)
        self._fg(DARK)
        self.set_x(M + 8)
        self.multi_cell(CW - 8, 7, title)
        self.set_font("SB", "", 12)
        self._fg(MID)
        self.set_x(M + 8)
        self.multi_cell(CW - 8, 6.5, desc)
        self.gap(3)

    def step_item(self, num, title, desc):
        y = self.get_y()
        # Circle bg
        self._rect(M, y, 9, 9, SAGE)
        self.set_font("SB", "B", 10)
        self._fg(WHITE)
        self.set_xy(M, y + 0.5)
        self.cell(9, 8, str(num), align="C")
        # Title
        self.set_font("SB", "B", 13)
        self._fg(DARK)
        self.set_xy(M + 12, y)
        self.multi_cell(CW - 12, 7, title)
        # Desc
        self.set_font("SB", "", 12)
        self._fg(MID)
        self.set_x(M + 12)
        self.multi_cell(CW - 12, 6.5, desc)
        self.gap(4)

    def check_item(self, label, desc):
        y = self.get_y()
        # Checkbox outline
        self._draw(SAGE_D)
        self._fill(WHITE)
        self.rect(M, y + 1, 5, 5, "D")
        self.set_font("SB", "B", 13)
        self._fg(DARK)
        self.set_xy(M + 8, y)
        self.multi_cell(CW - 8, 7, label)
        self.set_font("SB", "", 12)
        self._fg(MID)
        self.set_x(M + 8)
        self.multi_cell(CW - 8, 6.5, desc)
        self.gap(3)

    def faq_item(self, q, a):
        self.gap(4)
        self.set_font("SB", "B", 13)
        self._fg(SAGE_D)
        self.set_x(M)
        self.multi_cell(CW, 7, "Q: " + q)
        self.set_font("SB", "", 12)
        self._fg(DARK)
        self.set_x(M)
        self.multi_cell(CW, 6.5, "A: " + a)
        self._line(M, self.get_y() + 2, M + CW, self.get_y() + 2)
        self.gap(4)

    def tip_box(self, txt, title=""):
        self.gap(4)
        y = self.get_y()
        # measure height
        tmp = FPDF()
        tmp.add_font("SB", "", f"{FONTS}/Sarabun-Regular.ttf")
        tmp.add_page()
        tmp.set_font("SB", "", 12)
        lines = tmp.multi_cell(CW - 12, 6.5, txt, split_only=True)
        h = len(lines) * 6.5 + (10 if title else 4) + 10
        # bg
        self._fill(SAGE_L)
        self._draw(SAGE)
        self.rect(M, y, CW, h, "F")
        # left bar
        self._rect(M, y, 3, h, SAGE_D)
        # title
        yt = y + 5
        if title:
            self.set_font("SB", "B", 12)
            self._fg(SAGE_D)
            self.set_xy(M + 7, yt)
            self.multi_cell(CW - 10, 7, title)
            yt = self.get_y() + 1
        # text
        self.set_font("SB", "", 12)
        self._fg(DARK)
        self.set_xy(M + 7, yt)
        self.multi_cell(CW - 10, 6.5, txt)
        self.set_y(y + h + 2)
        self.gap(4)

    def code_box(self, txt):
        self.gap(3)
        y = self.get_y()
        tmp = FPDF()
        tmp.add_font("SB", "", f"{FONTS}/Sarabun-Regular.ttf")
        tmp.add_page()
        tmp.set_font("SB", "", 11)
        lines = tmp.multi_cell(CW - 8, 6, txt, split_only=True)
        h = len(lines) * 6 + 10
        self._rect(M, y, CW, h, CODE_BG)
        self._draw(BORDER)
        self.rect(M, y, CW, h, "D")
        self.set_font("SB", "", 11)
        self._fg(SAGE_D)
        self.set_xy(M + 4, y + 5)
        self.multi_cell(CW - 8, 6, txt)
        self.set_y(y + h + 2)
        self.gap(3)

    def contact_box(self):
        self.gap(6)
        self._line(M, self.get_y(), M + CW, self.get_y())
        self.gap(4)
        self.body("ติดต่อเรา", size=14, bold=True, color=SAGE_D)
        self.body("มีคำถามหรือปัญหา → ทักเราทาง LINE ได้เลย", size=12, color=MID)
        self.body("ตอบกลับภายใน 24 ชั่วโมงในวันทำการ (จันทร์–เสาร์)", size=12, color=MID)

    # ── page templates ────────────────────────────────────────────

    def cover(self, badge, title1, title2, sub1, sub2, price, days):
        self.add_page()
        self.set_auto_page_break(False)
        # sage bg
        self._rect(0, 0, 210, 262, SAGE)
        # white footer
        self._rect(0, 262, 210, 35, WHITE)
        # badge
        self.set_font("SB", "B", 11)
        self._fg(WHITE)
        self.set_xy(0, 32)
        self.cell(210, 8, badge, align="C")
        # title line 1
        self.set_font("SB", "B", 38)
        self.set_xy(0, 55)
        self.cell(210, 14, title1, align="C")
        # title line 2
        self.set_xy(0, 74)
        self.cell(210, 14, title2, align="C")
        # sub1
        self.set_font("SB", "", 15)
        self.set_xy(0, 102)
        self.cell(210, 8, sub1, align="C")
        # sub2
        self.set_font("SB", "", 13)
        self.set_xy(0, 114)
        self.cell(210, 7, sub2, align="C")
        # price pill
        pw, ph, pr = 92, 18, 9
        px = (210 - pw) / 2
        py = 148
        self._fill(WHITE)
        self._draw(WHITE)
        self._draw_rounded_rect(px, py, pw, ph, RenderStyle.F,
                                round_corners=True, r=pr)
        self.set_font("SB", "B", 20)
        self._fg(SAGE_D)
        self.set_xy(px, py)
        self.cell(pw, ph, price, align="C")
        # days
        self.set_font("SB", "", 12)
        self._fg(WHITE)
        self.set_xy(0, 174)
        self.cell(210, 7, days, align="C")
        # footer text
        self.set_font("SB", "", 11)
        self._fg(MID)
        self.set_xy(0, 271)
        self.cell(210, 7, "คู่มือนี้จัดทำขึ้นสำหรับลูกค้าเท่านั้น", align="C")
        self.set_auto_page_break(True, margin=20)

    def toc_page(self, chapters):
        self.add_page()
        self._rect(0, 0, 210, 297, CREAM)
        self.set_font("SB", "B", 22)
        self._fg(SAGE_D)
        self.set_xy(M, 35)
        self.cell(CW, 10, "สารบัญ")
        self._line(M, 52, M + CW, 52, SAGE_D)
        y = 60
        for i, (title, sub) in enumerate(chapters, 1):
            # number circle
            self._rect(M, y, 9, 9, SAGE)
            self.set_font("SB", "B", 10)
            self._fg(WHITE)
            self.set_xy(M, y + 0.5)
            self.cell(9, 8, str(i), align="C")
            # title
            self.set_font("SB", "B", 14)
            self._fg(DARK)
            self.set_xy(M + 14, y)
            self.multi_cell(CW - 14, 7, title)
            # sub
            self.set_font("SB", "", 12)
            self._fg(MID)
            self.set_x(M + 14)
            self.multi_cell(CW - 14, 6.5, sub)
            y = self.get_y() + 5
            self._line(M, y, M + CW, y)
            y += 5

    def ch_header(self, num, title, subtitle, ch_sub=""):
        self.add_page()
        self._rect(0, 0, 210, 78, SAGE)
        # chapter label
        self.set_font("SB", "B", 11)
        self._fg((255, 255, 255))
        self.set_xy(M, 20)
        self.cell(CW, 6, f"0{num}  ·  บทที่{'หนึ่ง สอง สาม สี่ ห้า หก'.split()[num-1]}")
        # main title
        self.set_font("SB", "B", 28)
        self._fg(WHITE)
        self.set_xy(M, 32)
        self.multi_cell(CW, 12, title)
        # subtitle
        self.set_font("SB", "", 14)
        self._fg((220, 232, 218))
        self.set_x(M)
        self.multi_cell(CW, 7, subtitle)
        # reset for content
        self.set_y(90)

    def thanks_page(self, msg, upgrade=""):
        self.add_page()
        self.set_auto_page_break(False)
        self._rect(0, 0, 210, 297, SAGE)
        self.set_font("SB", "B", 28)
        self._fg(WHITE)
        self.set_xy(0, 100)
        self.cell(210, 12, "ขอบคุณที่ไว้วางใจ", align="C")
        self.set_font("SB", "", 15)
        self.set_xy(M, 124)
        self.multi_cell(CW, 8, msg, align="C")
        if upgrade:
            self.gap(8)
            self.set_font("SB", "B", 13)
            self._fg((220, 232, 218))
            self.set_x(M)
            self.multi_cell(CW, 7, upgrade, align="C")
        self.set_auto_page_break(True, margin=20)


# ══════════════════════════════════════════════════════════════════
# Book 1 — Basic
# ══════════════════════════════════════════════════════════════════

def build_basic():
    p = EbookPDF()

    p.cover(
        "E-Book  ·  แพ็ก 1  ·  Basic",
        "คู่มือการใช้งาน",
        "เมนู QR Code",
        "เมนูออนไลน์สำหรับร้านอาหาร",
        "สวยงาม  ·  พิมพ์ได้  ·  ใช้ง่าย",
        "990 บาท",
        "ได้งานภายใน 2 วัน  ·  แก้ไขฟรี 1 ครั้ง",
    )

    p.toc_page([
        ("ยินดีต้อนรับ! คุณได้อะไรบ้าง?",     "ภาพรวมสิ่งที่ได้รับในแพ็กนี้"),
        ("ข้อมูลที่ต้องเตรียมส่งให้เรา",        "Checklist ครบชุด ก่อนเริ่มงาน"),
        ("วิธีใช้ QR Code ที่ร้าน",             "ติดโต๊ะ  →  ลูกค้าสแกน  →  ดูเมนู"),
        ("คำถามที่พบบ่อย",                      "ปัญหาที่มักเจอ และวิธีแก้ไข"),
    ])

    # Ch 1
    p.ch_header(1, "ยินดีต้อนรับ!\nคุณได้อะไรบ้าง?",
                "ทำความเข้าใจสิ่งที่คุณได้รับในแพ็ก Basic")
    p.body("ขอบคุณที่เลือกใช้บริการครับ ในแพ็กนี้คุณจะได้รับเมนูอาหารออนไลน์พร้อมใช้งาน ที่ลูกค้าสแกน QR Code แล้วดูเมนูได้ทันทีบนมือถือ โดยไม่ต้องดาวน์โหลดแอปใด ๆ")
    p.gap()
    p.h2("สิ่งที่คุณได้รับในแพ็กนี้")
    p.feature_item("เมนูออนไลน์สูงสุด 20 รายการ พร้อมรูปภาพ",
                   "แสดงรูปอาหาร ชื่อ ราคา และคำอธิบาย ดูสวยงามบนมือถือทุกรุ่น")
    p.feature_item("แยกหมวดหมู่ กรองเมนูได้",
                   "ลูกค้ากดเลือกหมวดได้ทันที เช่น ของทานเล่น เครื่องดื่ม หาเมนูเจอเร็วขึ้น")
    p.feature_item("QR Code ความละเอียดสูง พิมพ์ได้ทุกขนาด",
                   "ไฟล์ PNG ขนาดใหญ่ พิมพ์บนกระดาษ สติกเกอร์ อคริลิค หรือกรอบได้เลย")
    p.feature_item("ลิงก์เมนูออนไลน์",
                   "ส่งลิงก์ผ่าน LINE / Facebook ให้ลูกค้าเปิดดูได้โดยไม่ต้องสแกน QR")
    p.feature_item("แก้ไขฟรี 1 ครั้ง (ภายใน 30 วัน)",
                   "ขอแก้ชื่อเมนู ราคา หรือรูปภาพได้ 1 รอบ หลังจากนั้นคิดเพิ่มตามงาน")
    p.tip_box("เมนูสวยงาม ดูมืออาชีพ ลูกค้าดูรูปก่อนสั่ง ตัดสินใจเร็วขึ้น ยอดขายดีขึ้น", "ทำไมต้องเมนู QR Code?")
    p.tip_box("เมนูกระดาษพอราคาเปลี่ยน → ต้องพิมพ์ใหม่ทั้งเล่ม\nแต่เมนู QR Code → ส่งข้อมูลให้เราแก้ ราคาใหม่ขึ้นทันที ไม่ต้องพิมพ์ซ้ำ ประหยัดค่าพิมพ์ระยะยาว", "เปรียบเทียบกับเมนูกระดาษ")

    # Ch 2
    p.ch_header(2, "ข้อมูลที่ต้องเตรียม\nส่งให้เรา",
                "รวบรวมสิ่งเหล่านี้ก่อน แล้วส่งให้เราทาง LINE")
    p.body("ก่อนเราเริ่มทำงาน คุณต้องส่งข้อมูลเหล่านี้มาให้ก่อนนะครับ ยิ่งข้อมูลครบ งานยิ่งเสร็จเร็ว")
    p.gap()
    p.h2("Checklist ข้อมูลที่ต้องส่ง")
    p.check_item("ชื่อร้าน", "ชื่อที่ต้องการแสดงในเมนู เช่น ร้านข้าวขาหมูต้นตำรับ")
    p.check_item("รายการเมนูทั้งหมด (สูงสุด 20 รายการ)", "ชื่อเมนู + ราคา + หมวดหมู่ ส่งเป็น Excel, Note, หรือถ่ายรูปเมนูเดิมมาได้เลย")
    p.check_item("รูปอาหาร (ถ้ามี)", "รูปละเอียด สว่าง พื้นหลังสะอาด ส่งเป็น JPG/PNG ถ่ายจากมือถือได้เลย")
    p.check_item("โลโก้ร้าน (ถ้ามี)", "ไฟล์ PNG หรือ JPG โลโก้หน้าร้าน หรือตราสินค้า")
    p.check_item("สีหลักของร้าน", "สีที่ต้องการใช้ เช่น แดงเลือดหมู น้ำตาลโกโก้ หรือ code สี #XXXXXX ก็ได้")
    p.tip_box("ถ่ายในที่แสงสว่าง ไม่ต้องมีกล้องแพง — มือถือก็ได้ผลดีมาก\nใส่ในจาน/ชาม ให้เห็นหน้าอาหาร อย่าถ่ายจากมุมต่ำเกินไป\nพื้นหลังสีเรียบหรือโต๊ะไม้ดูดีมาก", "เคล็ดลับถ่ายรูปอาหาร")
    p.tip_box("ถ้ายังไม่มีรูปอาหาร — ส่งข้อมูลอื่นมาก่อนได้เลยครับ เราจะใส่รูป placeholder ไว้ก่อน แล้วค่อยส่งรูปจริงมาทีหลัง (นับเป็น 1 ครั้งของสิทธิ์แก้ไขฟรี)", "ยังไม่มีรูปก็ส่งได้")

    # Ch 3
    p.ch_header(3, "วิธีใช้ QR Code\nที่ร้าน",
                "ตั้งแต่พิมพ์ QR Code ไปจนถึงลูกค้าสแกนดูเมนู")
    p.h2("ขั้นตอนฝั่งร้าน — ติดตั้ง QR Code")
    p.step_item(1, "รับไฟล์ QR Code จากเราทาง LINE", "เราส่งไฟล์ PNG ให้ทาง LINE พร้อมลิงก์เมนูด้วย")
    p.step_item(2, "พิมพ์ QR Code ออกมา", "พิมพ์บนกระดาษธรรมดา สติกเกอร์ หรืออคริลิคก็ได้ ขนาดแนะนำ 8x8 ซม. ขึ้นไป")
    p.step_item(3, "ติดที่โต๊ะหรือเคาน์เตอร์", "วางให้ลูกค้าเห็นชัดเจน ไม่อยู่ในที่มืด ใส่กรอบอคริลิคดูดีและทนทาน")
    p.tip_box("แนะนำติดทุกโต๊ะ: ถ้ามีหลายโต๊ะ พิมพ์หลายแผ่นได้เลย ใช้ QR Code ไฟล์เดิมทั้งหมด ลิงก์เดียวกัน")
    p.h2("ขั้นตอนฝั่งลูกค้า — สแกนดูเมนู")
    p.step_item(1, "เปิดกล้องมือถือปกติ (ไม่ต้องโหลดแอปพิเศษ)", "ทั้ง iPhone และ Android ใช้กล้องธรรมดาได้เลย")
    p.step_item(2, "ชี้กล้องไปที่ QR Code บนโต๊ะ", "กล้องจะจับ QR Code อัตโนมัติ ไม่ต้องกดอะไร")
    p.step_item(3, "กดลิงก์ที่ขึ้นมาบนหน้าจอ", "กด Open / เปิดลิงก์ → เมนูเปิดในเบราว์เซอร์ทันที")
    p.step_item(4, "ดูเมนู เลือกรายการ แจ้งพนักงาน", "ดูรูปอาหาร ราคา อ่านคำอธิบาย แล้วแจ้งพนักงานสั่ง")
    p.tip_box("ถ้าลูกค้าสแกนแล้วไม่ขึ้น:\n- ลองกดค้างที่ QR Code → เปิดลิงก์\n- หรือใช้แอป LINE สแกนก็ได้\n- ตรวจสอบว่า QR Code ไม่เปื้อน ไม่ย่น และอยู่ในที่แสงสว่างพอ", "แก้ปัญหา")

    # Ch 4
    p.ch_header(4, "คำถามที่พบบ่อย",
                "ปัญหาที่มักเจอ และวิธีแก้ไขเบื้องต้น")
    p.faq_item("ลูกค้าสแกน QR แล้วไม่เปิด?",
               "ใช้กล้องมือถือปกติ (ไม่ต้องโหลดแอปพิเศษ) ถ้ายังไม่ขึ้น → ลองกดค้างที่ QR แล้วเลือก เปิดลิงก์ หรือใช้กล้องใน LINE สแกนแทนได้")
    p.faq_item("อยากแก้ราคาเมนู ทำได้ไหม?",
               "ได้ครับ ส่งรายการที่ต้องการแก้ให้เราทาง LINE เราจะอัปเดตให้ภายใน 1 วันทำการ (นับเป็น 1 ครั้งของสิทธิ์แก้ไขฟรี) ถ้าต้องการแก้ราคาเองได้ตลอดเวลา แนะนำอัปเกรดเป็นแพ็ก Standard")
    p.faq_item("อยากเพิ่มเมนูใหม่ ทำอย่างไร?",
               "ส่งชื่อเมนู ราคา และรูปภาพมาให้เรา เราจะเพิ่มให้ (ถ้ายังมีสิทธิ์แก้ไขฟรีอยู่ จะใช้สิทธิ์นั้น ถ้าหมดแล้วคิดตามงาน)")
    p.faq_item("เมนูขาดรูปภาพได้ไหม?",
               "ได้ครับ ระบบจะแสดงรูป placeholder แทน แต่แนะนำให้ใส่รูปจริง เพราะลูกค้าเห็นรูปแล้วตัดสินใจสั่งได้ง่ายขึ้นมาก")
    p.faq_item("ใช้สิทธิ์แก้ไขฟรีหมดแล้ว ครั้งต่อไปเสียเท่าไร?",
               "แก้ข้อความ / ราคา → 150 บาท/ครั้ง  ·  เพิ่มเมนูพร้อมรูป → 200 บาท/รายการ\nทักมาได้เลย เราจะ quote ราคาให้ก่อนเสมอ")
    p.faq_item("ต้องการลิงก์เป็นชื่อร้านเอง เช่น menu.ชื่อร้าน.com ทำได้ไหม?",
               "ได้ครับ ต้องซื้อ domain ก่อน (ประมาณ 500–800 บาท/ปี) แจ้งเราแล้วจะตั้งค่าให้ มีค่าบริการเพิ่มเติม ทักมาสอบถามราคาได้เลย")
    p.contact_box()

    p.thanks_page(
        "หวังว่าระบบเมนู QR Code จะช่วยให้ร้านของคุณ\nดูมืออาชีพและให้บริการลูกค้าได้ดียิ่งขึ้นครับ",
        "ต้องการอัปเกรดเป็นแพ็ก Standard หรือ Premium?\nทักเราได้เลย มีส่วนลดพิเศษสำหรับลูกค้าเดิม"
    )

    out = f"{OUT}/ebook-basic.pdf"
    p.output(out)
    print(f"  Basic:    {os.path.getsize(out)//1024} KB  ({out})")


# ══════════════════════════════════════════════════════════════════
# Book 2 — Standard
# ══════════════════════════════════════════════════════════════════

def build_standard():
    p = EbookPDF()

    p.cover(
        "E-Book  ·  แพ็ก 2  ·  Standard  -  แนะนำ",
        "คู่มือการใช้งาน",
        "เมนู QR Code",
        "2 ภาษา ไทย / อังกฤษ",
        "แก้ราคา  ·  เพิ่มเมนู  ·  ซ่อนเมนูได้เอง",
        "2,500 บาท",
        "ได้งานภายใน 4 วัน  ·  แก้ไขฟรี 3 ครั้ง",
    )

    p.toc_page([
        ("ยินดีต้อนรับ! คุณได้อะไรบ้าง?",         "ภาพรวมฟีเจอร์ทั้งหมดในแพ็ก Standard"),
        ("ข้อมูลที่ต้องเตรียมส่งให้เรา",            "Checklist ก่อนเริ่มงาน"),
        ("วิธีสลับภาษา ไทย / อังกฤษ",              "ปุ่ม ไทย | EN อยู่ที่ไหน และทำงานอย่างไร"),
        ("วิธีแก้ราคาและเพิ่มเมนูด้วยตัวเอง",       "เข้า Supabase  ·  แก้ราคา  ·  เพิ่มเมนูใหม่ ทีละขั้น"),
        ("วิธีซ่อน / แสดงเมนูชั่วคราว + FAQ",       "เมนูหมด ปิดชั่วคราวโดยไม่ต้องลบ"),
    ])

    # Ch 1
    p.ch_header(1, "ยินดีต้อนรับ!\nคุณได้อะไรบ้าง?",
                "สิ่งที่ได้รับเพิ่มเติมจากแพ็ก Basic ในแพ็ก Standard")
    p.body("แพ็ก Standard เหมาะกับร้านที่อยากให้ลูกค้าต่างชาติดูเมนูได้ และต้องการแก้ราคาหรือเพิ่มเมนูได้ด้วยตัวเอง โดยไม่ต้องรอเรา")
    p.gap()
    p.h2("สิ่งที่คุณได้รับทั้งหมด")
    p.feature_item("เมนูสูงสุด 60 รายการ พร้อมรูปภาพ",
                   "รองรับร้านที่มีเมนูหลากหลาย ดูสวยงามบนมือถือทุกรุ่น")
    p.feature_item("2 ภาษา ไทย / อังกฤษ — สลับได้ทันที",
                   "กดปุ่ม EN ที่มุมขวาบน → ชื่อเมนู หมวด คำอธิบาย เปลี่ยนเป็นอังกฤษทั้งหมด")
    p.feature_item("ปรับสีและโลโก้ตามแบรนด์ร้าน",
                   "สีหัวข้อ ปุ่ม และโลโก้ตรงตามแบรนด์ของคุณ")
    p.feature_item("แก้ราคา ชื่อ คำอธิบาย ด้วยตัวเองผ่านเว็บ",
                   "ผ่านเว็บ Supabase — คลิก แก้ กด Enter เสร็จ ไม่ต้องรู้โค้ด")
    p.feature_item("ซ่อน / แสดงเมนูชั่วคราวได้เอง",
                   "เมนูหมดสต็อก → ซ่อนได้ 1 คลิก โดยไม่ต้องลบออกถาวร")
    p.feature_item("QR Code + ไฟล์พิมพ์ PNG",
                   "ทั้ง QR Code และไฟล์ภาพพร้อมพิมพ์ใส่กรอบ")
    p.feature_item("แก้ไขฟรี 3 ครั้ง (ภายใน 60 วัน)",
                   "ขอแก้งานที่เราทำให้ได้ 3 รอบ เช่น เปลี่ยนสีใหม่ เพิ่มรูป ปรับดีไซน์")
    p.tip_box("แก้ราคาเองได้ทันที ไม่ต้องรอเรา ไม่ต้องรู้โค้ด\nลูกค้าต่างชาติก็สั่งได้สบาย", "ข้อดีหลักของแพ็ก Standard")

    # Ch 2
    p.ch_header(2, "ข้อมูลที่ต้องเตรียม\nส่งให้เรา",
                "รวบรวมสิ่งเหล่านี้ก่อน แล้วส่งให้เราทาง LINE")
    p.body("แพ็ก Standard รองรับ 2 ภาษา ถ้ามีชื่อเมนูภาษาอังกฤษอยู่แล้วก็ยิ่งดี ถ้าไม่มีเราจะแปลให้ครับ")
    p.gap()
    p.h2("Checklist ข้อมูลที่ต้องส่ง")
    p.check_item("ชื่อร้าน (ไทย + อังกฤษถ้ามี)", "เช่น ร้านข้าวขาหมู / Khao Kha Moo Restaurant")
    p.check_item("รายการเมนูสูงสุด 60 รายการ", "ชื่อไทย + ราคา + หมวดหมู่  ·  ไม่มีชื่ออังกฤษก็ได้ เราจะแปลให้")
    p.check_item("รูปอาหารทุกรายการ (ถ้ามี)", "ยิ่งครบยิ่งดี ถ่ายจากมือถือแสงสว่างได้เลย")
    p.check_item("โลโก้ร้าน (PNG หรือ JPG)", "โลโก้จะแสดงในหัวเมนู")
    p.check_item("สีหลักและสีรองของร้าน", "เช่น แดงเลือดหมู หรือ hex code เช่น #8B2635")
    p.check_item("อีเมลสำหรับสร้างบัญชี Supabase", "ใช้บัญชีนี้เข้าแก้ราคาเองในภายหลัง เราจะส่งคำเชิญให้")
    p.tip_box("Supabase คืออะไร?\nSupabase คือเว็บสำหรับจัดการข้อมูลเมนูร้านของคุณ เหมือน Google Sheets แต่เชื่อมกับแอปเมนูโดยตรง แก้ราคาในนั้น → เมนูในแอปอัปเดตทันที ใช้ผ่านเบราว์เซอร์ปกติ ไม่ต้องติดตั้งโปรแกรม")

    # Ch 3
    p.ch_header(3, "วิธีสลับภาษา\nไทย / อังกฤษ",
                "ลูกค้าต่างชาติสั่งได้เอง ไม่ต้องรอพนักงานแปล")
    p.body("มุมขวาบนของหน้าเลือกโต๊ะ จะเห็นปุ่ม  [ ไทย | EN ]  กดสลับได้ทันที")
    p.gap(5)
    p.body("กด EN → เปลี่ยนทั้งหมดทุกหน้า:\nชื่อเมนู  ·  หมวดหมู่  ·  คำอธิบาย  ·  ตัวเลือก — ทุกหน้าในแอปเปลี่ยนเป็นอังกฤษพร้อมกัน\nกด ไทย → กลับมาภาษาไทยทันที  ราคายังถูกต้องเสมอ")
    p.gap(5)
    p.h2("เปรียบเทียบก่อน / หลังกด EN")
    # Two-column comparison using code_box style
    p.tip_box(
        "ภาษาไทย (ปกติ):\n"
        "ขาหมูพะโล้เตาถ่าน\n"
        "หมวด: ขาหมู  ·  180 บาท\n"
        "ชุดขาหมู (1ขา) / ไส้ล้วน / คากิล้วน",
        "ภาษาไทย"
    )
    p.tip_box(
        "English (กด EN):\n"
        "Charcoal Pork Knuckle\n"
        "Category: Pork Knuckle  ·  180 Baht\n"
        "Pork Knuckle Set / Innards Only / Kaki Only",
        "English"
    )
    p.tip_box("ราคาแสดงในหน่วยบาท (฿) ทุกภาษา ไม่มีการแปลงสกุลเงิน")

    # Ch 4
    p.ch_header(4, "วิธีแก้ราคาและ\nเพิ่มเมนูด้วยตัวเอง",
                "ผ่านเว็บ Supabase — ง่าย ไม่ต้องรู้โค้ด ทำเสร็จภายใน 1 นาที")
    p.tip_box("ก่อนเริ่ม เตรียม 3 อย่างนี้:\n1. เบราว์เซอร์บนมือถือหรือคอม (Chrome / Safari ได้เลย)\n2. อีเมลและรหัสผ่าน Supabase (เราส่งให้ทาง LINE)\n3. รายการที่ต้องการแก้ไข เช่น ขาหมูใหญ่ เปลี่ยนจาก 180 เป็น 200 บาท")
    p.h2("วิธีแก้ราคาเมนู")
    p.step_item(1, "เปิดเบราว์เซอร์ → พิมพ์ supabase.com → กด Sign in", "กรอก email + password ที่เราส่งให้ กด Log in")
    p.step_item(2, "เลือกโปรเจกต์ร้านของคุณ", "จะเห็นชื่อโปรเจกต์ (ชื่อร้าน) อยู่หน้าแรก กดคลิกเข้าไป")
    p.step_item(3, "เมนูซ้ายมือ → กด Table Editor", "จะเห็นรายการตาราง → คลิกตาราง menu")
    p.step_item(4, "หาเมนูที่ต้องการแก้ → คลิกเซลล์ price → พิมพ์ราคาใหม่ → กด Enter", "บันทึกทันที อัปเดตในแอปภายใน 1-2 วินาที")
    p.tip_box("กด Enter แล้ว → แอปเมนูอัปเดตราคาใหม่ทันที ลูกค้าโหลดหน้าใหม่จะเห็นราคาใหม่ ไม่ต้อง deploy ใหม่ ไม่ต้องแจ้งเรา")
    p.h2("วิธีเพิ่มเมนูใหม่")
    p.step_item(1, "Table Editor → menu → กดปุ่ม Insert row (สีเขียว)", "หน้าต่าง New row เปิดขึ้น")
    p.step_item(2, "กรอกข้อมูลเมนูใหม่", "id (เลขไม่ซ้ำ)  ·  cat (หมวด)  ·  name (ชื่อ)  ·  price (ราคา)  ·  description (คำอธิบาย)")
    p.step_item(3, "กด Save → เมนูขึ้นในแอปทันที", "หมายเหตุ: รูปภาพต้องให้เราใส่ให้ (นับเป็น 1 ครั้งของสิทธิ์แก้ไขฟรี)")
    p.h2("แก้หลายรายการพร้อมกันด้วย SQL")
    p.body("ถ้าต้องการแก้ราคาหลายเมนูพร้อมกัน → เมนูซ้าย → SQL Editor → New query → วางโค้ดนี้ → กด Run", size=12, color=MID)
    p.code_box(
        "-- แก้ราคาเมนูเดียว\nUPDATE public.menu SET price = 80 WHERE id = 4;\n\n"
        "-- แก้ราคาหลายเมนูพร้อมกัน\nUPDATE public.menu SET price = 70 WHERE id IN (4, 5, 6);\n\n"
        "-- แก้ชื่อเมนู\nUPDATE public.menu SET name = 'ขาหมูพะโล้สูตรใหม่' WHERE id = 1;"
    )
    p.tip_box("ถ้า Supabase ขึ้น Paused:\nเข้า supabase.com → คลิกโปรเจกต์ → กด Resume project → รอ 1-2 นาที → ใช้งานได้ปกติ\n(เกิดจาก Free tier หยุดอัตโนมัติเมื่อไม่ใช้งาน 7 วัน)", "แก้ปัญหา Supabase Paused")

    # Ch 5
    p.ch_header(5, "ซ่อน / แสดงเมนู\n+ คำถามที่พบบ่อย",
                "เมนูหมดชั่วคราว ปิดได้ 1 คลิก โดยไม่ต้องลบ")
    p.body("เมื่อวัตถุดิบหมด หรืออยากปิดเมนูบางอย่างในวันนั้น ทำได้ง่ายมากครับ ไม่ต้องลบ กลับมาเปิดเมื่อไรก็ได้")
    p.gap()
    p.h2("วิธีซ่อนเมนูชั่วคราว")
    p.step_item(1, "Supabase → Table Editor → ตาราง menu", "หาเมนูที่ต้องการซ่อน")
    p.step_item(2, "มองหาคอลัมน์ is_available", "ค่าปัจจุบัน = true (แสดงอยู่)")
    p.step_item(3, "คลิกเซลล์ → เปลี่ยนเป็น false → กด Enter", "เมนูหายจากแอปทันที ลูกค้าจะไม่เห็น")
    p.step_item(4, "อยากเปิดอีกครั้ง → เปลี่ยนกลับเป็น true → Enter", "เมนูกลับมาแสดงทันที")
    p.tip_box("การซ่อน (false) ไม่ได้ลบข้อมูลออก แค่ซ่อนจากหน้าแอปเท่านั้น เปลี่ยนกลับ true ได้ตลอดเวลา")
    p.h2("คำถามที่พบบ่อย")
    p.faq_item("แก้ราคาแล้วแต่ยังเห็นราคาเดิม?",
               "โหลดหน้าใหม่ (ดึงหน้าจอลง / กด Refresh) ระบบจะดึงข้อมูลใหม่ทันที ถ้ายังไม่เปลี่ยน → ตรวจว่า Supabase ไม่ได้ Paused")
    p.faq_item("Supabase ขึ้น Paused ทำอย่างไร?",
               "เข้า supabase.com → คลิกโปรเจกต์ → กดปุ่ม Resume project สีเขียว → รอ 1-2 นาที → Refresh หน้าแอป")
    p.faq_item("อยากเพิ่มหมวดหมู่ใหม่ ทำเองได้ไหม?",
               "ส่วนนี้ต้องให้เราทำให้ครับ เพราะต้องแก้ในโค้ดแอป แจ้งชื่อหมวดใหม่มาได้เลย นับเป็นการแก้ไข 1 ครั้ง")
    p.faq_item("ใช้สิทธิ์แก้ไขฟรีหมดแล้ว ครั้งต่อไปเสียเท่าไร?",
               "แก้ข้อความ/ราคา → 150 บาท/ครั้ง  ·  เพิ่มเมนูพร้อมรูป → 200 บาท/รายการ  ·  แก้ดีไซน์ → เริ่มต้น 500 บาท\nทักมาได้เลย เราจะ quote ให้ก่อนเสมอ")
    p.contact_box()

    p.thanks_page(
        "หวังว่าระบบเมนู QR Code จะช่วยให้ร้านของคุณ\nให้บริการลูกค้าได้ดียิ่งขึ้น ทั้งไทยและต่างชาติ",
        "ต้องการออเดอร์เข้า LINE OA อัตโนมัติ?\nอัปเกรดเป็นแพ็ก Premium ได้เลย มีส่วนลดสำหรับลูกค้าเดิม"
    )

    out = f"{OUT}/ebook-standard.pdf"
    p.output(out)
    print(f"  Standard: {os.path.getsize(out)//1024} KB  ({out})")


# ══════════════════════════════════════════════════════════════════
# Book 3 — Premium
# ══════════════════════════════════════════════════════════════════

def build_premium():
    p = EbookPDF()

    p.cover(
        "E-Book  ·  แพ็ก 3  ·  Premium",
        "คู่มือการใช้งาน",
        "เมนู QR Code",
        "สั่งผ่าน LINE OA อัตโนมัติ",
        "รองรับ Delivery  ·  ตัวเลือกเมนูครบ  ·  2 ภาษา",
        "5,900 บาท",
        "ได้งานภายใน 7 วัน  ·  แก้ไขฟรี 5 ครั้ง  ·  สอน Zoom 30 นาที",
    )

    p.toc_page([
        ("ยินดีต้อนรับ! คุณได้อะไรบ้าง?",             "ภาพรวมทุกฟีเจอร์ในแพ็ก Premium"),
        ("ข้อมูลที่ต้องเตรียมส่งให้เรา",                "Checklist ครบสำหรับ LINE OA และ Supabase"),
        ("วิธีรับออเดอร์ผ่าน LINE OA (Dine In)",       "ลูกค้าสั่งที่โต๊ะ → ออเดอร์เข้า LINE ร้านทันที"),
        ("วิธีรับออเดอร์ Delivery (สั่งส่งถึงบ้าน)",   "ลูกค้ากรอกที่อยู่ → ออเดอร์ครบใน LINE"),
        ("วิธีแก้ราคาและจัดการเมนูเอง",                "Supabase Dashboard  ·  แก้ราคา  ·  ซ่อนเมนู"),
        ("Zoom สอนงาน + FAQ",                           "หัวข้อที่จะสอน และคำถามที่พบบ่อย"),
    ])

    # Ch 1
    p.ch_header(1, "ยินดีต้อนรับ!\nคุณได้อะไรบ้าง?",
                "ฟีเจอร์ครบถ้วนที่สุดในแพ็ก Premium")
    p.body("แพ็ก Premium เหมาะกับร้านที่ต้องการระบบสั่งอาหารครบวงจร ทั้งทานที่ร้านและส่งถึงบ้าน ออเดอร์ทุกรายการเข้า LINE OA ร้านอัตโนมัติ ไม่มีตกหล่น")
    p.gap()
    p.h2("สิ่งที่คุณได้รับทั้งหมด")
    p.feature_item("เมนูไม่จำกัดจำนวน", "ใส่เมนูได้ไม่จำกัด ไม่มีขีดสูงสุด")
    p.feature_item("ตัวเลือกเมนูครบ", "ขนาด · ประเภทเนื้อ · ท็อปปิ้ง · ความหวาน — เลือกก่อนใส่ตะกร้า ราคาปรับอัตโนมัติ")
    p.feature_item("2 ภาษา ไทย / อังกฤษ สลับได้ทันที", "ตัวเลือก ชื่อเมนู หมวด คำอธิบาย เปลี่ยนทุกหน้าพร้อมกัน")
    p.feature_item("ออเดอร์เข้า LINE OA ร้านอัตโนมัติ", "ลูกค้ากดยืนยัน → ร้านได้รับออเดอร์ครบ (โต๊ะ / เมนู / ราคา / วิธีชำระ) ใน LINE ทันที")
    p.feature_item("รองรับ Delivery ส่งถึงบ้าน", "ลูกค้ากรอกที่อยู่ เลือกรอบส่ง ชำระ PromptPay — ร้านได้ออเดอร์ครบใน LINE")
    p.feature_item("ดีไซน์เฉพาะแบรนด์เต็มรูปแบบ", "สี + โลโก้ + ฟอนต์ตามแบรนด์ร้านทั้งหมด")
    p.feature_item("สอนใช้งานผ่าน Zoom 30 นาที", "สอนแก้ราคา ซ่อนเมนู ดูออเดอร์ใน LINE ครบทุกอย่าง")
    p.feature_item("แก้ไขฟรี 5 ครั้ง (ภายใน 90 วัน)", "ขอแก้งานได้ 5 รอบ ภายใน 3 เดือน")
    p.tip_box("ลูกค้ากดสั่งเอง ออเดอร์เข้า LINE ทันที\nร้านไม่มีออเดอร์ตก ไม่จดผิด", "ข้อดีหลักของแพ็ก Premium")

    # Ch 2
    p.ch_header(2, "ข้อมูลที่ต้องเตรียม\nส่งให้เรา",
                "เตรียมครบ งานเสร็จเร็ว ไม่ต้องส่งซ้ำ")
    p.h2("Checklist ข้อมูลที่ต้องส่ง")
    p.check_item("ชื่อร้าน (ไทย + อังกฤษ)", "เช่น ร้านข้าวขาหมู / Khao Kha Moo Restaurant")
    p.check_item("รายการเมนูทั้งหมด", "ชื่อ + ราคา + หมวด + ตัวเลือก เช่น ขนาด S/M/L ส่งเป็น Excel หรือรูปถ่ายเมนูได้เลย")
    p.check_item("รูปอาหารทุกรายการ", "ยิ่งครบยิ่งดี ถ่ายจากมือถือแสงสว่างได้เลย")
    p.check_item("โลโก้ร้าน (PNG พื้นหลังใส หรือ JPG)", "โลโก้จะแสดงในหัวเมนู")
    p.check_item("สีหลัก + สีรองของแบรนด์", "เช่น แดงเลือดหมู + ครีม หรือ hex code ก็ได้")
    p.check_item("LINE OA Channel Access Token", "ขอได้จาก LINE Developer Console → Messaging API → Issue token (ขอแบบ Long-lived ไม่หมดอายุ)")
    p.check_item("อีเมลสำหรับสร้างบัญชี Supabase", "ใช้ login เข้าแก้ราคาและดูออเดอร์ในภายหลัง")
    p.tip_box("LINE OA Token คืออะไร?\nคือรหัสลับที่ใช้ให้ระบบเมนูส่งข้อความเข้า LINE OA ร้านของคุณได้\nขอได้ที่ developers.line.biz → Channel → Messaging API → Issue a Longterm channel access token\nถ้าไม่แน่ใจ — ทักเราได้เลย เราจะแนะนำขั้นตอนทีละขั้น")
    p.tip_box("ส่ง LINE OA Token ให้เราผ่าน LINE Direct (1:1) เท่านั้น อย่าโพสต์ลง Group หรือ Feed เพราะคนอื่นเอาไปใช้ได้", "ข้อควรระวัง")

    # Ch 3
    p.ch_header(3, "วิธีรับออเดอร์\nผ่าน LINE OA",
                "สำหรับลูกค้าที่ทานที่ร้าน (Dine In)")
    p.h2("ขั้นตอนฝั่งลูกค้า")
    p.step_item(1, "สแกน QR ที่โต๊ะ → เลือกหมายเลขโต๊ะ", "เปิดกล้องมือถือ → สแกน QR → เลือกโต๊ะของตัวเอง")
    p.step_item(2, "เลือกเมนู → เลือกตัวเลือก → เพิ่มลงตะกร้า", "เลือกขนาด / ประเภทเนื้อ / ความหวาน → ราคาปรับอัตโนมัติ")
    p.step_item(3, "ตรวจรายการในตะกร้า → กดยืนยัน", "เลือกวิธีชำระ: QR PromptPay หรือ เงินสด")
    p.step_item(4, "ออเดอร์เข้า LINE ร้านทันที!", "ร้านได้รับ: โต๊ะ + รายการ + ราคา + วิธีชำระ ครบ")
    p.h2("ตัวอย่างออเดอร์ที่เข้า LINE OA ร้าน")
    p.code_box(
        "ออเดอร์ใหม่  ·  จากระบบเมนู QR\n"
        "โต๊ะ 3\n\n"
        "ขาหมูพะโล้เตาถ่าน (ชุดใหญ่)    180 บาท\n"
        "ข้าวขาหมูพะโล้ x2                120 บาท\n"
        "กาแฟลาเต้เย็น (M)                 75 บาท\n\n"
        "ยอดรวม: 375 บาท\n"
        "วิธีชำระ: QR PromptPay\n"
        "หมายเหตุ: ไม่ใส่ผัก"
    )
    p.tip_box("ข้อมูลออเดอร์มาครบ ทั้งโต๊ะ เมนู ราคา วิธีชำระ หมายเหตุ — ไม่ต้องรอถามลูกค้าเพิ่ม")
    p.h2("ลูกค้าเลือกชำระแบบ QR PromptPay")
    p.step_item(1, "หน้าจอแสดง QR PromptPay ยอดรวม", "ลูกค้าสแกน QR ด้วยแอปธนาคาร → โอนเงิน")
    p.step_item(2, "แนบสลิปส่งมาใน LINE OA", "ลูกค้าแคปหน้าจอสลิป → ส่งใน LINE OA ร้าน")
    p.step_item(3, "ร้านตรวจสลิป → เริ่มทำอาหาร", "ยืนยันรับเงินแล้วจัดการออเดอร์ได้เลย")

    # Ch 4
    p.ch_header(4, "วิธีรับออเดอร์\nDelivery",
                "ลูกค้าสั่งส่งถึงบ้าน — ร้านได้ทุกอย่างใน LINE")
    p.h2("ขั้นตอนฝั่งลูกค้า")
    p.step_item(1, "เปิดเมนู → กดปุ่ม ส่งถึงบ้าน", "ปุ่มอยู่หน้าแรก เลือกเมนูตามต้องการได้เลย")
    p.step_item(2, "เลือกเมนู → เลือกตัวเลือก → เพิ่มลงตะกร้า", "เหมือนการสั่ง Dine In ทุกอย่าง")
    p.step_item(3, "กรอกข้อมูลจัดส่ง", "ชื่อ  ·  เบอร์โทร  ·  ที่อยู่  ·  เลือกรอบส่ง (เช้า / บ่าย)")
    p.step_item(4, "ชำระผ่าน QR PromptPay → แนบสลิป + ส่งโลเคชั่น", "โอนเงิน → แคปสลิป → ส่ง Pin โลเคชั่นบ้านผ่าน LINE OA")
    p.step_item(5, "ร้านได้รับออเดอร์ + ที่อยู่ + สลิป ครบใน LINE", "ยืนยัน → จัดส่งตามรอบที่ลูกค้าเลือก")
    p.h2("ตัวอย่างออเดอร์ Delivery ที่เข้า LINE OA")
    p.code_box(
        "Delivery ใหม่  ·  รอบบ่าย\n\n"
        "คุณสมหญิง  ·  081-234-5678\n\n"
        "ขาหมูพะโล้เตาถ่าน (ชุดใหญ่)    180 บาท\n"
        "ข้าวขาหมูพะโล้ x2                120 บาท\n\n"
        "ยอดรวม: 300 บาท\n"
        "ที่อยู่: รอ Pin โลเคชั่น"
    )
    p.tip_box("แนะนำตั้ง 2 รอบ: เช้า (ส่ง 11:00) และบ่าย (ส่ง 14:00)\nลูกค้าเลือกรอบได้เลย ร้านรวมออเดอร์ส่งครั้งเดียวประหยัดเวลา", "แนะนำกำหนดรอบส่งชัดเจน")
    p.tip_box("ระบบแสดงข้อมูลโซน: ≤5km ฟรี / มากกว่า 5km คิดตามระยะ ลูกค้าเห็นก่อนสั่ง เพื่อไม่ให้เกิดความเข้าใจผิด", "ค่าส่งและระยะ")

    # Ch 5
    p.ch_header(5, "วิธีแก้ราคาและ\nจัดการเมนูเอง",
                "ผ่านเว็บ Supabase  ·  ไม่ต้องรู้โค้ด  ·  เสร็จภายใน 1 นาที")
    p.tip_box("Supabase คืออะไร?\nSupabase คือเว็บจัดการข้อมูลเมนูร้านของคุณ เหมือน Google Sheets แต่เชื่อมกับแอปเมนูโดยตรง แก้ราคาในนั้น → เมนูในแอปอัปเดตทันที เข้าใช้ผ่านเบราว์เซอร์ปกติ ไม่ต้องติดตั้งโปรแกรม")
    p.h2("แก้ราคา ชื่อ หรือคำอธิบายเมนู")
    p.step_item(1, "เปิดเบราว์เซอร์ → supabase.com → Sign in", "ใช้ email + password ที่เราส่งให้")
    p.step_item(2, "เลือกโปรเจกต์ร้านของคุณ", "กดคลิกชื่อโปรเจกต์ที่หน้าแรก")
    p.step_item(3, "เมนูซ้ายมือ → Table Editor → ตาราง menu", "จะเห็นรายการเมนูทั้งหมด")
    p.step_item(4, "คลิกเซลล์ที่ต้องการแก้ → พิมพ์ค่าใหม่ → Enter", "แก้ได้ทั้ง price (ราคา) / name (ชื่อ) / description (คำอธิบาย)")
    p.tip_box("กด Enter แล้วเมนูในแอปอัปเดตภายใน 1-2 วินาที ไม่ต้อง deploy ใหม่ ไม่ต้องแจ้งเรา")
    p.h2("ซ่อน / แสดงเมนูชั่วคราว")
    p.body("เมื่อวัตถุดิบหมด หรืออยากปิดชั่วคราว — ทำได้ใน 3 คลิก โดยไม่ลบเมนูออก", size=12, color=MID)
    p.step_item(1, "Table Editor → menu → หาเมนูที่ต้องซ่อน", "")
    p.step_item(2, "คลิกเซลล์ is_available → เปลี่ยนเป็น false → Enter", "เมนูหายจากแอปทันที · เปลี่ยนกลับเป็น true เมื่อต้องการแสดงอีกครั้ง")
    p.h2("แก้หลายรายการด้วย SQL")
    p.code_box(
        "-- แก้ราคาเมนูเดียว\nUPDATE public.menu SET price = 200 WHERE id = 1;\n\n"
        "-- ซ่อนเมนู (วัตถุดิบหมด)\nUPDATE public.menu SET is_available = false WHERE id = 5;\n\n"
        "-- แสดงเมนูอีกครั้ง\nUPDATE public.menu SET is_available = true WHERE id = 5;"
    )
    p.tip_box("ถ้า Supabase ขึ้น Paused:\nเข้า supabase.com → คลิกโปรเจกต์ → กด Resume project → รอ 1-2 นาที → ใช้งานได้ปกติ", "แก้ปัญหา")

    # Ch 6
    p.ch_header(6, "Zoom สอนงาน\n+ คำถามที่พบบ่อย",
                "หัวข้อที่จะสอนใน Zoom 30 นาที และ FAQ")
    p.body("หลังส่งมอบงาน เราจะนัด Zoom สอนการใช้งานจริง 30 นาที")
    p.gap()
    p.h2("หัวข้อ Zoom สอนงาน 30 นาที")
    for topic, detail in [
        ("วิธีแก้ราคาและชื่อเมนูใน Supabase Dashboard", "ทำให้ดูทีละขั้น จนทำเองได้มั่นใจ"),
        ("วิธีซ่อน / แสดงเมนู", "เมื่อวัตถุดิบหมดหรืออยากปิดชั่วคราว"),
        ("วิธีดูและตอบออเดอร์ใน LINE OA", "รับออเดอร์ ยืนยัน และสื่อสารกับลูกค้า"),
        ("วิธีดูประวัติออเดอร์ทั้งหมด", "เข้าดูออเดอร์ย้อนหลังใน Supabase ได้"),
        ("วิธีขอแก้ไขงาน", "วิธีทักและแจ้งรายการที่ต้องการแก้ไข"),
    ]:
        p.feature_item(topic, detail)
    p.tip_box("แนะนำขอ Record การสอน Zoom ไว้ด้วย จะได้กลับมาดูทบทวนได้เมื่อไรก็ได้")
    p.h2("คำถามที่พบบ่อย")
    p.faq_item("ออเดอร์ไม่เข้า LINE OA ทำอย่างไร?",
               "ตรวจสอบว่า LINE OA ยังออนไลน์ และ Token ไม่ถูกลบ ถ้ายังผิดปกติ แจ้งเราทาง LINE เราตรวจสอบให้ภายใน 24 ชั่วโมง")
    p.faq_item("ลูกค้าสแกน QR แล้วไม่เปิด?",
               "ใช้กล้องมือถือปกติ (ไม่ต้องโหลดแอปพิเศษ) ถ้ายังไม่ขึ้น → ลองกดค้างที่ QR แล้วเลือก เปิดลิงก์ หรือใช้กล้องใน LINE")
    p.faq_item("LINE Token หมดอายุไหม?",
               "ถ้าขอแบบ Long-lived token (ตามที่เราแนะนำ) — ไม่หมดอายุ ใช้ได้ตลอด ไม่ต้อง renew ทุกเดือน")
    p.faq_item("อยากเพิ่มตัวเลือกเมนูใหม่ เช่น ท็อปปิ้งใหม่ ทำเองได้ไหม?",
               "ส่วนนี้ต้องให้เราทำให้ครับ แจ้งรายละเอียดมาได้เลย นับเป็นการแก้ไข 1 ครั้ง")
    p.faq_item("ใช้สิทธิ์แก้ไขฟรีหมดแล้ว ครั้งต่อไปเสียเท่าไร?",
               "แก้ข้อความ/ราคา → 150 บาท/ครั้ง  ·  เพิ่มเมนูพร้อมรูป → 200 บาท/รายการ  ·  เพิ่มตัวเลือก/หมวด → 300 บาท  ·  แก้ดีไซน์ → เริ่มต้น 500 บาท")
    p.contact_box()

    p.thanks_page(
        "หวังว่าระบบเมนู QR Code จะช่วยให้ร้านของคุณ\nให้บริการลูกค้าได้สะดวกยิ่งขึ้น ลดความผิดพลาด\nและเพิ่มยอดขายได้ในระยะยาว",
        "อย่าลืมนัด Zoom สอนงาน!\nทักเราเพื่อนัดวัน/เวลาที่สะดวก"
    )

    out = f"{OUT}/ebook-premium.pdf"
    p.output(out)
    print(f"  Premium:  {os.path.getsize(out)//1024} KB  ({out})")


if __name__ == "__main__":
    print("Generating E-book PDFs with fpdf2...")
    build_basic()
    build_standard()
    build_premium()
    print("Done!")
