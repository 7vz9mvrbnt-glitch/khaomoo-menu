# สกิล: แพ็ก 3 — Premium สั่งผ่าน LINE + ขึ้นเว็บให้

**ราคา: 5,900 บาท | ระยะเวลา: 7 วัน | แก้ไขฟรี: 5 ครั้ง**

สิ่งที่ลูกค้าได้รับ:
- เมนูไม่จำกัด + ตัวเลือกเมนู (ขนาด/หวาน/ท็อปปิ้ง)
- ปุ่มสั่งผ่าน LINE OA (ออเดอร์เข้าอัตโนมัติ)
- 2 ภาษา + ดีไซน์เฉพาะแบรนด์
- ขึ้นเว็บ/ลิงก์พร้อมใช้ (deploy ให้)
- สอนใช้งานผ่าน Zoom 30 นาที
- แก้ไขฟรี 5 ครั้ง

---

## ขั้นตอนที่ 1 — รับข้อมูลจากลูกค้า

```
□ ชื่อร้าน (ไทย + อังกฤษ)
□ เมนูทั้งหมด (ชื่อไทย/อังกฤษ + ราคา + หมวด + ตัวเลือก เช่น ขนาด S/M/L)
□ รูปอาหารทุกรายการ
□ โลโก้ร้าน (PNG พื้นหลังใส)
□ สีหลัก + สีรองของแบรนด์
□ LINE OA Channel Access Token (ได้จาก LINE Developer Console)
□ LINE OA Channel Secret
□ LINE OA ID (เช่น @shopname)
□ อีเมล Supabase ของลูกค้า
□ Domain ที่ต้องการ (ถ้ามี) หรือใช้ subdomain ฟรีของ Vercel/Netlify
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

สร้าง `.env.example` ไว้เป็นแม่แบบ (commit ได้):
```env
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here
LINE_CHANNEL_ACCESS_TOKEN=your_line_token_here
```

> **หมายเหตุ LINE Token:** ขอ **Long-lived token** จาก LINE Developer Console → Messaging API → Issue token
> (Long-lived token ไม่หมดอายุ ไม่ต้อง renew ทุก 30 วัน)

ตรวจสอบ `api/notify.js` — ไฟล์นี้คือ serverless function ที่รับออเดอร์แล้วส่ง push message ไปยัง LINE OA:
```js
// api/notify.js — ตรวจสอบว่ามี endpoint นี้ครบ:
// POST /api/notify → รับ { order, tableNum } → ส่ง LINE push message
```

ตรวจสอบใน `src/App.jsx` ว่า LINE_OA และ LINE_OA_ID ถูกต้อง:
```js
const LINE_OA = "@<ชื่อ LINE OA ลูกค้า>";
const LINE_OA_ID = "%40<ชื่อ LINE OA ลูกค้า>";
```

## ขั้นตอนที่ 4 — ตั้งค่า Supabase

1. สร้าง Supabase project ใหม่ที่ [supabase.com](https://supabase.com)
2. ไปที่ **Settings → API Keys → Legacy anon key** (ไม่ใช่ Settings → API — UI เปลี่ยนแล้ว)
3. copy URL + anon key (format JWT: `eyJhbGciOi...`) ใส่ใน `.env`
4. ถ้า project ขึ้น **"Unhealthy"** → กด Resume รอ 1-2 นาที
5. รัน `supabase/seed.sql` ใน SQL Editor
3. เพิ่ม **orders table** สำหรับเก็บประวัติออเดอร์:
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
4. แชร์ Supabase project ให้ลูกค้า

## ขั้นตอนที่ 5 — ใส่ข้อมูลเมนูพร้อมตัวเลือก

ใน `src/menuData.js` ใส่เมนูทั้งหมดพร้อม opts:
```js
{
  id: 1,
  cat: "Coffee",
  name: "Latte",
  price: 60,
  img: "latte",
  badge: "Best Seller",
  desc: "นมหอมละมุน เข้มข้นกำลังดี",
  opts: [
    { id: "s",    label: "เล็ก (S)",   price: 0,  group: "size" },
    { id: "m",    label: "กลาง (M)",   price: 10, group: "size" },
    { id: "l",    label: "ใหญ่ (L)",   price: 20, group: "size" },
    { id: "hot",  label: "ร้อน",       price: 0,  group: "temp" },
    { id: "cold", label: "เย็น",       price: 0,  group: "temp" },
    { id: "less", label: "หวานน้อย",  price: 0,  group: "sweet" },
    { id: "none", label: "ไม่หวาน",   price: 0,  group: "sweet" },
  ]
}
```

## ขั้นตอนที่ 6 — ปรับดีไซน์เฉพาะแบรนด์

1. **สีแบรนด์** — แก้ `const C = {` ใน App.jsx
2. **โลโก้** — แปลงเป็น base64 ใส่ใน IMGS แล้วแสดงใน header
3. **ฟอนต์** — เปลี่ยน Google Fonts ใน useEffect ที่โหลด font
4. **ภาพหน้าแรก (HomeView)** — ปรับข้อความต้อนรับ ชื่อร้าน
5. **2 ภาษา** — เพิ่ม `name_th`, `desc_th` และ lang toggle ตามแพ็ก Standard

## ขั้นตอนที่ 7 — ทดสอบ LINE OA

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
> ต้องครบทุกตัว ไม่งั้น LINE และ Supabase จะใช้งานไม่ได้บน production:
> - `VITE_SUPABASE_URL`
> - `VITE_SUPABASE_ANON_KEY`
> - `LINE_CHANNEL_ACCESS_TOKEN`
>
> หลังเพิ่ม env vars แล้วต้อง **Redeploy** ใน Vercel ด้วย

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
□ วิธีแก้ราคา/เพิ่มเมนูใน Supabase Dashboard
□ วิธีซ่อน/แสดงเมนู (is_available)
□ วิธีดูออเดอร์ที่เข้ามาใน LINE OA
□ วิธีดูประวัติออเดอร์ใน Supabase (orders table)
□ วิธีขอแก้ไข (แก้ไขฟรี 5 ครั้ง)
```

## Checklist ก่อนส่งงาน

```
□ เมนูครบทุกรายการ ตัวเลือกครบถ้วน
□ LINE OA รับออเดอร์ได้จริง (ทดสอบจริงบนมือถือ)
□ ดีไซน์ตรงแบรนด์ลูกค้า (สี + โลโก้ + ฟอนต์)
□ 2 ภาษา สลับได้ถูกต้อง
□ Supabase: ลูกค้าแก้เมนูเองได้
□ URL / Domain พร้อมใช้งาน
□ QR Code ส่งแล้ว (PNG 300dpi)
□ นัด Zoom สอนเรียบร้อย
□ ส่งสรุปคู่มือการใช้งานให้ลูกค้า
```

## หมายเหตุ

- **Vercel** แนะนำมากกว่า Netlify เพราะรองรับ `api/notify.js` (serverless) โดยตรง
- **LINE Token:** ขอ Long-lived token — ไม่หมดอายุ ไม่ต้อง renew ทุก 30 วัน
- **ความปลอดภัย:** `.env` ต้องอยู่ใน `.gitignore` เสมอ สร้าง `.env.example` ไว้แทน
- **Vercel env vars:** ต้องตั้งใน Dashboard แยกต่างหาก — ไฟล์ `.env` local ไม่ถูกส่งขึ้น Vercel
- **Supabase Free tier:** pause อัตโนมัติหลัง 1 สัปดาห์ / ขึ้น "Unhealthy" → กด Resume
  แนะนำ upgrade Supabase Pro ($25/เดือน) สำหรับร้านที่เปิดทุกวัน
- แก้ไขฟรี 5 ครั้ง — ครั้งที่ 6 เป็นต้นไปคิดเพิ่ม
