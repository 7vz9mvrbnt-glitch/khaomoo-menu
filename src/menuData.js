// ================================================================
// ไฟล์นี้คือที่เก็บข้อมูลเมนูทั้งหมด
// แก้ไขราคาได้ที่นี่เลย โดยไม่ต้องไปแตะ App.jsx
//
// โครงสร้างแต่ละรายการ:
//   id       : หมายเลขเมนู (ห้ามซ้ำ)
//   cat      : หมวดหมู่  → "ขาหมู" | "ข้าวขาหมู" | "เครื่องเคียง" | "กาแฟ Premium" | "เครื่องดื่ม"
//   name     : ชื่อเมนู
//   price    : ราคาตั้งต้น (บาท)  ← แก้ตรงนี้เพื่อเปลี่ยนราคา
//   img      : key รูปภาพ (อย่าแก้ถ้าไม่ได้เปลี่ยนรูป)
//   badge    : ป้ายกำกับ เช่น "Best Seller" | null = ไม่มีป้าย
//   desc     : คำอธิบายเมนู
//   opts     : ตัวเลือกเสริม (size, type, add-on) — price ในนี้คือราคาที่บวกเพิ่มจากราคาตั้งต้น
// ================================================================

export const MENU = [

  // ── ขาหมู ─────────────────────────────────────────────────────
  {
    id: 1, cat: "ขาหมู", name: "ชุดขาหมูพะโล้", price: 400,
    img: "khaomoo_set", badge: "แชร์ได้",
    desc: "ขาหมูพะโล้สูตรร้าน เนื้อนุ่ม หนังฉ่ำ เสิร์ฟพร้อมน้ำจิ้มและผักกาดดอง",
    opts: [
      { id: "khamoo",  label: "ชุดขาหมู (1 ขา)", price: 0,  group: "type" },
      { id: "kaki",    label: "ชุดคากิ",          price: 0,  group: "type" },
      { id: "egg",     label: "+ ไข่เป็ดต้ม",     price: 10, group: "add"  },
      { id: "mantou",  label: "+ หมั่นโถว",       price: 10, group: "add"  },
      { id: "pickle",  label: "+ ผักกาดดอง",      price: 20, group: "add"  },
    ],
  },

  {
    id: 2, cat: "ขาหมู", name: "ชุดขาหมูพะโล้สับ", price: 100,
    img: "khaomoo_chop", badge: "Best Seller",
    desc: "ขาหมูสับพร้อมเสิร์ฟ เลือกขนาดและเนื้อตามชอบ",
    opts: [
      { id: "size100",    label: "ชุด 100 บาท",   price: 0,  group: "size" },
      { id: "size150",    label: "ชุด 150 บาท",   price: 50, group: "size" },
      { id: "skin",       label: "เนื้อหนัง",     price: 0,  group: "type" },
      { id: "meat_only",  label: "เนื้อล้วน",     price: 0,  group: "type" },
      { id: "kaki",       label: "ขาหมูคากิ",     price: 0,  group: "type" },
      { id: "guts",       label: "ขาหมูไส้",      price: 0,  group: "type" },
      { id: "kaki_guts",  label: "ขาหมูคากิไส้", price: 0,  group: "type" },
      { id: "skin_heavy", label: "เน้นหนัง",      price: 0,  group: "type" },
      { id: "egg",        label: "+ ไข่เป็ดต้ม",  price: 10, group: "add"  },
    ],
  },

  {
    id: 3, cat: "ขาหมู", name: "ชุดคากิพะโล้สับ", price: 100,
    img: "kaki_chop", badge: "สายหนัง",
    desc: "คากินุ่มหนึบ เคี่ยวจนเข้าเนื้อ หอมเครื่องพะโล้",
    opts: [
      { id: "size100",      label: "ชุด 100 บาท",   price: 0,  group: "size" },
      { id: "size150",      label: "ชุด 150 บาท",   price: 50, group: "size" },
      { id: "kaki_only",    label: "คากิล้วน",      price: 0,  group: "type" },
      { id: "km_kaki",      label: "ขาหมูคากิ",     price: 0,  group: "type" },
      { id: "kaki_guts",    label: "คากิไส้",       price: 0,  group: "type" },
      { id: "km_kaki_guts", label: "ขาหมูคากิไส้", price: 0,  group: "type" },
      { id: "egg",          label: "+ ไข่เป็ดต้ม",  price: 10, group: "add"  },
    ],
  },

  {
    id: 26, cat: "ขาหมู", name: "ชุดไส้พะโล้เตาถ่าน", price: 100,
    img: "guts_palo", badge: null,
    desc: "ไส้พะโล้เตาถ่านเคี่ยวจนเข้าเนื้อ หอมเครื่อง นุ่มหนึบ สูตรต้นตำรับ",
    opts: [
      { id: "size100",      label: "ชุด 100 บาท",   price: 0,  group: "size" },
      { id: "size150",      label: "ชุด 150 บาท",   price: 50, group: "size" },
      { id: "guts_only",    label: "ไส้ล้วน",       price: 0,  group: "type" },
      { id: "km_guts",      label: "ขาหมูไส้",      price: 0,  group: "type" },
      { id: "kaki_guts",    label: "คากิไส้",       price: 0,  group: "type" },
      { id: "km_kaki_guts", label: "ขาหมูคากิไส้", price: 0,  group: "type" },
      { id: "egg",          label: "+ ไข่เป็ดต้ม",  price: 10, group: "add"  },
    ],
  },

  // ── ข้าวขาหมู ─────────────────────────────────────────────────
  {
    id: 4, cat: "ข้าวขาหมู", name: "ข้าวขาหมูพะโล้เตาถ่าน", price: 60,
    img: "rice_khaomoo", badge: "Best Seller",
    desc: "ข้าวขาหมูสูตรเตาถ่าน เสิร์ฟพร้อมน้ำจิ้มและผักกาดดอง",
    opts: [
      { id: "normal",    label: "ธรรมดา",         price: 0,  group: "size" },
      { id: "special",   label: "พิเศษ",          price: 10, group: "size" },
      { id: "jumbo",     label: "จัมโบ้",          price: 20, group: "size" },
      { id: "meat_only", label: "เนื้อล้วน",      price: 0,  group: "type" },
      { id: "skin",      label: "เนื้อหนัง",      price: 0,  group: "type" },
      { id: "kaki",      label: "ขาหมู + คากิ",   price: 0,  group: "type" },
      { id: "guts",      label: "ขาหมู + ไส้",    price: 0,  group: "type" },
      { id: "kaki_guts", label: "ขาหมู คากิ ไส้", price: 0,  group: "type" },
      { id: "skin_heavy",label: "เน้นหนัง",       price: 0,  group: "type" },
      { id: "egg",       label: "+ ไข่เป็ดต้ม",   price: 10, group: "add"  },
      { id: "mantou",    label: "+ หมั่นโถว",     price: 10, group: "add"  },
    ],
  },

  {
    id: 5, cat: "ข้าวขาหมู", name: "ข้าวคากิพะโล้เตาถ่าน", price: 60,
    img: "rice_kaki", badge: "ขายดี",
    desc: "คากินุ่มละลายในปาก เสิร์ฟพร้อมข้าวหอมร้อนๆ",
    opts: [
      { id: "normal",    label: "ธรรมดา",        price: 0,  group: "size" },
      { id: "special",   label: "พิเศษ",         price: 10, group: "size" },
      { id: "jumbo",     label: "จัมโบ้",         price: 20, group: "size" },
      { id: "kaki_only", label: "คากิล้วน",      price: 0,  group: "type" },
      { id: "kaki_km",   label: "ขาหมู + คากิ",  price: 0,  group: "type" },
      { id: "kaki_guts", label: "คากิ + ไส้",    price: 0,  group: "type" },
      { id: "all3",      label: "ขาหมู คากิ ไส้", price: 0,  group: "type" },
      { id: "egg",       label: "+ ไข่เป็ดต้ม",  price: 10, group: "add"  },
      { id: "mantou",    label: "+ หมั่นโถว",    price: 10, group: "add"  },
    ],
  },

  // ── เครื่องเคียง ──────────────────────────────────────────────
  { id: 6,  cat: "เครื่องเคียง", name: "ข้าวเปล่า",        price: 10, img: "rice_plain",     badge: null,          desc: "ข้าวสวยร้อนๆ หอมนุ่ม",                         opts: [] },
  { id: 7,  cat: "เครื่องเคียง", name: "หมั่นโถว (1 ลูก)", price: 10, img: "mantou_new",     badge: "Best Seller",  desc: "หมั่นโถวนึ่งเนื้อนุ่ม ทานคู่พะโล้",             opts: [] },
  { id: 19, cat: "เครื่องเคียง", name: "ผักกาดดอง",         price: 20, img: "pickle_cab",     badge: null,          desc: "ผักกาดดองรสเปรี้ยวหวาน ทานคู่ขาหมูลงตัว",       opts: [] },
  { id: 20, cat: "เครื่องเคียง", name: "ไชเท้า",            price: 20, img: "daikon",         badge: null,          desc: "ไชเท้าดองกรอบหวาน เคียงขาหมู",                  opts: [] },
  { id: 21, cat: "เครื่องเคียง", name: "ไข่เป็ดต้ม",        price: 10, img: "duck_egg",       badge: null,          desc: "ไข่เป็ดต้มสดใหม่ เนื้อนุ่มหอม",                 opts: [] },
  { id: 22, cat: "เครื่องเคียง", name: "หมั่นโถววอฟเฟิล",   price: 15, img: "waffle_mantou",  badge: null,          desc: "หมั่นโถววอฟเฟิลอบกรอบ หอมหวาน",                opts: [] },
  { id: 23, cat: "เครื่องเคียง", name: "น้ำจิ้มพริกส้ม",    price: 20, img: "orange_sauce",   badge: null,          desc: "น้ำจิ้มพริกส้มสูตรร้าน รสจัดจ้าน",              opts: [] },
  { id: 24, cat: "เครื่องเคียง", name: "พริกกระเทียม",       price: 10, img: "chili_garlic",   badge: null,          desc: "พริกกระเทียมสดๆ เข้มข้น กลมกล่อม",              opts: [] },
  { id: 25, cat: "เครื่องเคียง", name: "น้ำเปล่า",          price: 10, img: "water",          badge: null,          desc: "น้ำดื่มสิงห์ ขวดเย็น สะอาด",                    opts: [] },
  { id: 27, cat: "เครื่องเคียง", name: "ไอศกรีมลุงชม",      price: 45, img: "icecream_lungchom", badge: null,       desc: "ไอศกรีมลุงชมเชียงราย รสกะทิ หอมมะพร้าวแท้",    opts: [] },

  // ── กาแฟ Premium ──────────────────────────────────────────────
  {
    id: 8, cat: "กาแฟ Premium", name: "กาแฟขี้ชะมดร้อน", price: 199,
    img: "civet_hot", badge: "Signature",
    desc: "Hot Civet Coffee หอมเข้ม รสนุ่มละมุน จากเชียงราย",
    opts: [
      { id: "espresso",  label: "Espresso",  price: 0, group: "style" },
      { id: "americano", label: "Americano", price: 0, group: "style" },
      { id: "less",      label: "หวานน้อย", price: 0, group: "sweet" },
      { id: "nosweet",   label: "ไม่หวาน",  price: 0, group: "sweet" },
    ],
  },

  {
    id: 9, cat: "กาแฟ Premium", name: "กาแฟขี้ชะมดเย็น", price: 299,
    img: "civet_iced", badge: "Signature",
    desc: "Iced Civet Coffee หอมเข้ม สดชื่น ดื่มเพลิน",
    opts: [
      { id: "espresso",  label: "Espresso",  price: 0, group: "style" },
      { id: "americano", label: "Americano", price: 0, group: "style" },
      { id: "less",      label: "หวานน้อย", price: 0, group: "sweet" },
      { id: "nosweet",   label: "ไม่หวาน",  price: 0, group: "sweet" },
      { id: "nomilk",    label: "ไม่ใส่นม", price: 0, group: "sweet" },
    ],
  },

  // ── เครื่องดื่ม ───────────────────────────────────────────────
  // หมายเหตุ: ราคาตั้งต้น = เย็น, ถ้าเลือก "ร้อน" จะหัก 10฿ (price: -10)
  {
    id: 10, cat: "เครื่องดื่ม", name: "Espresso", price: 40,
    img: "espresso_new", badge: null,
    desc: "เอสเพรสโซ่เข้มข้น | ร้อน 30฿",
    opts: [
      { id: "cold",    label: "เย็น",       price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",       price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",       price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",   price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย",  price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ",  price: 0,   group: "sweet" },
    ],
  },
  {
    id: 11, cat: "เครื่องดื่ม", name: "Americano", price: 40,
    img: "americano", badge: null,
    desc: "อเมริกาโน่รสนุ่ม | ร้อน 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 12, cat: "เครื่องดื่ม", name: "Cappuccino", price: 40,
    img: "latte", badge: null,
    desc: "คาปูชิโน่ฟองนมนุ่ม | ร้อน 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 13, cat: "เครื่องดื่ม", name: "Coffee Latte", price: 40,
    img: "latte", badge: null,
    desc: "ลาเต้นมหอมละมุน | ร้อน 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 14, cat: "เครื่องดื่ม", name: "Mocha Coffee", price: 40,
    img: "mocha", badge: null,
    desc: "มอคค่าช็อกโกแลต | ร้อน 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 15, cat: "เครื่องดื่ม", name: "ชาไทย", price: 40,
    img: "thai_tea", badge: null,
    desc: "ชาไทยหอมนมสด | ร้อน 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 16, cat: "เครื่องดื่ม", name: "ชาเขียว", price: 40,
    img: "green_tea", badge: null,
    desc: "ชาเขียวญี่ปุ่นนมสด | ร้อน 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 17, cat: "เครื่องดื่ม", name: "นมเย็น", price: 40,
    img: "milk_cold", badge: null,
    desc: "นมสดเย็นสดชื่น | ร้อน 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 18, cat: "เครื่องดื่ม", name: "โกโก้", price: 40,
    img: "cocoa_new", badge: null,
    desc: "โกโก้ครีมท็อป ช็อกโกแลตแท้ | ร้อน 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", price: 0,   group: "sweet" },
    ],
  },
  { id: 28, cat: "เครื่องดื่ม", name: "น้ำอัดลม", price: 15, img: "soda", badge: null, desc: "น้ำอัดลม (โค้ก/เป๊ปซี่/สไปรท์)", opts: [] },

];

// ── หมวดหมู่ ──────────────────────────────────────────────────
export const CATS = ["ทั้งหมด", "ขาหมู", "ข้าวขาหมู", "เครื่องเคียง", "กาแฟ Premium", "เครื่องดื่ม"];

// ── ข้อความแนะนำสินค้า (upsell) ──────────────────────────────
export const UPSELL = {
  4: "คนส่วนใหญ่เพิ่มไข่เป็ดต้มด้วย 🥚 +10฿",
  5: "รับหมั่นโถวทานเคียงไหมคะ? 🥟",
  1: "รับกาแฟขี้ชะมดเย็นด้วยไหมคะ? ☕",
  2: "รับข้าวเปล่าเพิ่มไหมคะ? 🍚",
  8: "รับขาหมูทานคู่กาแฟไหมครับ? 🍖",
};

// ── ชื่อกลุ่มตัวเลือก ─────────────────────────────────────────
export const GROUP_LABEL = {
  size:  "ขนาด",
  type:  "เลือกเนื้อ",
  add:   "เพิ่มเติม",
  style: "สไตล์กาแฟ",
  sweet: "ความหวาน",
  temp:  "อุณหภูมิ / แบบ",
};
