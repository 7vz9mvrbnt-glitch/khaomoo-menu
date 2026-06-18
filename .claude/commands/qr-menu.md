# สกิล: จัดการเมนู QR Code LINE

คุณเป็นผู้ช่วยจัดการระบบเมนู QR Code สั่งอาหารผ่าน LINE OA
ระบบนี้ใช้ React + Vite + Supabase และ deploy บน Vercel/Netlify

## โครงสร้างไฟล์หลัก

| ไฟล์ | หน้าที่ |
|------|--------|
| `src/menuData.js` | ข้อมูลเมนูทั้งหมด (ชื่อ, ราคา, หมวด, ตัวเลือก) |
| `src/supabase.js` | Supabase client |
| `src/App.jsx` | แอปหลัก (UI + logic) |
| `supabase/seed.sql` | SQL สำหรับสร้างตารางและใส่เมนูใน Supabase |
| `.env` | VITE_SUPABASE_URL และ VITE_SUPABASE_ANON_KEY |

## คำสั่งที่รองรับ

เมื่อผู้ใช้บอกงานที่ต้องการ ให้ดูตามนี้:

### แก้ราคาเมนู
1. เปิด `src/menuData.js`
2. ค้นหาชื่อเมนูด้วย grep
3. แก้ค่า `price:` เป็นราคาใหม่
4. รัน `npm run build` ตรวจสอบ
5. commit + push

### เพิ่มเมนูใหม่
1. เปิด `src/menuData.js`
2. เพิ่ม object ใหม่ในอาร์เรย์ MENU ตามรูปแบบ:
```js
{
  id: <เลขไม่ซ้ำ>,
  cat: "<หมวดหมู่>",        // "ขาหมู" | "ข้าวขาหมู" | "เครื่องเคียง" | "กาแฟ Premium" | "เครื่องดื่ม"
  name: "<ชื่อเมนู>",
  price: <ราคา>,
  img: "<img_key>",         // key รูปภาพใน IMGS object ใน App.jsx
  badge: "<ป้าย>" | null,   // "Best Seller" | "Signature" | "ขายดี" | null
  desc: "<คำอธิบาย>",
  opts: [                   // ตัวเลือกเสริม — ถ้าไม่มีใส่ []
    { id: "<id>", label: "<ชื่อ>", price: <บวกเพิ่ม>, group: "<กลุ่ม>" }
    // group: "size" | "type" | "add" | "style" | "sweet" | "temp"
  ]
}
```
3. ถ้ามีรูปใหม่ → เพิ่ม base64 ใน IMGS object ใน `src/App.jsx`
4. อัปเดต `supabase/seed.sql` ให้รัน upsert ใหม่
5. รัน `npm run build` → commit + push

### เพิ่มหมวดหมู่ใหม่
1. เพิ่มชื่อหมวดใน `CATS` array ใน `src/menuData.js`
2. เพิ่มเมนูในหมวดนั้นใน `MENU` array
3. รัน `npm run build` → commit + push

### เพิ่มตัวเลือก (opts) ให้เมนู
ใน `src/menuData.js` หา opts ของเมนูนั้น แล้วเพิ่ม:
```js
{ id: "<unique_id>", label: "<ชื่อที่แสดง>", price: <บวกเพิ่ม>, group: "add" }
```

### อัปเดต Supabase
หลังแก้ `src/menuData.js` ให้ regenerate SQL:
```bash
node --input-type=module <<'EOF'
import { MENU } from '/home/user/khaomoo-menu/src/menuData.js';
import { writeFileSync } from 'fs';
// ... generate SQL และบันทึกลง supabase/seed.sql
EOF
```
แล้วบอกผู้ใช้ให้รัน `supabase/seed.sql` ใน Supabase Dashboard → SQL Editor

### ตั้งค่า Supabase (ครั้งแรก)
1. ตรวจสอบ `.env` มี VITE_SUPABASE_URL และ VITE_SUPABASE_ANON_KEY
2. รัน `supabase/seed.sql` ใน Supabase Dashboard → SQL Editor
3. ตาราง `menu` จะมีคอลัมน์: id, cat, name, price, img, badge, description, opts, is_available

### ซ่อน/แสดงเมนู (โดยไม่ต้อง deploy)
ใน Supabase Dashboard → Table Editor → ตาราง `menu`:
- ซ่อน: เปลี่ยน `is_available` = `false`
- แสดง: เปลี่ยน `is_available` = `true`

## ขั้นตอน deploy

```bash
npm run build          # ตรวจสอบไม่มี error
git add -p             # เลือก stage เฉพาะไฟล์ที่เปลี่ยน
git commit -m "..."
git push
```

## หมายเหตุสำคัญ

- **Fallback**: ถ้า Supabase ไม่ตอบสนอง แอปจะใช้ข้อมูลจาก `menuData.js` อัตโนมัติ
- **รูปภาพ**: ปัจจุบันเก็บเป็น base64 ใน App.jsx → ทำให้ bundle ใหญ่ (~1MB) — ในอนาคตควรย้ายไป Supabase Storage
- **LINE OA**: ตัวแปร LINE_OA และ LINE_OA_ID อยู่ใน App.jsx บรรทัดที่ประมาณ 44-45
- **Branch หลัก**: `claude/qr-line-food-menu-pricing-7e9r69`
