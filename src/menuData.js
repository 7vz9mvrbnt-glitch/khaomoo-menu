// ================================================================
// ไฟล์นี้คือที่เก็บข้อมูลเมนูทั้งหมด
// แก้ไขราคาได้ที่นี่เลย โดยไม่ต้องไปแตะ App.jsx
//
// โครงสร้างแต่ละรายการ:
//   id      : หมายเลขเมนู (ห้ามซ้ำ)
//   cat     : หมวดหมู่ (ภาษาไทย)
//   cat_en  : หมวดหมู่ (ภาษาอังกฤษ)
//   name    : ชื่อเมนู (ภาษาไทย)
//   name_en : ชื่อเมนู (ภาษาอังกฤษ)
//   price   : ราคาตั้งต้น (บาท)  ← แก้ตรงนี้เพื่อเปลี่ยนราคา
//   img     : key รูปภาพ (อย่าแก้ถ้าไม่ได้เปลี่ยนรูป)
//   badge   : ป้ายกำกับ เช่น "Best Seller" | null = ไม่มีป้าย
//   badge_en: ป้ายกำกับ (ภาษาอังกฤษ)
//   desc    : คำอธิบายเมนู (ภาษาไทย)
//   desc_en : คำอธิบายเมนู (ภาษาอังกฤษ)
//   opts    : ตัวเลือกเสริม (size, type, add-on) — price ในนี้คือราคาที่บวกเพิ่มจากราคาตั้งต้น
// ================================================================

export const MENU = [

  // ── ขาหมู ─────────────────────────────────────────────────────
  {
    id: 1, cat: "ขาหมู", cat_en: "Pork Knuckle",
    name: "ชุดขาหมูพะโล้", name_en: "Pork Knuckle Braised Set",
    price: 400, img: "khaomoo_set", badge: "แชร์ได้", badge_en: "Shareable",
    desc: "ขาหมูพะโล้สูตรร้าน เนื้อนุ่ม หนังฉ่ำ เสิร์ฟพร้อมน้ำจิ้มและผักกาดดอง",
    desc_en: "Whole pork knuckle in house palo spices, tender & juicy skin, served with dipping sauce and pickled cabbage",
    opts: [
      { id: "khamoo",  label: "ชุดขาหมู (1 ขา)", label_en: "Pork Knuckle Set (1 leg)", price: 0,  group: "type" },
      { id: "kaki",    label: "ชุดคากิ",          label_en: "Kaki (Pork Skin) Set",    price: 0,  group: "type" },
      { id: "egg",     label: "+ ไข่เป็ดต้ม",     label_en: "+ Boiled Duck Egg",       price: 10, group: "add"  },
      { id: "mantou",  label: "+ หมั่นโถว",       label_en: "+ Mantou Bun",            price: 10, group: "add"  },
      { id: "pickle",  label: "+ ผักกาดดอง",      label_en: "+ Pickled Cabbage",       price: 20, group: "add"  },
    ],
  },

  {
    id: 2, cat: "ขาหมู", cat_en: "Pork Knuckle",
    name: "ชุดขาหมูพะโล้สับ", name_en: "Chopped Pork Knuckle Set",
    price: 100, img: "khaomoo_chop", badge: "Best Seller", badge_en: "Best Seller",
    desc: "ขาหมูสับพร้อมเสิร์ฟ เลือกขนาดและเนื้อตามชอบ",
    desc_en: "Chopped pork knuckle in palo braise, choose your size and meat preference",
    opts: [
      { id: "size100",    label: "ชุด 100 บาท",   label_en: "100 Baht Set",                    price: 0,  group: "size" },
      { id: "size150",    label: "ชุด 150 บาท",   label_en: "150 Baht Set",                    price: 50, group: "size" },
      { id: "skin",       label: "เนื้อหนัง",     label_en: "Meat & Skin",                     price: 0,  group: "type" },
      { id: "meat_only",  label: "เนื้อล้วน",     label_en: "Meat Only",                       price: 0,  group: "type" },
      { id: "kaki",       label: "ขาหมูคากิ",     label_en: "Pork Knuckle + Kaki",             price: 0,  group: "type" },
      { id: "guts",       label: "ขาหมูไส้",      label_en: "Pork Knuckle + Innards",          price: 0,  group: "type" },
      { id: "kaki_guts",  label: "ขาหมูคากิไส้", label_en: "Pork Knuckle + Kaki + Innards",   price: 0,  group: "type" },
      { id: "skin_heavy", label: "เน้นหนัง",      label_en: "Extra Skin",                      price: 0,  group: "type" },
      { id: "egg",        label: "+ ไข่เป็ดต้ม",  label_en: "+ Boiled Duck Egg",               price: 10, group: "add"  },
    ],
  },

  {
    id: 3, cat: "ขาหมู", cat_en: "Pork Knuckle",
    name: "ชุดคากิพะโล้สับ", name_en: "Chopped Pork Skin Set",
    price: 100, img: "kaki_chop", badge: "สายหนัง", badge_en: "Pork Skin Fan",
    desc: "คากินุ่มหนึบ เคี่ยวจนเข้าเนื้อ หอมเครื่องพะโล้",
    desc_en: "Melt-in-your-mouth pork skin, braised until tender and fragrant with palo spices",
    opts: [
      { id: "size100",      label: "ชุด 100 บาท",   label_en: "100 Baht Set",                    price: 0,  group: "size" },
      { id: "size150",      label: "ชุด 150 บาท",   label_en: "150 Baht Set",                    price: 50, group: "size" },
      { id: "kaki_only",    label: "คากิล้วน",      label_en: "Kaki Only",                       price: 0,  group: "type" },
      { id: "km_kaki",      label: "ขาหมูคากิ",     label_en: "Pork Knuckle + Kaki",             price: 0,  group: "type" },
      { id: "kaki_guts",    label: "คากิไส้",       label_en: "Kaki + Innards",                  price: 0,  group: "type" },
      { id: "km_kaki_guts", label: "ขาหมูคากิไส้", label_en: "Pork Knuckle + Kaki + Innards",   price: 0,  group: "type" },
      { id: "egg",          label: "+ ไข่เป็ดต้ม",  label_en: "+ Boiled Duck Egg",               price: 10, group: "add"  },
    ],
  },

  {
    id: 26, cat: "ขาหมู", cat_en: "Pork Knuckle",
    name: "ชุดไส้พะโล้เตาถ่าน", name_en: "Charcoal Pork Innards Set",
    price: 100, img: "guts_palo", badge: null,
    desc: "ไส้พะโล้เตาถ่านเคี่ยวจนเข้าเนื้อ หอมเครื่อง นุ่มหนึบ สูตรต้นตำรับ",
    desc_en: "Charcoal-braised pork innards in palo spices, tender and deeply aromatic, classic recipe",
    opts: [
      { id: "size100",      label: "ชุด 100 บาท",   label_en: "100 Baht Set",                    price: 0,  group: "size" },
      { id: "size150",      label: "ชุด 150 บาท",   label_en: "150 Baht Set",                    price: 50, group: "size" },
      { id: "guts_only",    label: "ไส้ล้วน",       label_en: "Innards Only",                    price: 0,  group: "type" },
      { id: "km_guts",      label: "ขาหมูไส้",      label_en: "Pork Knuckle + Innards",          price: 0,  group: "type" },
      { id: "kaki_guts",    label: "คากิไส้",       label_en: "Kaki + Innards",                  price: 0,  group: "type" },
      { id: "km_kaki_guts", label: "ขาหมูคากิไส้", label_en: "Pork Knuckle + Kaki + Innards",   price: 0,  group: "type" },
      { id: "egg",          label: "+ ไข่เป็ดต้ม",  label_en: "+ Boiled Duck Egg",               price: 10, group: "add"  },
    ],
  },

  // ── ข้าวขาหมู ─────────────────────────────────────────────────
  {
    id: 4, cat: "ข้าวขาหมู", cat_en: "Rice Dishes",
    name: "ข้าวขาหมูพะโล้เตาถ่าน", name_en: "Charcoal Pork Knuckle Rice",
    price: 60, img: "rice_khaomoo", badge: "Best Seller", badge_en: "Best Seller",
    desc: "ข้าวขาหมูสูตรเตาถ่าน เสิร์ฟพร้อมน้ำจิ้มและผักกาดดอง",
    desc_en: "Charcoal-braised pork knuckle over jasmine rice, served with dipping sauce and pickled cabbage",
    opts: [
      { id: "normal",    label: "ธรรมดา",         label_en: "Regular",                        price: 0,  group: "size" },
      { id: "special",   label: "พิเศษ",          label_en: "Special",                        price: 10, group: "size" },
      { id: "jumbo",     label: "จัมโบ้",          label_en: "Jumbo",                          price: 20, group: "size" },
      { id: "meat_only", label: "เนื้อล้วน",      label_en: "Meat Only",                      price: 0,  group: "type" },
      { id: "skin",      label: "เนื้อหนัง",      label_en: "Meat & Skin",                    price: 0,  group: "type" },
      { id: "guts_only", label: "ไส้ล้วน",        label_en: "Innards Only",                   price: 0,  group: "type" },
      { id: "kaki",      label: "ขาหมู + คากิ",   label_en: "Pork Knuckle + Kaki",            price: 0,  group: "type" },
      { id: "guts",      label: "ขาหมู + ไส้",    label_en: "Pork Knuckle + Innards",         price: 0,  group: "type" },
      { id: "kaki_guts", label: "ขาหมู คากิ ไส้", label_en: "Pork Knuckle + Kaki + Innards",  price: 0,  group: "type" },
      { id: "skin_heavy",label: "เน้นหนัง",       label_en: "Extra Skin",                     price: 0,  group: "type" },
      { id: "egg",       label: "+ ไข่เป็ดต้ม",   label_en: "+ Boiled Duck Egg",              price: 10, group: "add"  },
      { id: "mantou",    label: "+ หมั่นโถว",     label_en: "+ Mantou Bun",                   price: 10, group: "add"  },
    ],
  },

  {
    id: 5, cat: "ข้าวขาหมู", cat_en: "Rice Dishes",
    name: "ข้าวคากิพะโล้เตาถ่าน", name_en: "Charcoal Pork Skin Rice",
    price: 60, img: "rice_kaki", badge: "ขายดี", badge_en: "Popular",
    desc: "คากินุ่มละลายในปาก เสิร์ฟพร้อมข้าวหอมร้อนๆ",
    desc_en: "Melt-in-your-mouth pork skin served over hot steamed rice",
    opts: [
      { id: "normal",    label: "ธรรมดา",        label_en: "Regular",                       price: 0,  group: "size" },
      { id: "special",   label: "พิเศษ",         label_en: "Special",                       price: 10, group: "size" },
      { id: "jumbo",     label: "จัมโบ้",         label_en: "Jumbo",                         price: 20, group: "size" },
      { id: "kaki_only", label: "คากิล้วน",      label_en: "Kaki Only",                     price: 0,  group: "type" },
      { id: "kaki_km",   label: "ขาหมู + คากิ",  label_en: "Pork Knuckle + Kaki",           price: 0,  group: "type" },
      { id: "kaki_guts", label: "คากิ + ไส้",    label_en: "Kaki + Innards",                price: 0,  group: "type" },
      { id: "all3",      label: "ขาหมู คากิ ไส้", label_en: "Pork Knuckle + Kaki + Innards", price: 0,  group: "type" },
      { id: "egg",       label: "+ ไข่เป็ดต้ม",  label_en: "+ Boiled Duck Egg",             price: 10, group: "add"  },
      { id: "mantou",    label: "+ หมั่นโถว",    label_en: "+ Mantou Bun",                  price: 10, group: "add"  },
    ],
  },

  // ── เครื่องเคียง ──────────────────────────────────────────────
  { id: 6,  cat: "เครื่องเคียง", cat_en: "Sides", name: "ข้าวเปล่า",        name_en: "Steamed Rice",            price: 10, img: "rice_plain",     badge: null,          desc: "ข้าวสวยร้อนๆ หอมนุ่ม",                         desc_en: "Hot steamed jasmine rice, soft and fragrant",            opts: [] },
  { id: 7,  cat: "เครื่องเคียง", cat_en: "Sides", name: "หมั่นโถว (1 ลูก)", name_en: "Mantou Bun (1 pc)",       price: 10, img: "mantou_new",     badge: "Best Seller", badge_en: "Best Seller", desc: "หมั่นโถวนึ่งเนื้อนุ่ม ทานคู่พะโล้",             desc_en: "Steamed mantou bun, soft texture, perfect with palo braise", opts: [] },
  { id: 19, cat: "เครื่องเคียง", cat_en: "Sides", name: "ผักกาดดอง",         name_en: "Pickled Cabbage",         price: 20, img: "pickle_cab",     badge: null,          desc: "ผักกาดดองรสเปรี้ยวหวาน ทานคู่ขาหมูลงตัว",       desc_en: "Sweet-sour pickled cabbage, pairs perfectly with pork knuckle", opts: [] },
  { id: 20, cat: "เครื่องเคียง", cat_en: "Sides", name: "ไชเท้า",            name_en: "Pickled Radish",          price: 20, img: "daikon",         badge: null,          desc: "ไชเท้าดองกรอบหวาน เคียงขาหมู",                  desc_en: "Crispy sweet-pickled radish, great alongside pork knuckle", opts: [] },
  { id: 21, cat: "เครื่องเคียง", cat_en: "Sides", name: "ไข่เป็ดต้ม",        name_en: "Boiled Duck Egg",         price: 10, img: "duck_egg",       badge: null,          desc: "ไข่เป็ดต้มสดใหม่ เนื้อนุ่มหอม",                 desc_en: "Fresh boiled duck egg, tender and savory",               opts: [] },
  { id: 22, cat: "เครื่องเคียง", cat_en: "Sides", name: "หมั่นโถววอฟเฟิล",   name_en: "Waffle Mantou",           price: 15, img: "waffle_mantou",  badge: null,          desc: "หมั่นโถววอฟเฟิลอบกรอบ หอมหวาน",                desc_en: "Crispy baked waffle mantou, lightly sweet",              opts: [] },
  { id: 23, cat: "เครื่องเคียง", cat_en: "Sides", name: "น้ำจิ้มพริกส้ม",    name_en: "Chili Orange Sauce",      price: 20, img: "orange_sauce",   badge: null,          desc: "น้ำจิ้มพริกส้มสูตรร้าน รสจัดจ้าน",              desc_en: "House-recipe chili orange dipping sauce, bold and tangy", opts: [] },
  { id: 24, cat: "เครื่องเคียง", cat_en: "Sides", name: "พริกกระเทียม",       name_en: "Chili Garlic",            price: 10, img: "chili_garlic",   badge: null,          desc: "พริกกระเทียมสดๆ เข้มข้น กลมกล่อม",              desc_en: "Fresh chili garlic, rich and savory",                    opts: [] },
  { id: 25, cat: "เครื่องเคียง", cat_en: "Sides", name: "น้ำเปล่า",          name_en: "Water",                   price: 10, img: "water",          badge: null,          desc: "น้ำดื่มสิงห์ ขวดเย็น สะอาด",                    desc_en: "Singha drinking water, chilled",                         opts: [] },
  { id: 27, cat: "เครื่องเคียง", cat_en: "Sides", name: "ไอศกรีมลุงชม",      name_en: "Uncle Chom Ice Cream",    price: 45, img: "icecream_lungchom", badge: null,       desc: "ไอศกรีมลุงชมเชียงราย รสกะทิ หอมมะพร้าวแท้",    desc_en: "Uncle Chom Chiang Rai coconut ice cream, authentic coconut flavour", opts: [] },

  // ── กาแฟ Premium ──────────────────────────────────────────────
  {
    id: 8, cat: "กาแฟ Premium", cat_en: "Premium Coffee",
    name: "กาแฟขี้ชะมดร้อน", name_en: "Hot Kopi Luwak Coffee",
    price: 199, img: "civet_hot", badge: "Signature", badge_en: "Signature",
    desc: "Hot Civet Coffee หอมเข้ม รสนุ่มละมุน จากเชียงราย",
    desc_en: "Hot Kopi Luwak — rich aroma, exceptionally smooth, sourced from Chiang Rai",
    opts: [
      { id: "espresso",  label: "Espresso",  label_en: "Espresso",   price: 0, group: "style" },
      { id: "americano", label: "Americano", label_en: "Americano",  price: 0, group: "style" },
      { id: "less",      label: "หวานน้อย", label_en: "Less Sweet", price: 0, group: "sweet" },
      { id: "nosweet",   label: "ไม่หวาน",  label_en: "No Sugar",   price: 0, group: "sweet" },
    ],
  },

  {
    id: 9, cat: "กาแฟ Premium", cat_en: "Premium Coffee",
    name: "กาแฟขี้ชะมดเย็น", name_en: "Iced Kopi Luwak Coffee",
    price: 299, img: "civet_iced", badge: "Signature", badge_en: "Signature",
    desc: "Iced Civet Coffee หอมเข้ม สดชื่น ดื่มเพลิน",
    desc_en: "Iced Kopi Luwak — rich aroma, refreshing and smooth over ice",
    opts: [
      { id: "espresso",  label: "Espresso",  label_en: "Espresso",   price: 0, group: "style" },
      { id: "americano", label: "Americano", label_en: "Americano",  price: 0, group: "style" },
      { id: "less",      label: "หวานน้อย", label_en: "Less Sweet", price: 0, group: "sweet" },
      { id: "nosweet",   label: "ไม่หวาน",  label_en: "No Sugar",   price: 0, group: "sweet" },
      { id: "nomilk",    label: "ไม่ใส่นม", label_en: "No Milk",    price: 0, group: "sweet" },
    ],
  },

  // ── เครื่องดื่ม ───────────────────────────────────────────────
  // หมายเหตุ: ราคาตั้งต้น = เย็น, ถ้าเลือก "ร้อน" จะหัก 10฿ (price: -10)
  {
    id: 10, cat: "เครื่องดื่ม", cat_en: "Beverages",
    name: "Espresso", name_en: "Espresso",
    price: 40, img: "espresso_new", badge: null,
    desc: "เอสเพรสโซ่เข้มข้น | ร้อน 30฿",
    desc_en: "Concentrated espresso shot | Hot 30฿",
    opts: [
      { id: "cold",    label: "เย็น",       label_en: "Iced",         price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",       label_en: "Hot",          price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",       label_en: "Blended",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",   label_en: "No Sugar",     price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย",  label_en: "Less Sweet",   price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ",  label_en: "Normal Sweet", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 11, cat: "เครื่องดื่ม", cat_en: "Beverages",
    name: "Americano", name_en: "Americano",
    price: 40, img: "americano", badge: null,
    desc: "อเมริกาโน่รสนุ่ม | ร้อน 30฿",
    desc_en: "Smooth americano | Hot 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      label_en: "Iced",         price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      label_en: "Hot",          price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      label_en: "Blended",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  label_en: "No Sugar",     price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", label_en: "Less Sweet",   price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", label_en: "Normal Sweet", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 12, cat: "เครื่องดื่ม", cat_en: "Beverages",
    name: "Cappuccino", name_en: "Cappuccino",
    price: 40, img: "latte", badge: null,
    desc: "คาปูชิโน่ฟองนมนุ่ม | ร้อน 30฿",
    desc_en: "Cappuccino with silky milk foam | Hot 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      label_en: "Iced",         price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      label_en: "Hot",          price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      label_en: "Blended",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  label_en: "No Sugar",     price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", label_en: "Less Sweet",   price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", label_en: "Normal Sweet", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 13, cat: "เครื่องดื่ม", cat_en: "Beverages",
    name: "Coffee Latte", name_en: "Coffee Latte",
    price: 40, img: "latte", badge: null,
    desc: "ลาเต้นมหอมละมุน | ร้อน 30฿",
    desc_en: "Creamy milk latte | Hot 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      label_en: "Iced",         price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      label_en: "Hot",          price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      label_en: "Blended",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  label_en: "No Sugar",     price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", label_en: "Less Sweet",   price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", label_en: "Normal Sweet", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 14, cat: "เครื่องดื่ม", cat_en: "Beverages",
    name: "Mocha Coffee", name_en: "Mocha Coffee",
    price: 40, img: "mocha", badge: null,
    desc: "มอคค่าช็อกโกแลต | ร้อน 30฿",
    desc_en: "Chocolate mocha coffee | Hot 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      label_en: "Iced",         price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      label_en: "Hot",          price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      label_en: "Blended",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  label_en: "No Sugar",     price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", label_en: "Less Sweet",   price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", label_en: "Normal Sweet", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 15, cat: "เครื่องดื่ม", cat_en: "Beverages",
    name: "ชาไทย", name_en: "Thai Tea",
    price: 40, img: "thai_tea", badge: null,
    desc: "ชาไทยหอมนมสด | ร้อน 30฿",
    desc_en: "Thai tea with fresh milk | Hot 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      label_en: "Iced",         price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      label_en: "Hot",          price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      label_en: "Blended",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  label_en: "No Sugar",     price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", label_en: "Less Sweet",   price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", label_en: "Normal Sweet", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 16, cat: "เครื่องดื่ม", cat_en: "Beverages",
    name: "ชาเขียว", name_en: "Green Tea",
    price: 40, img: "green_tea", badge: null,
    desc: "ชาเขียวญี่ปุ่นนมสด | ร้อน 30฿",
    desc_en: "Japanese green tea with fresh milk | Hot 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      label_en: "Iced",         price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      label_en: "Hot",          price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      label_en: "Blended",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  label_en: "No Sugar",     price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", label_en: "Less Sweet",   price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", label_en: "Normal Sweet", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 17, cat: "เครื่องดื่ม", cat_en: "Beverages",
    name: "นมเย็น", name_en: "Fresh Milk",
    price: 40, img: "milk_cold", badge: null,
    desc: "นมสดเย็นสดชื่น | ร้อน 30฿",
    desc_en: "Fresh cold milk | Hot 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      label_en: "Iced",         price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      label_en: "Hot",          price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      label_en: "Blended",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  label_en: "No Sugar",     price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", label_en: "Less Sweet",   price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", label_en: "Normal Sweet", price: 0,   group: "sweet" },
    ],
  },
  {
    id: 18, cat: "เครื่องดื่ม", cat_en: "Beverages",
    name: "โกโก้", name_en: "Cocoa",
    price: 40, img: "cocoa_new", badge: null,
    desc: "โกโก้ครีมท็อป ช็อกโกแลตแท้ | ร้อน 30฿",
    desc_en: "Cocoa with cream top, real chocolate | Hot 30฿",
    opts: [
      { id: "cold",    label: "เย็น",      label_en: "Iced",         price: 0,   group: "temp"  },
      { id: "hot",     label: "ร้อน",      label_en: "Hot",          price: -10, group: "temp"  },
      { id: "blend",   label: "ปั่น",      label_en: "Blended",      price: 5,   group: "temp"  },
      { id: "nosweet", label: "ไม่หวาน",  label_en: "No Sugar",     price: 0,   group: "sweet" },
      { id: "less",    label: "หวานน้อย", label_en: "Less Sweet",   price: 0,   group: "sweet" },
      { id: "normal",  label: "หวานปกติ", label_en: "Normal Sweet", price: 0,   group: "sweet" },
    ],
  },
  { id: 28, cat: "เครื่องดื่ม", cat_en: "Beverages", name: "น้ำอัดลม", name_en: "Soft Drink", price: 15, img: "soda", badge: null, desc: "น้ำอัดลม (โค้ก/เป๊ปซี่/สไปรท์)", desc_en: "Soft drink (Coke / Pepsi / Sprite)", opts: [] },

];

// ── หมวดหมู่ ──────────────────────────────────────────────────
export const CATS    = ["ทั้งหมด", "ขาหมู", "ข้าวขาหมู", "เครื่องเคียง", "กาแฟ Premium", "เครื่องดื่ม"];
export const CATS_EN = ["All",     "Pork Knuckle", "Rice Dishes", "Sides", "Premium Coffee", "Beverages"];

// ── ข้อความแนะนำสินค้า (upsell) ──────────────────────────────
export const UPSELL = {
  4: "คนส่วนใหญ่เพิ่มไข่เป็ดต้มด้วย 🥚 +10฿",
  5: "รับหมั่นโถวทานเคียงไหมคะ? 🥟",
  1: "รับกาแฟขี้ชะมดเย็นด้วยไหมคะ? ☕",
  2: "รับข้าวเปล่าเพิ่มไหมคะ? 🍚",
  8: "รับขาหมูทานคู่กาแฟไหมครับ? 🍖",
};
export const UPSELL_EN = {
  4: "Most people add a duck egg too 🥚 +10฿",
  5: "Add mantou buns on the side? 🥟",
  1: "How about a cold Kopi Luwak? ☕",
  2: "Add a bowl of steamed rice? 🍚",
  8: "Pair your pork knuckle with coffee? 🍖",
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
export const GROUP_LABEL_EN = {
  size:  "Size",
  type:  "Meat Choice",
  add:   "Add-ons",
  style: "Coffee Style",
  sweet: "Sweetness",
  temp:  "Temperature / Type",
};
