# สกิล: แพ็ก 3 — Premium สั่งผ่าน LINE + ขึ้นเว็บให้

**ราคา: 5,900 บาท | ระยะเวลา: 7 วัน | แก้ไขฟรี: 5 ครั้ง**

สิ่งที่ลูกค้าได้รับ:
- เมนูไม่จำกัด + ตัวเลือกเมนู (ขนาด/หวาน/ท็อปปิ้ง)
- ปุ่มสั่งผ่าน LINE OA (ออเดอร์เข้าอัตโนมัติ)
- 2 ภาษา ไทย/อังกฤษ + ดีไซน์เฉพาะแบรนด์
- รองรับ Dine-In และ Delivery
- ขึ้นเว็บ/ลิงก์พร้อมใช้ (deploy ให้)
- สอนใช้งานผ่าน Zoom 30 นาที
- แก้ไขฟรี 5 ครั้ง

---

## ขั้นตอนที่ 1 — รับข้อมูลจากลูกค้า

```
□ ชื่อร้าน (ไทย + อังกฤษ)
□ เมนูทั้งหมด (ชื่อไทย/อังกฤษ + ราคา + หมวด + ตัวเลือก เช่น ขนาด S/M/L)
□ รูปอาหารทุกรายการ (JPG/PNG)
□ โลโก้ร้าน (PNG พื้นหลังใส)
□ สีหลัก + สีรองของแบรนด์ (hex code)
□ LINE OA Channel Access Token (จาก LINE Developer Console → Messaging API → Issue token)
□ LINE OA Channel Secret
□ LINE OA ID (เช่น @shopname)
□ อีเมล Supabase ของลูกค้า
□ Domain ที่ต้องการ (ถ้ามี) หรือใช้ subdomain ฟรีของ Vercel
```

## ขั้นตอนที่ 2 — ตั้งค่าโปรเจกต์

```bash
git clone https://github.com/[repo]/khaomoo-menu my-[ชื่อร้าน]-menu
cd my-[ชื่อร้าน]-menu
npm install
```

## ขั้นตอนที่ 3 — ตั้งค่า LINE OA

สร้าง `.env` (ห้าม commit — ต้องอยู่ใน `.gitignore`):
```env
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
LINE_CHANNEL_ACCESS_TOKEN=xxxx
```

สร้าง `.env.example` ไว้เป็นแม่แบบ (commit ได้ — ไม่มี key จริง):
```env
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here
LINE_CHANNEL_ACCESS_TOKEN=your_line_token_here
```

> **LINE Token:** ขอ **Long-lived token** จาก LINE Developer Console → Messaging API → Issue token
> Long-lived token ไม่หมดอายุ — ไม่ต้อง renew ทุก 30 วัน (ต่างจาก stateless token)

ตรวจสอบ `api/notify.js` — serverless function รับออเดอร์แล้วส่ง push message ไปยัง LINE OA:
```js
// POST /api/notify → รับ { order, tableNum } → ส่ง LINE push message
```

ตรวจสอบใน `src/App.jsx` ว่า LINE_OA และ LINE_OA_ID ถูกต้อง:
```js
const LINE_OA    = "@<ชื่อ LINE OA ลูกค้า>";
const LINE_OA_ID = "%40<ชื่อ LINE OA ลูกค้า>";  // URL-encoded @ = %40
```

## ขั้นตอนที่ 4 — ตั้งค่า Supabase

1. สร้าง Supabase project ใหม่ที่ [supabase.com](https://supabase.com)
2. ไปที่ **Settings → API Keys → Legacy anon, service_role API keys**
   > ⚠️ UI เปลี่ยนแล้ว — ต้องไปที่ "Legacy" section
3. copy **Project URL** และ **Legacy anon key**
   > ⚠️ **anon key ต้องเป็น JWT format:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (ยาว ~200+ chars)
   > ห้ามใช้ `sb_publishable_xxx` — นั่นคือ key รูปแบบใหม่ที่ยังไม่รองรับ
4. ถ้า project ขึ้น **"Unhealthy"** → กด Resume รอ 1-2 นาที
5. รัน `supabase/seed.sql` ใน SQL Editor
6. เพิ่ม **orders table** สำหรับเก็บประวัติออเดอร์:
```sql
CREATE TABLE public.orders (
  id          uuid    DEFAULT gen_random_uuid() PRIMARY KEY,
  table_num   text    NOT NULL,
  items       jsonb   NOT NULL,
  total       integer NOT NULL,
  note        text,
  status      text    NOT NULL DEFAULT 'pending',
  created_at  timestamptz DEFAULT now()
);
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY "allow_insert" ON public.orders FOR INSERT WITH CHECK (true);
CREATE POLICY "allow_read"   ON public.orders FOR SELECT USING (true);
```
7. แชร์ Supabase project ให้ลูกค้า (Settings → Team → invite ด้วย email ลูกค้า)

## ขั้นตอนที่ 5 — ใส่ข้อมูลเมนูพร้อมตัวเลือก 2 ภาษา

ใน `src/menuData.js` ใส่เมนูทั้งหมดพร้อม **EN fields ครบทุก field รวมถึง opts**:
```js
{
  id: 1,
  cat: "Coffee",          cat_en: "Coffee",
  name: "ลาเต้",          name_en: "Latte",
  price: 60,
  img: "latte",
  badge: "Best Seller",   badge_en: "Best Seller",
  desc: "นมหอมละมุน เข้มข้นกำลังดี",
  desc_en: "Smooth creamy milk latte, perfectly balanced",
  opts: [
    { id: "s",    label: "เล็ก (S)",  label_en: "Small (S)",    price: 0,  group: "size" },
    { id: "m",    label: "กลาง (M)", label_en: "Medium (M)",   price: 10, group: "size" },
    { id: "l",    label: "ใหญ่ (L)", label_en: "Large (L)",    price: 20, group: "size" },
    { id: "hot",  label: "ร้อน",      label_en: "Hot",          price: 0,  group: "temp" },
    { id: "cold", label: "เย็น",      label_en: "Iced",         price: 0,  group: "temp" },
    { id: "less", label: "หวานน้อย", label_en: "Less Sweet",   price: 0,  group: "sweet" },
    { id: "none", label: "ไม่หวาน",  label_en: "No Sugar",     price: 0,  group: "sweet" },
  ]
}
```

> **กฎสำคัญ:**
> - ทุก opt ต้องมี `label_en` — ถ้าขาดจะแสดงภาษาไทยเสมอแม้กด EN
> - ทุกเมนูที่มี `badge` ต้องมี `badge_en` คู่กัน
> - `cat_en` ต้องตรงกับ index ใน `CATS_EN[]`

อัปเดต exports ด้านบน `menuData.js`:
```js
export const CATS        = ["All", "ขาหมู", "ข้าว", "เครื่องเคียง"];
export const CATS_EN     = ["All", "Pork Knuckle", "Rice Dishes", "Sides"];
export const GROUP_LABEL = { size: "ขนาด", type: "เนื้อ", add: "เพิ่มเติม",
                              style: "สไตล์", sweet: "ความหวาน", temp: "อุณหภูมิ" };
export const GROUP_LABEL_EN = { size: "Size", type: "Meat Choice", add: "Add-ons",
                                 style: "Coffee Style", sweet: "Sweetness", temp: "Temperature" };
```

## ขั้นตอนที่ 6 — ปรับดีไซน์เฉพาะแบรนด์

1. **สีแบรนด์** — แก้ `const C = {` ใน `src/App.jsx`
2. **โลโก้** — แปลงเป็น base64 ใส่ใน `IMGS` object แล้วแสดงใน header
3. **ฟอนต์** — เปลี่ยน Google Fonts ใน useEffect ที่โหลด font
4. **ชื่อร้านและ UI text** — แปลทั้งไทยและอังกฤษใน HomeView/TableSelectView

ระบบ lang toggle:
- ปุ่ม `ไทย | EN` มุมขวาบน `TableSelectView`
- `lang` state (`"th"` | `"en"`) ส่งเป็น prop ทุก view
- ถ้าไม่มี EN field → fallback แสดงไทยอัตโนมัติ

## ขั้นตอนที่ 7 — ทดสอบ LINE OA บน Staging

1. Deploy staging ก่อน (Vercel Preview URL)
2. ทดสอบสั่งอาหาร → กดยืนยัน → ต้องได้รับข้อความใน LINE OA
3. ตรวจสอบ format ข้อความออเดอร์ถูกต้อง (โต๊ะ/เมนู/ราคา/หมายเหตุ)
4. ทดสอบ Delivery flow ด้วย

## ขั้นตอนที่ 8 — Deploy Production บน Vercel

```bash
npm run build
npx vercel --prod
```

> ⚠️ **สำคัญมาก:** ตั้ง Environment Variables ใน **Vercel Dashboard → Settings → Environment Variables**
> ต้องครบทุกตัว — ไฟล์ `.env` local ไม่ถูกส่งขึ้น Vercel:
> - `VITE_SUPABASE_URL`
> - `VITE_SUPABASE_ANON_KEY`
> - `LINE_CHANNEL_ACCESS_TOKEN`
>
> หลังเพิ่ม env vars แล้วต้อง **Redeploy** ใน Vercel Dashboard ด้วย

**ถ้าลูกค้ามี custom domain:**
```bash
vercel domains add <domain> --prod
```

## ขั้นตอนที่ 9 — สร้าง QR Code

1. ใช้ URL production สร้าง QR Code ความละเอียดสูง
2. ส่งไฟล์ QR (PNG 300dpi) + ลิงก์ให้ลูกค้า
3. แนะนำพิมพ์ติดที่โต๊ะ/เคาน์เตอร์

## ขั้นตอนที่ 10 — นัด Zoom สอนใช้งาน 30 นาที

หัวข้อที่ต้องสอน:
```
□ วิธีแก้ราคา/เพิ่มเมนูใน Supabase Dashboard (Table Editor → menu)
□ วิธีซ่อน/แสดงเมนู (แก้ is_available → false/true)
□ วิธีดูออเดอร์ที่เข้ามาใน LINE OA
□ วิธีดูประวัติออเดอร์ใน Supabase (orders table)
□ วิธีขอแก้ไข (แก้ไขฟรี 5 ครั้ง)
```

---

## Checklist ก่อนส่งงาน

```
□ เมนูครบทุกรายการ ตัวเลือกครบถ้วน
□ LINE OA รับออเดอร์ได้จริง (ทดสอบจริงบนมือถือ)
□ ดีไซน์ตรงแบรนด์ลูกค้า (สี + โลโก้ + ฟอนต์)
□ 2 ภาษา — ตรวจครบทุกหน้าเมื่อกด EN:
  □ หน้าเลือกโต๊ะ (TableSelectView) — ปุ่ม ไทย/EN แสดง
  □ หน้าเมนู — ชื่อ/desc/หมวด/badge เป็น EN
  □ ItemModal — option chips เป็น EN (label_en ครบ), badge เป็น EN, ปุ่ม Add to Cart
  □ ตะกร้า (CartView) — ชื่อเมนู/opts/ยอดรวม เป็น EN
  □ หน้าชำระเงิน (PaymentView) — วิธีชำระ/ยอด เป็น EN
  □ หน้าสถานะ (StatusView) — สถานะ/ปุ่ม เป็น EN
□ กด ไทย → กลับมาภาษาไทยครบทุกหน้า
□ Supabase: ลูกค้าแก้ราคาเองได้ผ่าน Table Editor
□ URL / Domain พร้อมใช้งาน
□ QR Code ส่งแล้ว (PNG 300dpi)
□ นัด Zoom สอนเรียบร้อย
□ ส่งสรุปคู่มือการใช้งานให้ลูกค้า
```

---

## หมายเหตุสำคัญ

- **ความปลอดภัย:** `.env` ต้องอยู่ใน `.gitignore` เสมอ — ห้าม commit key จริงขึ้น git
- สร้าง `.env.example` ไว้เป็นแม่แบบ (ใส่แค่ชื่อ key ไม่ใส่ค่าจริง)
- **LINE Token:** ขอ Long-lived token เท่านั้น — ไม่หมดอายุ ไม่ต้อง renew ทุก 30 วัน
- **Supabase anon key** ต้องเป็น JWT: `eyJhbGciOi...` ไม่ใช่ `sb_publishable_xxx`
- **Vercel** แนะนำมากกว่า Netlify เพราะรองรับ `api/notify.js` (serverless) โดยตรง
- **Supabase Free tier:** pause อัตโนมัติหลัง 1 สัปดาห์ → แนะนำ upgrade Supabase Pro ($25/เดือน) สำหรับร้านที่เปิดทุกวัน
- แก้ไขฟรี 5 ครั้ง — ครั้งที่ 6 เป็นต้นไปคิดเพิ่ม

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
# ตรวจว่าพอดีหน้า — ถ้าเกินให้ add_page ก่อน
if self.get_y() + box_h > 270:
    self.add_page()
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

รันสร้าง PDF ทั้ง 3 แพ็ก: `python docs/make_pdf.py`
