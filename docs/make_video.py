#!/usr/bin/env python3
"""
Generate presentation video from slide content + Thai TTS narration.
Uses PIL for slide rendering (no browser needed) + gTTS + moviepy.
"""
import os, textwrap
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

DOCS  = Path("/home/user/khaomoo-menu/docs")
OUT   = DOCS / "slides-premium-video.mp4"
FONT_REG  = "/tmp/fonts/Sarabun-Regular.ttf"
FONT_BOLD = "/tmp/fonts/Sarabun-Bold.ttf"

# Canvas 1920×1080 (1080p 16:9)
W, H = 1920, 1080

# Colors (RGB tuples)
SAGE     = (135,160,128); SAGE_L = (236,242,235); SAGE_D = (85,114,82)
CREAM    = (248,245,239); DARK   = (42,42,42);   MID    = (94,94,94)
WHITE    = (255,255,255); RED    = (220,38,38)
G_GOOD   = (22,101,52);  G_BG   = (240,253,244); G_BOR  = (34,197,94)
WARN_BG  = (255,249,230); WARN_FG= (122,85,0);   WARN_BD= (204,160,16)
HINT_BG  = (238,242,255); HINT_FG= (55,48,163);  HINT_BD= (99,102,241)
DB_BG    = (15,23,42);   DB_MID = (30,41,59);   DB_GRN = (62,207,142)
DB_RED   = (248,113,113); DB_TXT= (203,213,225); DB_MUT = (148,163,184)
LINE_GN  = (238,255,221); LINE_HD= (54,61,68)
CODE_BG  = (30,41,59);   CODE_BL= (125,211,252); CODE_GN= (134,239,172)
CODE_PR  = (192,132,252); CODE_YL= (252,211,77);  CODE_GR= (71,85,105)

def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REG
    return ImageFont.truetype(path, size)

def wrap(text, font_obj, max_w, draw):
    """Word-wrap Thai/mixed text to fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bb = draw.textbbox((0,0), test, font=font_obj)
        if bb[2] > max_w and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines

def new_img(bg=WHITE):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)

def draw_text(d, text, x, y, size=28, bold=False, color=DARK, align="left", max_w=None):
    f = font(size, bold)
    if max_w:
        lines = wrap(text, f, max_w, d)
    else:
        lines = [text]
    for line in lines:
        bb = d.textbbox((0,0), line, font=f)
        tw = bb[2]-bb[0]
        if align == "center":
            d.text((x - tw//2, y), line, font=f, fill=color)
        elif align == "right":
            d.text((x - tw, y), line, font=f, fill=color)
        else:
            d.text((x, y), line, font=f, fill=color)
        y += bb[3]-bb[1] + 4
    return y

def draw_rect(d, x,y,w,h, fill=None, outline=None, radius=12):
    d.rounded_rectangle([x,y,x+w,y+h], radius=radius, fill=fill, outline=outline, width=3)

def draw_badge(d, text, x, y, w=240):
    draw_rect(d, x, y, w, 44, fill=SAGE)
    draw_text(d, text, x+w//2, y+6, size=22, bold=True, color=WHITE, align="center")

def draw_header(d, badge_text, title, bg=WHITE):
    draw_badge(d, badge_text, 50, 28)
    draw_text(d, title, 50, 82, size=52, bold=True, color=DARK, max_w=1820)
    d.rectangle([50,162,1870,170], fill=SAGE_L)

def draw_tip(d, title, body, x,y,w,h, bg_c=SAGE_L, tc=SAGE_D, bc=SAGE):
    draw_rect(d, x, y, 14, h, fill=bc, radius=4)
    draw_rect(d, x+14, y, w-14, h, fill=bg_c, radius=8)
    cy = y + 14
    cy = draw_text(d, title, x+28, cy, size=26, bold=True, color=tc, max_w=w-50)
    draw_text(d, body, x+28, cy+4, size=22, color=DARK, max_w=w-50)

def draw_step(d, num, title, body, x, y):
    draw_rect(d, x, y, 52, 52, fill=SAGE, radius=26)
    draw_text(d, str(num), x+26, y+6, size=26, bold=True, color=WHITE, align="center")
    ty = draw_text(d, title, x+68, y+4, size=28, bold=True, color=DARK, max_w=W-x-120)
    if body:
        draw_text(d, body, x+68, ty+2, size=22, color=MID, max_w=W-x-120)

def save_slide(img, i):
    path = f"/tmp/slide_{i:02d}.png"
    img.save(path, "PNG")
    return path

# ── Slides ───────────────────────────────────────────────────────────────────
slides_paths = []

# SLIDE 1 — Cover
img, d = new_img(SAGE)
draw_text(d,"สไลด์สอนงาน · แพ็ก Premium",W//2,60,size=28,bold=True,color=WHITE,align="center")
draw_text(d,"🚀",W//2,120,size=80,color=WHITE,align="center")
draw_text(d,"สอนใช้งาน แพ็ก Premium",W//2,260,size=88,bold=True,color=WHITE,align="center")
draw_text(d,"QR Code เมนูครบวงจร  ·  ออเดอร์เข้า LINE OA  ·  Delivery  ·  2 ภาษา",
          W//2,400,size=34,color=WHITE,align="center")
draw_rect(d,W//2-340,500,680,70,fill=WHITE,radius=14)
draw_text(d,"← กด ← → หรือปัดซ้าย/ขวา →",W//2,514,size=26,color=SAGE_D,align="center")
slides_paths.append(save_slide(img,1))

# SLIDE 2 — Features
img, d = new_img(WHITE)
draw_header(d,"ภาพรวม","แพ็ก Premium — ได้อะไรบ้าง?")
feats=[("💬","ออเดอร์เข้า LINE OA","ลูกค้ากดยืนยัน → ร้านได้รับออเดอร์ทันที"),
       ("🏠","Delivery ส่งถึงบ้าน","กรอกที่อยู่ + PromptPay ครบในขั้นตอนเดียว"),
       ("🌐","2 ภาษา ไทย / EN","กดปุ่มสลับ ทุกหน้าเปลี่ยนพร้อมกัน"),
       ("🎛️","ตัวเลือกเมนูครบ","ขนาด · เนื้อ · ท็อปปิ้ง · ความหวาน"),
       ("✏️","แก้ราคาเองได้","Supabase Dashboard คลิก แก้ Enter เสร็จ"),
       ("👁️","ซ่อน/แสดงเมนู","ของหมด ซ่อน 1 คลิก ไม่ต้องลบถาวร")]
cols=[(50,185),(660,185),(1270,185),(50,580),(660,580),(1270,580)]
for i,(ic,ti,bo) in enumerate(feats):
    cx,cy=cols[i]; cw=580; ch=360
    draw_rect(d,cx,cy,cw,ch,fill=SAGE_L,radius=18)
    draw_text(d,ic+" "+ti,cx+24,cy+22,size=30,bold=True,color=DARK,max_w=cw-40)
    draw_text(d,bo,cx+24,cy+90,size=24,color=MID,max_w=cw-40)
slides_paths.append(save_slide(img,2))

# SLIDE 3 — Dine In
img, d = new_img(WHITE)
draw_header(d,"Dine In","ขั้นตอนลูกค้าทานที่ร้าน")
flow=[("📷","สแกน QR"),("🪑","เลือกโต๊ะ"),("🍽️","เลือกเมนู"),
      ("🛒","ตรวจตะกร้า"),("💳","จ่ายเงิน"),("💬","เข้า LINE!")]
fw=280; fy=185
for i,(ic,lb) in enumerate(flow):
    fx=50+i*(fw+30)
    fc=LINE_GN if i==5 else SAGE_L
    draw_rect(d,fx,fy,fw,90,fill=fc,radius=14)
    draw_text(d,ic+"  "+lb,fx+fw//2,fy+18,size=24,bold=True,color=DARK,align="center")
    if i<5:
        draw_text(d,"→",fx+fw+2,fy+28,size=32,color=SAGE_D,align="left")
steps=[("1","สแกน QR ที่โต๊ะ — ไม่ต้องโหลดแอป","ใช้กล้องมือถือปกติ ทั้ง iPhone และ Android"),
       ("2","เลือกหมายเลขโต๊ะ","โต๊ะติดมากับออเดอร์อัตโนมัติ ร้านไม่ต้องถามซ้ำ"),
       ("3","เลือกเมนู + ตัวเลือก → ใส่ตะกร้า","ขนาด / เนื้อ / ความหวาน ราคาปรับทุกตัวเลือก"),
       ("4","ยืนยัน → เลือกวิธีชำระ","PromptPay หรือเงินสด → ออเดอร์เข้า LINE ร้านทันที")]
for i,(n,t,b) in enumerate(steps):
    draw_step(d,n,t,b,50,310+i*178)
slides_paths.append(save_slide(img,3))

# SLIDE 4 — LINE Order (real data)
img, d = new_img(WHITE)
draw_header(d,"LINE OA","ออเดอร์จริงที่เข้ามาใน LINE ร้าน")
# phone frame
draw_rect(d,50,185,620,860,fill=WHITE,outline=(42,42,42),radius=20)
# LINE header
draw_rect(d,50,185,620,70,fill=LINE_HD,radius=20)
draw_text(d,"← ขาหมูนาย ต.  ☏  ⋮",70,198,size=24,bold=True,color=WHITE)
# chat bg
draw_rect(d,50,255,620,790,fill=(240,240,240),radius=0)
# bubble
draw_rect(d,100,275,540,720,fill=LINE_GN,radius=16)
cy=295
for ln,sz,bl,col in [
    ("📩 ระบบเมนู QR — ออเดอร์ใหม่",20,False,MID),
    ("🍖 ออเดอร์ใหม่! โต๊ะ 6",28,True,DARK),
    ("",14,False,DARK),
    ("ชุดไส้พะโล้เตาถ่าน ×2 (ไส้ล้วน) 200฿",22,False,DARK),
    ("ชุดขาหมูพะโล้สับ ×2 (เนื้อหนัง) 200฿",22,False,DARK),
    ("ชุดคากิพะโล้สับ ×2 200฿",22,False,DARK),
    ("ไข่เปิ๊ดต้ม ×7 70฿",22,False,DARK),
    ("ข้าวเปล่า ×7 70฿",22,False,DARK),
    ("",14,False,DARK),
    ("────────────────────────",16,False,(134,239,172)),
    ("💰 ยอดรวม  740฿",28,True,DARK),
    ("💳 ชำระ: เงินสด",20,False,MID),
    ("📝 หมายเหตุ: เนื้อสัตว์กะเอิน",20,False,MID),
]:
    if ln:
        cy = draw_text(d,ln,118,cy,size=sz,bold=bl,color=col,max_w=500)
    else:
        cy += sz
draw_text(d,"12:19 น.",520,972,size=18,color=MID)

# right panel
draw_tip(d,"✅ ข้อมูลครบทุกอย่าง — ไม่ต้องถามเพิ่ม",
         "โต๊ะ · รายการ · ตัวเลือก · จำนวน · ยอดรวม · วิธีชำระ · หมายเหตุ\nร้านรับออเดอร์แล้วเริ่มทำได้เลย",
         700,185,1170,200,bg_c=G_BG,tc=G_GOOD,bc=G_BOR)
draw_tip(d,"💳 ลูกค้าเลือก QR PromptPay",
         "แสดง QR บนหน้าจอ → สแกนโอน → แคปสลิปส่ง LINE OA\nร้านยืนยันรับเงินก่อนเริ่มทำ",
         700,410,1170,180)
draw_tip(d,"📊 ดูออเดอร์ย้อนหลังได้ตลอด",
         "ออเดอร์ทุกโต๊ะเข้า LINE เดียวกัน เรียงตามเวลา\nสามารถตรวจสอบย้อนหลังและพิมพ์ใบเสร็จได้",
         700,615,1170,180,bg_c=HINT_BG,tc=HINT_FG,bc=HINT_BD)
slides_paths.append(save_slide(img,4))

# SLIDE 5 — Delivery
img, d = new_img(WHITE)
draw_header(d,"Delivery","ขั้นตอนลูกค้าสั่งส่งถึงบ้าน")
steps5=[("1","กดปุ่ม 'ส่งถึงบ้าน' ที่หน้าแรก","ปุ่มอยู่ก่อนเลือกโต๊ะ — สั่งจากบ้านได้เลย"),
        ("2","เลือกเมนูและตัวเลือก เหมือน Dine In","ใส่ตะกร้าได้หลายรายการ"),
        ("3","กรอกข้อมูลจัดส่ง","ชื่อ · เบอร์โทร · ที่อยู่ · เลือกรอบส่ง"),
        ("4","ชำระ PromptPay → แคปสลิป → ส่ง LINE OA","พร้อมส่ง Pin โลเคชั่นด้วย"),
        ("5","ร้านได้รับออเดอร์ + ที่อยู่ + สลิป ครบใน LINE","ยืนยัน → จัดส่งตามรอบที่เลือก")]
for i,(n,t,b) in enumerate(steps5):
    draw_step(d,n,t,b,50,185+i*162)
draw_tip(d,"💡 แนะนำตั้ง 2 รอบส่ง: เช้า 11:00 + บ่าย 14:00",
         "ลูกค้าเลือกเอง ร้านรวมออเดอร์ส่งครั้งเดียว ประหยัดเวลาและค่าน้ำมัน",
         50,1000,1870,70,bg_c=HINT_BG,tc=HINT_FG,bc=HINT_BD)
slides_paths.append(save_slide(img,5))

# SLIDE 6 — Chapter
img, d = new_img(SAGE)
draw_text(d,"⭐  สำคัญที่สุด — เน้นเป็นพิเศษ",W//2,140,size=32,bold=True,color=WHITE,align="center")
draw_text(d,"ซ่อน / แสดง",W//2,260,size=110,bold=True,color=WHITE,align="center")
draw_text(d,"เมนูชั่วคราว",W//2,400,size=110,bold=True,color=WHITE,align="center")
draw_text(d,"เมื่อวัตถุดิบหมด หรืออยากปิดเมนูชั่วคราว",W//2,600,size=36,color=WHITE,align="center")
draw_text(d,"ทำได้เองใน 3 คลิก โดยไม่ต้องลบออกถาวร",W//2,650,size=36,color=WHITE,align="center")
slides_paths.append(save_slide(img,6))

# SLIDE 7 — Why hide
img, d = new_img(WHITE)
draw_header(d,"ซ่อนเมนู","ใช้ซ่อนเมนูเมื่อไร?")
scenarios=[("🥩","วัตถุดิบหมดวันนั้น",
            "เช่น ขาหมูขายหมดก่อนร้านปิด ซ่อนทันที ไม่ให้ลูกค้าสั่งเพิ่ม วันรุ่งขึ้นเปิดกลับมา"),
           ("⏸️","ปิดเมนูชั่วคราว",
            "เมนูฤดูกาล หรือรับออเดอร์ได้บางวัน ซ่อนแทนการลบ เปิดได้ตลอด"),
           ("🔧","อยู่ระหว่างปรับราคา",
            "ซ่อนไว้ก่อนระหว่างแก้ราคา แก้เสร็จแล้วค่อยเปิดให้ลูกค้าเห็น")]
for i,(ic,ti,bo) in enumerate(scenarios):
    sy=190+i*258
    draw_rect(d,50,sy,1870,230,fill=SAGE_L,radius=18)
    draw_text(d,ic+"  "+ti,74,sy+20,size=34,bold=True,color=DARK,max_w=1820)
    draw_text(d,bo,74,sy+80,size=26,color=MID,max_w=1820)
draw_tip(d,"✅ ซ่อน ≠ ลบ — ข้อมูลยังอยู่ครบทุกอย่าง",
         "รูปภาพ ราคา ตัวเลือก ทุกอย่างยังอยู่ในระบบ เพียงแต่ลูกค้าไม่เห็นชั่วคราว",
         50,980,1870,80,bg_c=G_BG,tc=G_GOOD,bc=G_BOR)
slides_paths.append(save_slide(img,7))

# SLIDE 8 — Open Supabase
img, d = new_img(WHITE)
draw_header(d,"ซ่อนเมนู · ขั้น 1","เปิดเว็บ Supabase")
steps8=[("1","เปิดเบราว์เซอร์ → พิมพ์  supabase.com",""),
        ("2","กด Sign in → กรอก Email + Password ที่เราส่งให้ทาง LINE",""),
        ("3","คลิกชื่อโปรเจกต์ร้านของคุณ (เห็นในหน้าแรก)",""),
        ("4","เมนูซ้ายมือ → กด 'Table Editor' → คลิกตาราง  menu","")]
for i,(n,t,b) in enumerate(steps8):
    draw_step(d,n,t,b,50,185+i*192)
draw_tip(d,"💡 เคล็ดลับสำคัญ: Bookmark URL ไว้เลย!",
         "เข้า Table Editor ครั้งแรก → กด Bookmark ในเบราว์เซอร์ทันที\nครั้งต่อไปกดบุ๊กมาร์กได้เลย ไม่ต้องคลิกหลายขั้น",
         50,960,1870,100,bg_c=HINT_BG,tc=HINT_FG,bc=HINT_BD)
slides_paths.append(save_slide(img,8))

# SLIDE 9 — Table Editor
img, d = new_img(CREAM)
draw_header(d,"ซ่อนเมนู · ขั้น 2","หน้าตา Table Editor ใน Supabase")
draw_text(d,"หลังกด Table Editor แล้วคลิก 'menu' จะเห็นตารางแบบนี้:",
          50,175,size=26,color=MID)
# DB mockup
def db_row(d,y,h,bg,cells):
    draw_rect(d,50,y,1870,h,fill=bg,radius=0)
    x=70
    for t,c,sz,bl in cells:
        draw_text(d,t,x,y+8,size=sz,bold=bl,color=c)
        x+=t.__len__()*sz//2+30 if len(t)<20 else 480

db_row(d,220,56,DB_BG,[("⚡ Supabase ",DB_GRN,24,True),
    ("  ›  ขาหมูนาย ต.  ›  Table Editor  ›  ",DB_MUT,22,False),("menu",DB_GRN,22,True)])
db_row(d,276,40,DB_MID,[("Authentication   ",DB_MUT,20,False),
    ("● Table Editor   ",DB_GRN,20,True),("SQL Editor   Storage",DB_MUT,20,False)])
db_row(d,316,42,DB_MID,[("id      ",DB_MUT,20,True),("name (ชื่อเมนู)                              ",DB_MUT,20,True),
    ("price    ",DB_MUT,20,True),("is_available",DB_MUT,20,True)])
rows=[("1 ","ขาหมูพะโล้เตาถ่าน (ชุดใหญ่)           ","180  ","✓ true",True),
      ("5 ","ชุดไส้พะโล้เตาถ่าน                     ","100  ","✓ true",True),
      ("4 ","ข้าวขาหมูพะโล้เตาถ่าน                  ","60   ","✓ true",True),
      ("7 ","กาแฟสด Premium                         ","65   ","✓ true",True)]
for ri,(id_,nm,pr,av,tval) in enumerate(rows):
    ry=358+ri*78
    db_row(d,ry,74,DB_BG,[
        (id_,DB_TXT,22,False),(nm,DB_TXT,22,False),(pr,DB_TXT,22,False),
        (av,DB_GRN if tval else DB_RED,22,True)])

draw_text(d,"☝️  คอลัมน์ is_available ด้านขวา คือตัวควบคุม   true = แสดง   false = ซ่อน",
          50,680,size=30,bold=True,color=RED)
draw_tip(d,"ℹ️  is_available = 'มีพร้อมสั่งไหม?'",
         "true = มีพร้อมสั่ง (ลูกค้าเห็น)  ·  false = ไม่มี (ลูกค้าไม่เห็น แต่ข้อมูลยังอยู่ในระบบ)",
         50,760,1870,130)
slides_paths.append(save_slide(img,9))

# SLIDE 10 — Click false
img, d = new_img(CREAM)
draw_header(d,"ซ่อนเมนู · ขั้น 3","คลิกเซลล์ → พิมพ์ false → กด Enter")
draw_text(d,"ตัวอย่าง: ต้องการซ่อน 'ชุดไส้พะโล้เตาถ่าน' เพราะขายหมด",
          50,175,size=26,color=MID)
db_row(d,216,52,DB_BG,[("⚡ Supabase ",DB_GRN,24,True),("  ›  Table Editor › menu",DB_MUT,22,False)])
db_row(d,268,40,DB_MID,[("id      ",DB_MUT,20,True),("name (ชื่อเมนู)                              ",DB_MUT,20,True),
    ("price    ",DB_MUT,20,True),("is_available",DB_MUT,20,True)])
rows10=[("1 ","ขาหมูพะโล้เตาถ่าน (ชุดใหญ่)           ","180  ","✓ true",True,False),
        ("5 ","ชุดไส้พะโล้เตาถ่าน                     ","100  ","false|",False,True),
        ("4 ","ข้าวขาหมูพะโล้เตาถ่าน                  ","60   ","✓ true",True,False)]
for ri,(id_,nm,pr,av,tval,hl) in enumerate(rows10):
    ry=308+ri*90
    rbg=(13,33,22) if hl else DB_BG
    draw_rect(d,50,ry,1870,86,fill=rbg,radius=0)
    if hl:
        draw_rect(d,50,ry,1870,86,fill=None,outline=DB_GRN,radius=0)
    x=70
    for t,c,bl in [(id_,DB_TXT,False),(nm,CODE_YL if hl else DB_TXT,hl),
                   (pr,DB_TXT,False),(av,DB_RED if not tval else DB_GRN,True)]:
        draw_text(d,t,x,ry+18,size=24,bold=bl,color=c)
        x += len(t)*14+30 if len(t) < 10 else 480

draw_text(d,"⬆️  แถวนี้กำลังแก้ไข — พิมพ์  false  แล้วกด  Enter  เมนูหายทันที",
          50,590,size=30,bold=True,color=RED)
draw_step(d,"①","ดับเบิลคลิกที่เซลล์ is_available ของเมนูที่ต้องการซ่อน",
          "เซลล์เข้าโหมดแก้ไข เห็น cursor กะพริบ",50,680)
draw_step(d,"②","ลบค่าเดิม พิมพ์ false (ตัวเล็กทั้งหมด) → Enter",
          "เมนูหายจากแอปลูกค้าทันที ไม่ต้อง Refresh",50,880)
slides_paths.append(save_slide(img,10))

# SLIDE 11 — Before/After
img, d = new_img(WHITE)
draw_header(d,"ผลลัพธ์","ลูกค้าเห็นอะไร ก่อน / หลัง ซ่อนเมนู")
# Before
draw_rect(d,50,185,880,660,fill=WHITE,outline=(254,202,202),radius=16)
draw_rect(d,50,185,880,64,fill=(254,226,226),radius=16)
draw_text(d,"ก่อนซ่อน ❌",490,196,size=28,bold=True,color=(153,27,27),align="center")
bf=[("🍖 ขาหมูพะโล้","180฿",False),("🫀 ชุดไส้พะโล้","100฿",True),
    ("🍚 ข้าวขาหมู","60฿",False),("☕ กาแฟสด","65฿",False)]
for bi,(nm,pr,hl) in enumerate(bf):
    by=265+bi*120
    if hl: draw_rect(d,60,by,860,110,fill=(254,249,195),radius=8)
    draw_text(d,nm,80,by+24,size=28,bold=hl,color=DARK)
    draw_text(d,pr,840,by+24,size=28,bold=hl,color=DARK,align="right")
# After
draw_rect(d,990,185,880,660,fill=WHITE,outline=(134,239,172),radius=16)
draw_rect(d,990,185,880,64,fill=(220,252,231),radius=16)
draw_text(d,"หลังซ่อน ✅",1430,196,size=28,bold=True,color=G_GOOD,align="center")
af=[("🍖 ขาหมูพะโล้","180฿"),("🍚 ข้าวขาหมู","60฿"),("☕ กาแฟสด","65฿")]
for ai,(nm,pr) in enumerate(af):
    ay=265+ai*120
    draw_text(d,nm,1010,ay+24,size=28,color=DARK)
    draw_text(d,pr,1780,ay+24,size=28,color=DARK,align="right")
draw_text(d,"✓ 'ชุดไส้' หายออกไปแล้ว",1010,645,size=24,bold=True,color=(22,163,74))

draw_tip(d,"↩️ อยากเปิดกลับมา?",
         "ดับเบิลคลิกเซลล์เดิม → พิมพ์ true → Enter  เมนูกลับมาทันที",
         50,880,1870,90,bg_c=WARN_BG,tc=WARN_FG,bc=WARN_BD)
draw_tip(d,"✅ ซ่อนไม่ลบ — ข้อมูลไม่หายไปไหน",
         "รูปภาพ ราคา ตัวเลือก ทุกอย่างยังอยู่ครบ แค่ลูกค้าไม่เห็นชั่วคราว",
         50,988,1870,80,bg_c=G_BG,tc=G_GOOD,bc=G_BOR)
slides_paths.append(save_slide(img,11))

# SLIDE 12 — SQL
img, d = new_img(WHITE)
draw_header(d,"💡 ข้อเสนอแนะ","วิธีเร็วกว่า — ใช้ SQL แทน Table Editor")
draw_tip(d,"🎯 ทำไม SQL ถึงง่ายกว่า?",
         "Table Editor: ต้องหาแถว → เลื่อนหา column → คลิก → แก้\nSQL: พิมพ์ชื่อเมนู → กด Run → เสร็จ ใช้เวลาไม่ถึง 10 วินาที!",
         50,185,1870,170,bg_c=HINT_BG,tc=HINT_FG,bc=HINT_BD)
draw_text(d,"เมนูซ้าย → SQL Editor → New Query → วางโค้ดนี้ → กด Run",
          50,370,size=28,color=MID)
# SQL code block
draw_rect(d,50,420,1870,440,fill=CODE_BG,radius=16)
code_lines=[
    [("-- 🙈 ซ่อนเมนู (เปลี่ยนแค่ชื่อในกรอบเหลือง)",CODE_GR,False)],
    [("UPDATE ",CODE_PR,True),("public.menu",CODE_BL,False)],
    [("SET ",CODE_PR,True),("is_available = ",CODE_BL,False),("false",CODE_GN,True)],
    [("WHERE ",CODE_PR,True),("name ",CODE_BL,False),("ILIKE ",CODE_PR,True),
     ("'%",CODE_GN,False),("ชุดไส้",CODE_YL,True),("%';",CODE_GN,False)],
    [("",CODE_GR,False)],
    [("-- 👁️ เปิดกลับมา — เปลี่ยน false เป็น true เท่านั้น",CODE_GR,False)],
    [("UPDATE ",CODE_PR,True),("public.menu  ",CODE_BL,False),("SET ",CODE_PR,True),
     ("is_available = ",CODE_BL,False),("true  ",CODE_GN,True),
     ("WHERE name ILIKE ",CODE_PR,False),("'%",CODE_GN,False),("ชุดไส้",CODE_YL,True),("%';",CODE_GN,False)],
]
cy=440
for parts in code_lines:
    cx=80
    for t,c,b in parts:
        f=font(26,b); bb=d.textbbox((cx,cy+18),t,font=f)
        d.text((cx,cy+18),t,font=f,fill=c)
        cx += bb[2]-bb[0]
    cy += 50 if parts[0][0] else 24

draw_tip(d,"✏️  เปลี่ยนแค่คำสีเหลือง  'ชุดไส้'  = ชื่อ (หรือส่วนของชื่อ) เมนูที่ต้องการซ่อน",
         "เช่น ซ่อน 'ขาหมูพะโล้เตาถ่าน' → พิมพ์  ขาหมู   ILIKE ค้นหาชื่อที่มีคำนั้น ไม่สน ตัวเล็ก/ใหญ่",
         50,880,1870,120,bg_c=HINT_BG,tc=HINT_FG,bc=HINT_BD)
slides_paths.append(save_slide(img,12))

# SLIDE 13 — Edit price
img, d = new_img(WHITE)
draw_header(d,"แก้ราคา","แก้ราคาเมนูด้วยตัวเอง")
steps13=[("1","Supabase → Table Editor → ตาราง menu","เห็นรายการเมนูทั้งหมด พร้อมราคาปัจจุบัน"),
         ("2","หาเมนูที่ต้องการ → ดับเบิลคลิกเซลล์ price","เซลล์เข้าโหมดแก้ไข เห็น cursor กะพริบ"),
         ("3","พิมพ์ราคาใหม่ → กด Enter","แอปลูกค้าอัปเดตภายใน 1–2 วินาที ไม่ต้อง deploy ใหม่")]
for i,(n,t,b) in enumerate(steps13):
    draw_step(d,n,t,b,50,185+i*210)
db_row(d,830,52,DB_BG,[("⚡ Supabase ",DB_GRN,24,True),("  ›  Table Editor › menu",DB_MUT,22,False)])
db_row(d,882,40,DB_MID,[("id      ",DB_MUT,20,True),("name                                  ",DB_MUT,20,True),
    ("price        ",DB_MUT,20,True),("is_available",DB_MUT,20,True)])
rows13=[("1 ","ขาหมูพะโล้เตาถ่าน              ","200|  ",True),
        ("4 ","ข้าวขาหมูพะโล้เตาถ่าน           ","60    ",False)]
for ri,(id_,nm,pr,hl) in enumerate(rows13):
    ry=922+ri*80
    rbg=(13,33,22) if hl else DB_BG
    draw_rect(d,50,ry,1870,76,fill=rbg,radius=0)
    if hl: draw_rect(d,50,ry,1870,76,fill=None,outline=DB_GRN,radius=0)
    x=70
    for t,c,bl in [(id_,DB_TXT,False),(nm,DB_TXT,False),(pr,CODE_YL if hl else DB_TXT,hl),("✓ true",DB_GRN,True)]:
        draw_text(d,t,x,ry+18,size=24,bold=bl,color=c)
        x += len(t)*14+30 if len(t) < 8 else 480
draw_text(d,"☝️  คลิกเซลล์ price → พิมพ์ราคาใหม่ → Enter เสร็จ อัปเดตทันที",
          50,1050,size=28,bold=True,color=RED)
slides_paths.append(save_slide(img,13))

# SLIDE 14 — Paused
img, d = new_img(WHITE)
draw_header(d,"แก้ปัญหา","Supabase ขึ้น 'Paused' — ทำอย่างไร?")
draw_tip(d,"⚠️  Paused เกิดจากอะไร?",
         "Supabase แบบฟรีจะหยุดทำงานอัตโนมัติถ้าไม่ได้ใช้งานนาน 7 วัน\nเมนูลูกค้ายังดูได้ แต่การแก้ราคาจะยังไม่มีผล จนกว่าจะ Resume",
         50,185,1870,180,bg_c=WARN_BG,tc=WARN_FG,bc=WARN_BD)
steps14=[("1","เข้า supabase.com → Sign in → คลิกโปรเจกต์","จะเห็นสถานะ 'Paused' หรือ 'Unhealthy'"),
         ("2","กดปุ่มสีเขียว 'Resume project'","โปรเจกต์จะเริ่มต้นใหม่ ใช้เวลา 1–2 นาที"),
         ("3","รอ 2 นาที → กด Refresh หน้าแอปเมนู","ทุกอย่างกลับมาปกติ ราคาอัปเดตได้ตามเดิม")]
for i,(n,t,b) in enumerate(steps14):
    draw_step(d,n,t,b,50,400+i*192)
draw_tip(d,"💡 ป้องกัน Paused — เข้า Supabase สัปดาห์ละครั้ง",
         "แค่เปิดหน้า Table Editor ก็นับว่า active แล้ว ไม่ต้องทำอะไรเพิ่ม",
         50,970,1870,80,bg_c=HINT_BG,tc=HINT_FG,bc=HINT_BD)
slides_paths.append(save_slide(img,14))

# SLIDE 15 — End
img, d = new_img(SAGE)
draw_text(d,"🎥",W//2,80,size=100,color=WHITE,align="center")
draw_text(d,"จบสไลด์แล้ว!",W//2,240,size=90,bold=True,color=WHITE,align="center")
draw_text(d,"ดูครบแล้ว ถ้ามีคำถามอะไรเพิ่ม ทักเราทาง LINE ได้เลยครับ",
          W//2,380,size=34,color=WHITE,align="center")
draw_rect(d,W//2-600,470,1200,500,fill=WHITE,radius=20)
cy2=500
for ln,b in [("📅 อย่าลืมนัด Zoom สอนงานจริง 30 นาที",True),
             ("✓  ทดลองซ่อนเมนูพร้อมกัน live",False),
             ("✓  ทดลองแก้ราคาใน Supabase",False),
             ("✓  ดูออเดอร์เข้า LINE OA จริง",False),
             ("✓  ตอบคำถามที่ค้างอยู่ทุกข้อ",False)]:
    cy2=draw_text(d,ln,W//2,cy2,size=30,bold=b,color=DARK,align="center")+4
slides_paths.append(save_slide(img,15))

print(f"Generated {len(slides_paths)} slide images")

# ── Narration ────────────────────────────────────────────────────────────────
NARRATION = [
    "สวัสดีครับ วันนี้เราจะสอนการใช้งานระบบเมนู QR Code แพ็ก Premium "
    "ครอบคลุมตั้งแต่ขั้นตอนการสั่งอาหาร Delivery และเรื่องสำคัญที่สุด คือการซ่อนเมนูเมื่อวัตถุดิบหมด ครับ",

    "แพ็ก Premium มีฟีเจอร์หลัก 6 อย่างครับ ออเดอร์เข้า LINE OA อัตโนมัติ "
    "รองรับ Delivery ส่งถึงบ้าน มี 2 ภาษาทั้งไทยและอังกฤษ ตัวเลือกเมนูครบ "
    "แก้ราคาได้เองผ่าน Supabase และซ่อนหรือแสดงเมนูได้ 1 คลิก ครับ",

    "เริ่มจากการทานที่ร้านก่อนครับ "
    "ลูกค้าสแกน QR Code ที่โต๊ะ ไม่ต้องโหลดแอป จากนั้นเลือกโต๊ะ เลือกเมนูพร้อมตัวเลือก "
    "กดยืนยัน เลือกวิธีชำระ แล้วออเดอร์จะเข้า LINE ร้านทันทีครับ",

    "นี่คือตัวอย่างออเดอร์จริงที่เข้ามาใน LINE OA ของร้านครับ "
    "จะเห็นว่าข้อมูลครบทุกอย่าง ทั้งหมายเลขโต๊ะ รายการอาหาร ตัวเลือก จำนวน ยอดรวม และวิธีชำระ "
    "ร้านรับออเดอร์แล้วเริ่มทำได้เลยครับ",

    "สำหรับ Delivery ครับ ลูกค้ากดปุ่มส่งถึงบ้านที่หน้าแรก เลือกเมนู กรอกข้อมูลจัดส่ง "
    "ชำระผ่าน PromptPay ส่งสลิปมาทาง LINE "
    "ร้านได้รับออเดอร์พร้อมที่อยู่และสลิปครบในทีเดียว ครับ",

    "ทีนี้มาถึงเรื่องสำคัญที่สุดในวันนี้ครับ "
    "นั่นก็คือการซ่อนและแสดงเมนูชั่วคราว ทำได้เองใน 3 คลิก โดยไม่ต้องลบออกถาวร ครับ",

    "เราจะใช้ซ่อนเมนูเมื่อไร? มี 3 กรณีหลักครับ "
    "หนึ่ง วัตถุดิบหมดวันนั้น สอง ปิดเมนูชั่วคราว และสาม อยู่ระหว่างปรับราคา "
    "สิ่งสำคัญคือ ซ่อนไม่เท่ากับลบ ข้อมูลยังอยู่ครบ เปิดได้ตลอดเวลาครับ",

    "วิธีเข้า Supabase ครับ เปิดเบราว์เซอร์ไปที่ supabase.com แล้วกด Sign in "
    "กรอก email และ password ที่เราส่งให้ทาง LINE "
    "จากนั้นคลิกชื่อโปรเจกต์ร้าน แล้วไปที่ Table Editor แล้วคลิกตาราง menu ครับ "
    "เคล็ดลับคือ Bookmark หน้า Table Editor ไว้เลย ครั้งต่อไปเข้าได้ทันที",

    "เมื่อเข้ามาแล้วจะเห็นตารางแบบนี้ครับ "
    "คอลัมน์ที่สำคัญที่สุดคือ is_available ด้านขวาสุด "
    "true หมายความว่าเมนูนั้นแสดงในแอปลูกค้า false คือซ่อน แต่ข้อมูลยังอยู่ในระบบครับ",

    "วิธีซ่อนเมนูครับ ให้ดับเบิลคลิกที่เซลล์ is_available ของเมนูที่ต้องการซ่อน "
    "เซลล์จะเข้าโหมดแก้ไข จากนั้นลบค่าเดิม พิมพ์ false ตัวพิมพ์เล็กทั้งหมด แล้วกด Enter "
    "เมนูจะหายจากแอปลูกค้าทันทีเลยครับ",

    "ดูผลลัพธ์ก่อนและหลังซ่อนครับ ก่อนซ่อนลูกค้าเห็นชุดไส้พะโล้ "
    "หลังซ่อนรายการนั้นหายออกจากเมนู "
    "ถ้าอยากเปิดกลับมา ก็แค่เปลี่ยน false กลับเป็น true แล้วกด Enter ครับ",

    "มีวิธีที่เร็วกว่า Table Editor ครับ คือการใช้ SQL Editor "
    "แค่วางโค้ดที่เราเตรียมไว้ เปลี่ยนแค่ชื่อเมนูในกรอบเหลือง แล้วกด Run "
    "เสร็จใน 10 วินาที เร็วกว่าการหาแถวใน Table Editor มากครับ",

    "การแก้ราคาก็ทำได้เองเช่นกันครับ ไปที่ Table Editor ตาราง menu "
    "ดับเบิลคลิกเซลล์ price พิมพ์ราคาใหม่ กด Enter "
    "แอปลูกค้าอัปเดตภายใน 1 ถึง 2 วินาที ไม่ต้อง deploy ใหม่ ไม่ต้องแจ้งเราครับ",

    "ถ้า Supabase ขึ้นว่า Paused ไม่ต้องตกใจครับ "
    "เกิดจากไม่ได้ใช้งาน 7 วัน ให้กดปุ่ม Resume project สีเขียว รอ 2 นาที แล้ว Refresh "
    "วิธีป้องกันคือเข้าหน้า Supabase สัปดาห์ละครั้งก็พอครับ",

    "เท่านี้ก็จบการสอนแพ็ก Premium แล้วครับ "
    "ถ้ามีคำถามอะไร ทักมาทาง LINE ได้เลย "
    "และอย่าลืมนัด Zoom สอนงานจริง 30 นาที เพื่อทดลองซ่อนเมนูและแก้ราคาพร้อมกัน ขอบคุณมากครับ",
]

print("Generating Thai audio narration (espeak-ng)...")
audio_files = []
for i, text in enumerate(NARRATION):
    wav = f"/tmp/audio_{i:02d}.wav"
    subprocess.run(
        ["espeak-ng", "-v", "th", "-s", "155", "-p", "52", "-w", wav, text],
        check=True, capture_output=True
    )
    audio_files.append(wav)
    print(f"  Audio {i+1}/{len(NARRATION)} done")

print("Assembling video...")
clips = []
for i, (png, aud) in enumerate(zip(slides_paths, audio_files)):
    audio = AudioFileClip(aud)
    dur = audio.duration + 0.6
    clip = ImageClip(png).with_duration(dur).with_audio(audio)
    clips.append(clip)

final = concatenate_videoclips(clips, method="compose")
final.write_videofile(str(OUT), fps=24, codec="libx264",
                      audio_codec="aac", logger=None)
final.close()
print(f"\nVideo saved: {OUT}")
print(f"Duration: {final.duration:.1f}s ({final.duration/60:.1f} min)")
