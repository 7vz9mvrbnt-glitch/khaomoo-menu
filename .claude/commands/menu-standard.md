# สกิล: แพ็ก 2 — Standard 2 ภาษา + แก้ราคาเองได้ (แนะนำ)

**ราคา: 2,500 บาท | ระยะเวลา: 4 วัน | แก้ไขฟรี: 3 ครั้ง**

สิ่งที่ลูกค้าได้รับ:
- เมนูสูงสุด 60 รายการ
- 2 ภาษา ไทย/อังกฤษ
- ปรับสี/โลโก้ตามแบรนด์
- เจ้าของแก้ราคา/เมนูเองได้ (ผ่าน Supabase Dashboard)
- QR Code + ไฟล์พร้อมพิมพ์ (PDF/PNG)
- แก้ไขฟรี 3 ครั้ง

---

## ขั้นตอนที่ 1 — รับข้อมูลจากลูกค้า

```
□ ชื่อร้าน (ไทย + อังกฤษ)
□ เมนูสูงสุด 60 รายการ (ชื่อไทย + ชื่ออังกฤษ + ราคา + หมวดหมู่)
□ รูปอาหารแต่ละเมนู
□ โลโก้ร้าน (PNG พื้นหลังใส)
□ สีหลัก + สีรอง ของแบรนด์ (หรือส่ง hex code มา)
□ อีเมล Supabase ที่ลูกค้าจะใช้ล็อกอินแก้เมนูเอง
```

## ขั้นตอนที่ 2 — ตั้งค่าโปรเจกต์

```bash
git clone https://github.com/[repo]/khaomoo-menu my-[ชื่อร้าน]-menu
cd my-[ชื่อร้าน]-menu
npm install
```

## ขั้นตอนที่ 3 — ตั้งค่า Supabase

1. สร้าง Supabase project ใหม่ที่ [supabase.com](https://supabase.com)
2. ไปที่ **Settings → API** → copy URL และ anon key
3. สร้างไฟล์ `.env`:
```env
VITE_SUPABASE_URL=https://xxxx.supabase.co
VITE_SUPABASE_ANON_KEY=sb_publishable_xxxx
```
4. รัน `supabase/seed.sql` ใน Supabase Dashboard → SQL Editor
5. **แชร์ Supabase project** ให้ลูกค้า (Settings → Team) ด้วย email ของลูกค้า

## ขั้นตอนที่ 4 — ใส่ข้อมูลเมนู (2 ภาษา)

เปิด `src/menuData.js` แล้วใส่เมนูลูกค้า โครงสร้าง 2 ภาษา:
```js
{
  id: 1,
  cat: "Main Dish",          // หมวดภาษาอังกฤษ
  cat_th: "อาหารหลัก",       // เพิ่ม field นี้
  name: "Pad Thai",
  name_th: "ผัดไทย",         // เพิ่ม field นี้
  price: 80,
  img: "<img_key>",
  badge: null,
  desc: "Stir-fried rice noodles",
  desc_th: "ผัดไทยสูตรต้นตำรับ",
  opts: []
}
```

> **หมายเหตุ:** ถ้าโปรเจกต์ยังไม่รองรับ 2 ภาษา ให้เพิ่ม logic สลับภาษาใน App.jsx ก่อน (ดูขั้นตอนที่ 5)

## ขั้นตอนที่ 5 — เพิ่ม Language Toggle ใน App.jsx

เพิ่ม state และ toggle ปุ่ม TH/EN:
```js
// ใน App component
const [lang, setLang] = useState("th");

// ส่ง lang เป็น prop ให้ทุก component
// ใน MenuView ใช้: item.lang === "th" ? item.name_th : item.name
```

## ขั้นตอนที่ 6 — ปรับแบรนด์

ใน `src/App.jsx` หา `const C = {` แล้วแก้สีตามแบรนด์ลูกค้า:
```js
const C = {
  red:    "<primary color>",
  cream:  "<background color>",
  dark:   "#1A1A1A",
  gold:   "<accent color>",
  border: "<border color>",
  muted:  "<muted color>"
};
```

ใส่โลโก้: เพิ่มรูปโลโก้ base64 ใน IMGS แล้วแสดงใน header

## ขั้นตอนที่ 7 — อัปเดต Supabase ด้วยเมนูลูกค้า

หลังใส่เมนูใน menuData.js ครบแล้ว รัน generate SQL ใหม่:
```bash
node --input-type=module -e "
import { MENU } from './src/menuData.js';
// generate INSERT statements แล้วบันทึกลง supabase/seed.sql
"
```
แล้วรัน seed.sql ที่ได้ใน Supabase Dashboard

## ขั้นตอนที่ 8 — สร้างไฟล์พร้อมพิมพ์ (PDF/PNG)

```bash
# build แอป
npm run build

# screenshot QR menu เป็น PNG ด้วย puppeteer (optional)
# หรือส่ง URL ให้ลูกค้าพิมพ์ผ่านเบราว์เซอร์ Ctrl+P → Save as PDF
```

## ขั้นตอนที่ 9 — Deploy

```bash
npx vercel --prod   # หรือ Netlify
```

สร้าง QR Code จาก URL → ส่งไฟล์ QR (PNG 300dpi) + link ให้ลูกค้า

## ขั้นตอนที่ 10 — สอนลูกค้าแก้เมนูเอง

ส่งคู่มือนี้ให้ลูกค้า:
```
วิธีแก้ราคา/เพิ่มเมนูเอง (ไม่ต้องรู้โค้ด):
1. เข้า supabase.com → log in
2. เลือกโปรเจกต์ร้านคุณ
3. คลิก Table Editor → ตาราง menu
4. คลิกเซลล์ price → แก้ตัวเลข → Enter
5. เมนูจะอัปเดตในแอปทันที ไม่ต้อง deploy ใหม่
```

## Checklist ก่อนส่งงาน

```
□ เมนูครบ ราคาถูกต้อง ทั้ง 2 ภาษา
□ ปุ่มสลับ TH/EN ทำงานได้
□ สี/โลโก้ตรงแบรนด์ลูกค้า
□ ลูกค้า login Supabase แล้วแก้ราคาเองได้
□ QR Code สแกนได้ ลิงก์ถูกต้อง
□ ไฟล์ PDF/PNG พร้อมพิมพ์
□ ทดสอบบนมือถือ
```

## หมายเหตุ

- แก้ไขฟรี 3 ครั้ง — ครั้งที่ 4 เป็นต้นไปคิดเพิ่ม
- ถ้าลูกค้าต้องการสั่งอาหารผ่าน LINE → แนะนำ upgrade แพ็ก 3 (Premium)
- Supabase Free tier: pause หลังไม่ใช้งาน 1 สัปดาห์ — แนะนำ upgrade Supabase Pro ($25/เดือน) ถ้าใช้งานจริง
