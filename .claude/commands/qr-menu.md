# สกิล: จัดการเมนู QR Code LINE

คุณเป็นผู้ช่วยจัดการระบบเมนู QR Code สั่งอาหารผ่าน LINE OA
ระบบนี้ใช้ React + Vite + Supabase และ deploy บน Vercel

## ข้อมูลโปรเจกต์ปัจจุบัน

| รายการ | ค่า |
|--------|-----|
| **URL จริง** | `https://khaomoo-menu.vercel.app` |
| **Supabase project** | `neeogfqgxogtmstssrjt` |
| **Branch** | `claude/qr-line-food-menu-pricing-7e9r69` |
| **ตาราง Supabase** | `public.menu` (28 รายการ), RLS เปิดอยู่ |

## โครงสร้างไฟล์หลัก

| ไฟล์ | หน้าที่ |
|------|--------|
| `src/menuData.js` | ข้อมูลเมนูทั้งหมด (ชื่อ, ราคา, หมวด, ตัวเลือก) — **แก้ราคาที่นี่** |
| `src/supabase.js` | Supabase client |
| `src/App.jsx` | แอปหลัก (UI + logic) |
| `supabase/seed.sql` | SQL สร้างตาราง + ใส่เมนูทั้งหมด (รัน upsert ซ้ำได้ปลอดภัย) |
| `.env` | key จริง — **ห้าม commit** (อยู่ใน .gitignore แล้ว) |
| `.env.example` | แม่แบบ key — commit ได้ปลอดภัย |

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
2. เพิ่ม object ใหม่ในอาร์เรย์ MENU ตามรูปแบบ **2 ภาษา**:
```js
{
  id: <เลขไม่ซ้ำ>,
  cat: "<หมวดหมู่ไทย>",     // "ขาหมู" | "ข้าวขาหมู" | "เครื่องเคียง" | "กาแฟ Premium" | "เครื่องดื่ม"
  cat_en: "<หมวดอังกฤษ>",   // "Pork Knuckle" | "Rice Dishes" | "Sides" | "Premium Coffee" | "Beverages"
  name: "<ชื่อเมนูไทย>",
  name_en: "<ชื่อเมนูอังกฤษ>",
  price: <ราคา>,
  img: "<img_key>",          // key รูปภาพใน IMGS object ใน App.jsx
  badge: "<ป้าย>" | null,    // "Best Seller" | "Signature" | "ขายดี" | "แชร์ได้" | "สายหนัง" | null
  badge_en: "<ป้ายอังกฤษ>" | null, // "Best Seller" | "Signature" | "Popular" | "Shareable" | "Pork Skin Fan" | null
  desc: "<คำอธิบายไทย>",
  desc_en: "<คำอธิบายอังกฤษ>",
  opts: [                    // ตัวเลือกเสริม — ถ้าไม่มีใส่ []
    { id: "<id>", label: "<ชื่อไทย>", label_en: "<ชื่ออังกฤษ>", price: <บวกเพิ่ม>, group: "<กลุ่ม>" }
    // group: "size" | "type" | "add" | "style" | "sweet" | "temp"
  ]
}
```
3. ถ้ามีรูปใหม่ → เพิ่ม base64 ใน IMGS object ใน `src/App.jsx`
4. อัปเดต `supabase/seed.sql` ให้รัน upsert ซ้ำ
5. รัน `npm run build` → commit + push

### เพิ่มหมวดหมู่ใหม่
1. เพิ่มชื่อหมวดใน `CATS` array และ `CATS_EN` ใน `src/menuData.js` ตำแหน่งเดียวกัน (index ตรงกัน)
2. เพิ่มเมนูในหมวดนั้นใน `MENU` array พร้อม `cat_en`
3. รัน `npm run build` → commit + push

### เพิ่มตัวเลือก (opts) ให้เมนู
ใน `src/menuData.js` หา opts ของเมนูนั้น แล้วเพิ่มพร้อม `label_en`:
```js
{ id: "<unique_id>", label: "<ชื่อไทย>", label_en: "<ชื่ออังกฤษ>", price: <บวกเพิ่ม>, group: "add" }
```

### อัปเดต Supabase หลังแก้เมนู
หลังแก้ `src/menuData.js` ให้ regenerate seed.sql แล้วรันใน Supabase:
```bash
node --input-type=module <<'NODEOF'
import { MENU } from '/home/user/khaomoo-menu/src/menuData.js';
import { writeFileSync } from 'fs';
const esc = s => s ? s.replace(/'/g,"''") : null;
const nul = v => v===null ? 'NULL' : `'${esc(v)}'`;
let sql = `INSERT INTO public.menu (id,cat,name,price,img,badge,description,opts) VALUES\n`;
sql += MENU.map(m=>`(${m.id},'${esc(m.cat)}','${esc(m.name)}',${m.price},'${esc(m.img)}',${nul(m.badge)},'${esc(m.desc)}','${JSON.stringify(m.opts).replace(/'/g,"''")}'::jsonb)`).join(',\n');
sql += `\nON CONFLICT (id) DO UPDATE SET\n  cat=EXCLUDED.cat,name=EXCLUDED.name,price=EXCLUDED.price,\n  img=EXCLUDED.img,badge=EXCLUDED.badge,description=EXCLUDED.description,opts=EXCLUDED.opts;\n`;
writeFileSync('/home/user/khaomoo-menu/supabase/seed.sql', sql);
console.log('seed.sql updated with', MENU.length, 'items');
NODEOF
```
แล้วบอกผู้ใช้ให้รัน `supabase/seed.sql` ใน **Supabase Dashboard → SQL Editor → Run**

### ตั้งค่า Supabase (ครั้งแรกของโปรเจกต์ใหม่)
1. สร้าง Supabase project → ไปที่ **Settings → API Keys → Legacy anon key** (ไม่ใช่ Settings → API)
2. copy URL และ anon key (format: `eyJhbGciOi...` ยาว) ใส่ใน `.env`
3. รัน `supabase/seed.sql` ใน SQL Editor
4. ตาราง `menu`: id, cat, name, price, img, badge, description, opts, is_available

### ซ่อน/แสดงเมนู (โดยไม่ต้อง deploy)
ใน Supabase Dashboard → Table Editor → ตาราง `menu`:
- ซ่อน: เปลี่ยน `is_available` = `false`
- แสดง: เปลี่ยน `is_available` = `true`

---

## คู่มือจัดการเมนูผ่าน Supabase (ไม่ต้องแตะโค้ด)

> การเปลี่ยนแปลงผ่าน Supabase มีผลทันที — แอปดึงข้อมูลใหม่อัตโนมัติ ไม่ต้อง deploy ใหม่

### วิธีที่ 1 — Table Editor (ง่ายที่สุด)

ไปที่: **Supabase Dashboard → Table Editor → ตาราง `menu`**

**แก้ราคา:**
1. คลิกไอคอนดินสอที่แถวเมนูที่ต้องการ → หน้าต่าง "Update row" เปิดขึ้น
2. แก้ตัวเลขในช่อง `price` (int4 = ตัวเลขเต็ม)
3. กด **Save**

**เพิ่มเมนูใหม่:**
1. กดปุ่ม **Insert** (สีเขียว มุมขวาบน)
2. กรอกข้อมูล:

| ช่อง | ความหมาย | ตัวอย่าง |
|------|-----------|---------|
| `id` | เลขไม่ซ้ำ (ปัจจุบัน max = 28) | `29` |
| `cat` | หมวดหมู่ | `ขาหมู` / `ข้าวขาหมู` / `เครื่องเคียง` / `เครื่องดื่ม` / `กาแฟ Premium` |
| `name` | ชื่อเมนู | `ข้าวไส้พะโล้` |
| `price` | ราคาหลัก (บาท) | `80` |
| `img` | key รูปภาพ (ไม่มีนามสกุล) | `rice_guts` |
| `badge` | ป้ายกำกับ (ไม่บังคับ) | `Best Seller` / `ใหม่` / เว้นว่าง |
| `description` | คำอธิบาย | `ไส้พะโล้เตาถ่านหอมเข้ม` |
| `opts` | ตัวเลือกเสริม (JSON) | `[]` ถ้าไม่มี |
| `is_available` | แสดงในเมนู | `TRUE` |

### วิธีที่ 2 — SQL Editor (เร็ว เหมาะแก้หลายรายการ)

**แก้ราคาเมนูเดียว:**
```sql
UPDATE public.menu SET price = 120 WHERE id = 4;
```

**แก้ราคาหลายรายการพร้อมกัน:**
```sql
UPDATE public.menu SET price = 70 WHERE id IN (4, 5);
```

**เพิ่มเมนูใหม่:**
```sql
INSERT INTO public.menu (id, cat, name, price, img, badge, description, opts)
VALUES (
  29, 'เครื่องเคียง', 'เต้าหู้พะโล้', 30, 'tofu_palo',
  NULL, 'เต้าหู้พะโล้เคี่ยวนุ่ม หอมเครื่อง', '[]'
);
```

### รูปแบบ `opts` (ตัวเลือกเสริม)

```json
[
  {"id":"normal",  "label":"ธรรมดา",       "label_en":"Regular",        "price":0,  "group":"size"},
  {"id":"special", "label":"พิเศษ",        "label_en":"Special",        "price":10, "group":"size"},
  {"id":"egg",     "label":"+ ไข่เป็ดต้ม", "label_en":"+ Boiled Duck Egg","price":10,"group":"add"}
]
```

- `group`: `size` (ขนาด) | `type` (ประเภทเนื้อ) | `add` (ของเพิ่ม) | `sweet` (ความหวาน) | `temp` (อุณหภูมิ)
- `price` ในตัวเลือก = ราคาที่บวกเพิ่มจากราคาหลัก (ใส่ `0` ถ้าราคาเท่ากัน)
- `label_en` จำเป็นสำหรับระบบ 2 ภาษา — ถ้าไม่ใส่จะ fallback เป็น `label` ไทยเสมอ

## ระบบ 2 ภาษา (ไทย / EN)

แอปรองรับ 2 ภาษาผ่าน `lang` state (`"th"` | `"en"`) ใน App component

### โครงสร้างข้อมูล 2 ภาษา (ใน menuData.js)

| Field | ไทย | อังกฤษ |
|-------|-----|--------|
| `cat` | หมวดหมู่ | `cat_en` |
| `name` | ชื่อเมนู | `name_en` |
| `desc` | คำอธิบาย | `desc_en` |
| `badge` | ป้าย | `badge_en` |
| opt `label` | ตัวเลือก | opt `label_en` |
| `CATS[]` | อาร์เรย์หมวด | `CATS_EN[]` (index ต้องตรงกัน) |
| `GROUP_LABEL` | ชื่อกลุ่ม opts | `GROUP_LABEL_EN` |
| `UPSELL` | ข้อความ upsell | `UPSELL_EN` |

### Supabase + 2 ภาษา (สำคัญ)

Supabase DB เก็บเฉพาะ `label` ไทยใน `opts` JSON — ไม่มี `label_en`
App จึง merge ข้อมูล opts จาก local `menuData.js` หลัง fetch Supabase:

```js
// ใน useEffect (App.jsx)
const localById = Object.fromEntries(MENU.map(m => [m.id, m]));
setMenuItems(data.map(r => ({
  ...r, desc: r.description,
  name_en:  localById[r.id]?.name_en,
  desc_en:  localById[r.id]?.desc_en,
  cat_en:   localById[r.id]?.cat_en,
  badge_en: localById[r.id]?.badge_en,
  opts: (localById[r.id]?.opts ?? r.opts ?? []).map(localOpt => {
    const dbOpt = (r.opts ?? []).find(o => o.id === localOpt.id);
    return dbOpt ? { ...localOpt, price: dbOpt.price } : localOpt;
  }),
})));
```

กฎ: **EN fields และ opts structure มาจาก local** / **ราคา (price) มาจาก Supabase** เสมอ
→ เจ้าของร้านแก้ราคาใน Supabase Dashboard ได้ปกติ

### LangToggle component

```jsx
function LangToggle({ lang, setLang }) {
  return (
    <div style={{ display:"flex", border:"1px solid #D0CCC4",
                  borderRadius:999, overflow:"hidden", fontSize:13, fontWeight:500 }}>
      {["th","en"].map(l => (
        <button key={l} onClick={() => setLang(l)}
          style={{ padding:"5px 14px", cursor:"pointer", border:"none", fontFamily:"inherit",
                   background: lang===l ? "#1A1A1A" : "#fff",
                   color:      lang===l ? "#fff"     : "#1A1A1A" }}>
          {l === "th" ? "ไทย" : "EN"}
        </button>
      ))}
    </div>
  );
}
```

วางใน `TableSelectView` มุมขวาบน (`position:"absolute", top:20, right:20`)

### เพิ่ม/แก้คำแปล opt labels

ทุกครั้งที่เพิ่ม opt ใหม่ใน menuData.js ต้องใส่ `label_en` คู่กันเสมอ ไม่งั้นจะแสดงเป็นไทยเมื่อกด EN

---

## ขั้นตอน deploy

```bash
npm run build          # ตรวจสอบไม่มี error
git add -p             # เลือก stage เฉพาะไฟล์ที่เปลี่ยน
git commit -m "..."
git push
```

## หมายเหตุสำคัญ

- **Fallback**: ถ้า Supabase ไม่ตอบสนอง แอปจะใช้ข้อมูลจาก `menuData.js` อัตโนมัติ
- **รูปภาพ**: เก็บเป็น base64 ใน App.jsx → bundle ~1MB — ในอนาคตควรย้ายไป Supabase Storage
- **LINE OA**: `LINE_OA` และ `LINE_OA_ID` อยู่ใน App.jsx บรรทัด 45-46
- **LINE Token**: ใช้ Long-lived token (ไม่หมดอายุ) — ตั้งค่าใน LINE Developer Console
- **ความปลอดภัย**: `.env` อยู่ใน `.gitignore` แล้ว — ห้าม commit เด็ดขาด ใช้ `.env.example` เป็นแม่แบบ
- **Vercel env vars**: ต้องตั้งแยกใน Vercel Dashboard (Settings → Environment Variables) แอปถึงจะใช้ key ได้บน production
- **Supabase Free tier**: pause อัตโนมัติหลังไม่ใช้ 1 สัปดาห์ → status จะขึ้น "Unhealthy" → ต้อง Resume ก่อนใช้งาน
