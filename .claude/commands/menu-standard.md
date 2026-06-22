# สกิล: แพ็ก 2 — Standard 2 ภาษา + แก้ราคาเองได้ (แนะนำ)

**ราคา: 2,500 บาท | ระยะเวลา: 4 วัน | แก้ไขฟรี: 3 ครั้ง**

สิ่งที่ลูกค้าได้รับ:
- เมนูสูงสุด 60 รายการ แยกหมวด + ใส่รูปอาหาร
- 2 ภาษา ไทย/อังกฤษ (ปุ่มสลับมุมขวาบน)
- ปรับสี/โลโก้ตามแบรนด์
- เจ้าของแก้ราคา/เมนูเองได้ผ่าน Supabase Dashboard (ไม่ต้องรู้โค้ด)
- QR Code + ไฟล์พร้อมพิมพ์ (PDF/PNG)
- แก้ไขฟรี 3 ครั้ง

**ไม่รวม:** LINE OA / ตัวเลือกเมนู (ขนาด/หวาน/ท็อปปิ้ง) → อยู่ในแพ็ก 3

---

## ขั้นตอนที่ 1 — รับข้อมูลจากลูกค้า

```
□ ชื่อร้าน (ไทย + อังกฤษ)
□ เมนูสูงสุด 60 รายการ (ชื่อไทย + ชื่ออังกฤษ + ราคา + หมวดหมู่)
□ รูปอาหารแต่ละเมนู (JPG/PNG)
□ โลโก้ร้าน (PNG พื้นหลังใส)
□ สีหลัก + สีรอง ของแบรนด์ (hex code)
□ อีเมล Supabase ที่ลูกค้าจะใช้ login แก้เมนูเอง
```

## ขั้นตอนที่ 2 — ตั้งค่าโปรเจกต์

```bash
git clone https://github.com/[repo]/khaomoo-menu my-[ชื่อร้าน]-menu
cd my-[ชื่อร้าน]-menu
npm install
```

## ขั้นตอนที่ 3 — ตั้งค่า Supabase

1. สร้าง Supabase project ใหม่ที่ [supabase.com](https://supabase.com)
2. ไปที่ **Settings → API Keys → Legacy anon, service_role API keys**
   > ⚠️ UI เปลี่ยนแล้ว — ต้องไปที่ "Legacy" ไม่ใช่ "API" ปกติ
3. copy **Project URL** และ **Legacy anon key**
   > ⚠️ **anon key ต้องเป็น JWT format:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (ยาว ~200+ chars)
   > ห้ามใช้ `sb_publishable_xxx` — นั่นคือ key รูปแบบใหม่ที่ยังไม่รองรับ
4. สร้างไฟล์ `.env` (ห้าม commit — ต้องอยู่ใน `.gitignore`):
```env
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
5. สร้าง `.env.example` ไว้เป็นแม่แบบ (commit ได้ — ไม่มี key จริง):
```env
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here
```
6. รัน `supabase/seed.sql` ใน Supabase Dashboard → SQL Editor → Run
7. **แชร์ Supabase project ให้ลูกค้า:** Settings → Team → invite ด้วย email ลูกค้า
8. ถ้า project ขึ้น **"Unhealthy"** → กด Resume แล้วรอ 1-2 นาที (Free tier pause อัตโนมัติ)

## ขั้นตอนที่ 4 — ใส่ข้อมูลเมนู (2 ภาษา)

เปิด `src/menuData.js` แล้วใส่เมนูลูกค้า โครงสร้างต้องมี EN fields ครบ:
```js
{
  id: 1,
  cat: "Rice Dishes",           // หมวด EN (ใช้ใน filter tab เมื่อกด EN)
  cat_en: "Rice Dishes",        // ซ้ำ cat ได้ถ้าเหมือนกัน
  name: "ผัดไทย",
  name_en: "Pad Thai",          // ชื่อเมนู EN
  price: 80,
  img: "padthai",
  badge: null,                   // หรือ "Best Seller" / "New" / "Spicy"
  badge_en: null,                // badge EN (ต้องมีถ้า badge ไม่ null)
  desc: "ผัดไทยสูตรต้นตำรับ",
  desc_en: "Stir-fried rice noodles, classic recipe",
  opts: []                       // Standard ไม่ต้องมี opts
}
```

> **กฎสำคัญ:**
> - ทุกเมนูที่มี `badge` ต้องมี `badge_en` คู่กัน
> - `cat_en` ต้องตรงกับ index ใน `CATS_EN[]` (ดูด้านล่าง)

อัปเดต arrays ที่ด้านบน `menuData.js`:
```js
export const CATS    = ["All", "อาหารหลัก", "ของหวาน", "เครื่องดื่ม"];
export const CATS_EN = ["All", "Main Dish",  "Dessert", "Beverages"];
// index ต้องตรงกันทุกตำแหน่ง
```

## ขั้นตอนที่ 5 — ตรวจสอบ Language Toggle ใน App.jsx

ระบบ lang toggle มีอยู่แล้วในโปรเจกต์:
- ปุ่ม `ไทย | EN` มุมขวาบนหน้าเลือกโต๊ะ (`TableSelectView`)
- `lang` state (`"th"` | `"en"`) ส่งเป็น prop ทุก view
- ถ้า EN field ว่าง → fallback แสดงภาษาไทยอัตโนมัติ

ถ้าโปรเจกต์ยังไม่มี lang toggle ให้เพิ่ม state ใน App:
```js
const [lang, setLang] = useState("th");
// ส่ง lang เป็น prop ให้ทุก component
// ใน MenuView: lang === "en" ? item.name_en : item.name
```

## ขั้นตอนที่ 6 — ปรับแบรนด์

ใน `src/App.jsx` หา `const C = {` แล้วแก้สีตามแบรนด์ลูกค้า:
```js
const C = {
  red:    "<primary color>",    // เช่น "#8B2635"
  cream:  "<background color>", // เช่น "#FAF7F2"
  dark:   "#1A1A1A",
  gold:   "<accent color>",
  border: "<border color>",
  muted:  "<muted color>"
};
```

ใส่โลโก้: แปลงรูปโลโก้เป็น base64 เพิ่มใน `IMGS` object แล้วแสดงใน header

## ขั้นตอนที่ 7 — อัปเดต Supabase ด้วยเมนูลูกค้า

หลังใส่เมนูใน `menuData.js` ครบแล้ว รัน generate SQL ใหม่:
```bash
node --input-type=module -e "
import { MENU } from './src/menuData.js';
const rows = MENU.map(m =>
  \`INSERT INTO menu (id, name, price, category, description, is_available, img_key)
   VALUES (\${m.id}, '\${m.name}', \${m.price}, '\${m.cat}', '\${m.desc ?? ''}', true, '\${m.img}');\`
).join('\n');
console.log(rows);
" > supabase/seed.sql
```
แล้วรัน `seed.sql` ที่ได้ใน Supabase Dashboard → SQL Editor

## ขั้นตอนที่ 8 — Deploy บน Vercel

```bash
npm run build
npx vercel --prod
```

> ⚠️ **สำคัญ:** ต้องตั้ง Environment Variables ใน **Vercel Dashboard → Settings → Environment Variables**:
> - `VITE_SUPABASE_URL`
> - `VITE_SUPABASE_ANON_KEY`
>
> หลังเพิ่ม env vars ต้อง **Redeploy** ด้วย — ไม่งั้นแอป production จะไม่เชื่อม Supabase

สร้าง QR Code จาก URL → ส่งไฟล์ QR (PNG 300dpi) + link ให้ลูกค้า

## ขั้นตอนที่ 9 — ส่งเอกสารสรุปให้ลูกค้า

สร้าง PDF ไฟล์คู่มือ: `python docs/make_pdf.py` (ถ้ามี script นี้ในโปรเจกต์)

ส่งคู่มือแก้เมนูเองนี้ให้ลูกค้า:
```
วิธีแก้ราคา/เพิ่มเมนูเอง (ไม่ต้องรู้โค้ด):
1. เข้า supabase.com → log in
2. เลือกโปรเจกต์ร้านคุณ
3. คลิก Table Editor → ตาราง menu
4. คลิกเซลล์ price → แก้ตัวเลข → Enter
5. เมนูจะอัปเดตในแอปทันที ไม่ต้อง deploy ใหม่
```

---

## Checklist ก่อนส่งงาน

```
□ เมนูครบ ราคาถูกต้อง ทั้ง 2 ภาษา
□ ปุ่มสลับ ไทย/EN ทำงานได้ (มุมขวาบน TableSelectView)
□ กด EN → ชื่อเมนู/หมวด/desc เปลี่ยนเป็นอังกฤษ
□ กด ไทย → กลับมาภาษาไทยครบทุกหน้า
□ สี/โลโก้ตรงแบรนด์ลูกค้า
□ ลูกค้า login Supabase แล้วแก้ราคาเองได้
□ QR Code สแกนได้ ลิงก์ถูกต้อง
□ ทดสอบบนมือถือ (iOS + Android)
□ ส่งคู่มือใช้งานให้ลูกค้าแล้ว
```

---

## หมายเหตุสำคัญ

- **ความปลอดภัย:** `.env` ต้องอยู่ใน `.gitignore` เสมอ — ห้าม commit key จริงขึ้น git
- สร้าง `.env.example` ไว้เป็นแม่แบบ (ใส่แค่ชื่อ key ไม่ใส่ค่าจริง)
- **Supabase anon key** ต้องเป็น JWT: `eyJhbGciOi...` ไม่ใช่ `sb_publishable_xxx`
- **Supabase Free tier:** pause หลังไม่ใช้งาน 1 สัปดาห์ → แนะนำ upgrade Supabase Pro ($25/เดือน) ถ้าใช้งานจริง
- แก้ไขฟรี 3 ครั้ง — ครั้งที่ 4 เป็นต้นไปคิดเพิ่ม
- ถ้าลูกค้าต้องการสั่งอาหารผ่าน LINE → แนะนำ upgrade แพ็ก 3 (Premium)

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

**tip_box() — วัดความสูงก่อนวาด (ป้องกันหน้าว่างเกิน):**
```python
lines = self.multi_cell(inner_w, LH, text, dry_run=True, output='LINES')
n_lines = len(lines)
box_h = n_lines * LH + PAD * 2
self.set_auto_page_break(False)   # ขณะวาดข้อความในกล่อง
self.multi_cell(inner_w, LH, text, align='L')
self.set_auto_page_break(True, margin=20)
```

**fpdf2 v2.8.7 — กล่องมุมโค้ง:**
```python
from fpdf.enums import RenderStyle
self._draw_rounded_rect(x, y, w, h, RenderStyle.DF, round_corners=True, r=4)
# ห้ามใช้ self.rounded_rect() — method นั้นไม่มีใน v2.8.7
```

**Font path:**
```
/tmp/fonts/Sarabun-Regular.ttf
/tmp/fonts/Sarabun-Bold.ttf
```

รันสร้าง PDF: `python docs/make_pdf.py`
