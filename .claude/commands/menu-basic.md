# สกิล: แพ็ก 1 — Basic เมนู QR เริ่มต้น

**ราคา: 990 บาท | ระยะเวลา: 2 วัน | แก้ไขฟรี: 1 ครั้ง**

สิ่งที่ลูกค้าได้รับ:
- เมนูออนไลน์สูงสุด 20 รายการ แยกหมวด + ใส่รูปอาหาร
- QR Code พร้อมใช้งาน (PNG 300dpi)
- ภาษาไทยอย่างเดียว
- แก้ไขฟรี 1 ครั้ง

**ไม่รวม:** Supabase / LINE OA / ตัวเลือกเมนู / 2 ภาษา (อยู่ในแพ็ก 2-3)

---

## ขั้นตอนที่ 1 — รับข้อมูลจากลูกค้า

```
□ ชื่อร้าน
□ รายการเมนูสูงสุด 20 รายการ (ชื่อ + ราคา + หมวดหมู่)
□ รูปอาหารแต่ละเมนู (JPG/PNG — ถ้าไม่มีใช้ emoji หรือ placeholder)
□ โลโก้ร้าน (PNG พื้นหลังใส — ถ้าไม่มีใช้ชื่อร้านแทน)
□ สีหลักของร้าน (ถ้าไม่มีใช้ #8B2635 เป็น default)
```

## ขั้นตอนที่ 2 — ตั้งค่าโปรเจกต์

```bash
git clone https://github.com/[repo]/khaomoo-menu my-[ชื่อร้าน]-menu
cd my-[ชื่อร้าน]-menu
npm install
```

## ขั้นตอนที่ 3 — แก้ข้อมูลเมนูใน menuData.js

เปิด `src/menuData.js` แล้ว:

1. **ลบเมนูตัวอย่างทั้งหมด** แล้วใส่เมนูของลูกค้าแทน (ไม่เกิน 20 รายการ)
2. โครงสร้างแต่ละรายการ (Basic — ไม่ต้องใส่ EN fields):
```js
{
  id: 1,
  cat: "<หมวดหมู่>",
  name: "<ชื่อเมนู>",
  price: <ราคา>,
  img: "<img_key>",
  badge: null,          // หรือ "Best Seller", "New", "Spicy" ฯลฯ
  desc: "<คำอธิบายสั้นๆ>",
  opts: []              // Basic ไม่มีตัวเลือกเสริม
}
```
3. อัปเดต `CATS` array ให้ตรงกับหมวดหมู่ของร้าน:
```js
export const CATS = ["All", "อาหารหลัก", "ของหวาน", "เครื่องดื่ม"];
```

## ขั้นตอนที่ 4 — ใส่รูปอาหาร (base64)

แปลงรูปเป็น base64 แล้วเพิ่มใน `IMGS` object ใน `src/App.jsx`:
```bash
base64 -w 0 รูปภาพ.jpg
```
ใส่ผลลัพธ์ใน:
```js
const IMGS = {
  ชื่อ_key: "data:image/jpeg;base64,<base64 string>",
  // ...
}
```
ให้ `img` ใน menuData.js ตรงกับ key นี้

## ขั้นตอนที่ 5 — ปรับสีแบรนด์

ใน `src/App.jsx` หาบรรทัด `const C = {` แล้วแก้:
```js
const C = {
  red:    "<สีหลักร้าน>",   // เช่น "#8B2635"
  cream:  "#FAF7F2",
  dark:   "#1A1A1A",
  gold:   "#F0B030",
  border: "#EDE8DF",
  muted:  "#B08060"
};
```

## ขั้นตอนที่ 6 — Build และตรวจสอบ

```bash
npm run build
# ต้องไม่มี error — เปิด dist/index.html ทดสอบบน browser
```

## ขั้นตอนที่ 7 — Deploy และส่ง QR Code

**ใช้ Vercel (แนะนำ — ฟรี + deploy อัตโนมัติเมื่อ push)**
```bash
npx vercel --prod
# Vercel จะถามชื่อ project และ directory → กด Enter ตามค่า default
# ได้ URL เช่น https://ชื่อร้าน.vercel.app
```

> ⚠️ **ถ้าแอปใช้ `.env`:** ต้องตั้ง Environment Variables ใน Vercel Dashboard ด้วย
> (Settings → Environment Variables) — ไม่งั้น Supabase/LINE จะใช้งานไม่ได้บน production

หลัง deploy ได้ URL → สร้าง QR Code → ดาวน์โหลดเป็น PNG 300dpi ส่งให้ลูกค้าพิมพ์ติดโต๊ะ

---

## Checklist ก่อนส่งงาน

```
□ เมนูครบ ราคาถูกต้องทุกรายการ
□ รูปอาหารแสดงครบ ไม่มีรูปแตก
□ หมวดหมู่กรองได้ถูกต้อง
□ QR Code สแกนแล้วเปิดเมนูได้
□ ทดสอบบนมือถือ (iOS + Android)
□ ชื่อร้านแสดงถูกต้อง
□ QR Code ส่งไฟล์ PNG 300dpi แล้ว
```

---

## หมายเหตุสำคัญ

- **ความปลอดภัย:** `.env` ต้องอยู่ใน `.gitignore` เสมอ — ห้าม commit key จริงขึ้น git
- สร้าง `.env.example` ไว้เป็นแม่แบบ (ใส่แค่ชื่อ key ไม่ใส่ค่าจริง)
- แก้ไขฟรี 1 ครั้ง — ครั้งที่ 2 เป็นต้นไปคิดเพิ่ม
- ถ้าลูกค้าอยากแก้ราคาเองในอนาคต → แนะนำ upgrade แพ็ก 2 (Standard)
- ถ้าลูกค้าต้องการ LINE OA / ตัวเลือกเมนู → แนะนำ upgrade แพ็ก 3 (Premium)

---

## แก้ปัญหา Thai PDF (วรรณยุกต์/สระ/อักขระทับกัน)

เมื่อต้องสร้าง PDF ภาษาไทยด้วย `docs/make_pdf.py`:

**ปัญหาหลัก:** วรรณยุกต์ ไม้โท สระ ทับตัวอักษรฐาน → แก้ด้วยการเพิ่ม line height

**Line Height ที่ปลอดภัย (fpdf2 + Sarabun font):**
```
body text 12pt  → 8.5mm  (ไม่ใช่ 6.5mm)
desc text 11pt  → 7.5mm  (ไม่ใช่ 6.0mm)
tip box 11pt    → 8.0mm  (ไม่ใช่ 6.5mm)
subtitle 13pt   → 9.0mm  (ไม่ใช่ 7.0mm)
```

**tip_box() — วัดความสูงก่อนวาด (ป้องกันหน้าว่าง):**
```python
lines = self.multi_cell(inner_w, LH, text, dry_run=True, output='LINES')
n_lines = len(lines)
box_h = n_lines * LH + PAD * 2
self.set_auto_page_break(False)   # ขณะวาดข้อความในกล่อง
self.multi_cell(inner_w, LH, text, align='L')
self.set_auto_page_break(True, margin=20)
```

**fpdf2 v2.8.7 — กล่องมุมโค้ง (ใช้ private method):**
```python
from fpdf.enums import RenderStyle
# ถูก:
self._draw_rounded_rect(x, y, w, h, RenderStyle.DF, round_corners=True, r=4)
# ผิด (method นี้ไม่มีใน v2.8.7):
# self.rounded_rect(...)
```

**Font path:**
```
/tmp/fonts/Sarabun-Regular.ttf
/tmp/fonts/Sarabun-Bold.ttf
```

รันสร้าง PDF: `python docs/make_pdf.py`
