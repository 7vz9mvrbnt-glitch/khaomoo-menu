-- ================================================================
-- Supabase seed: สร้างตาราง menu และใส่ข้อมูลทั้งหมด
-- วิธีใช้: เปิด Supabase Dashboard → SQL Editor → วางโค้ดนี้ทั้งหมด → Run
-- ================================================================

-- 1. สร้างตาราง
CREATE TABLE IF NOT EXISTS public.menu (
  id           integer  PRIMARY KEY,
  cat          text     NOT NULL,
  name         text     NOT NULL,
  price        integer  NOT NULL,
  img          text     NOT NULL,
  badge        text,
  description  text,
  opts         jsonb    NOT NULL DEFAULT '[]'::jsonb,
  is_available boolean  NOT NULL DEFAULT true
);

-- 2. เปิด RLS + อนุญาตให้อ่านได้สาธารณะ
ALTER TABLE public.menu ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "allow_public_read" ON public.menu;
CREATE POLICY "allow_public_read" ON public.menu
  FOR SELECT USING (true);

-- 3. ใส่ข้อมูลเมนู (upsert — รันซ้ำได้ปลอดภัย)
INSERT INTO public.menu (id, cat, name, price, img, badge, description, opts) VALUES
(1, 'ขาหมู', 'ชุดขาหมูพะโล้', 400, 'khaomoo_set', 'แชร์ได้', 'ขาหมูพะโล้สูตรร้าน เนื้อนุ่ม หนังฉ่ำ เสิร์ฟพร้อมน้ำจิ้มและผักกาดดอง', '[{"id":"khamoo","label":"ชุดขาหมู (1 ขา)","price":0,"group":"type"},{"id":"kaki","label":"ชุดคากิ","price":0,"group":"type"},{"id":"egg","label":"+ ไข่เป็ดต้ม","price":10,"group":"add"},{"id":"mantou","label":"+ หมั่นโถว","price":10,"group":"add"},{"id":"pickle","label":"+ ผักกาดดอง","price":20,"group":"add"}]'::jsonb),
(2, 'ขาหมู', 'ชุดขาหมูพะโล้สับ', 100, 'khaomoo_chop', 'Best Seller', 'ขาหมูสับพร้อมเสิร์ฟ เลือกขนาดและเนื้อตามชอบ', '[{"id":"size100","label":"ชุด 100 บาท","price":0,"group":"size"},{"id":"size150","label":"ชุด 150 บาท","price":50,"group":"size"},{"id":"skin","label":"เนื้อหนัง","price":0,"group":"type"},{"id":"meat_only","label":"เนื้อล้วน","price":0,"group":"type"},{"id":"kaki","label":"ขาหมูคากิ","price":0,"group":"type"},{"id":"guts","label":"ขาหมูไส้","price":0,"group":"type"},{"id":"kaki_guts","label":"ขาหมูคากิไส้","price":0,"group":"type"},{"id":"skin_heavy","label":"เน้นหนัง","price":0,"group":"type"},{"id":"egg","label":"+ ไข่เป็ดต้ม","price":10,"group":"add"}]'::jsonb),
(3, 'ขาหมู', 'ชุดคากิพะโล้สับ', 100, 'kaki_chop', 'สายหนัง', 'คากินุ่มหนึบ เคี่ยวจนเข้าเนื้อ หอมเครื่องพะโล้', '[{"id":"size100","label":"ชุด 100 บาท","price":0,"group":"size"},{"id":"size150","label":"ชุด 150 บาท","price":50,"group":"size"},{"id":"kaki_only","label":"คากิล้วน","price":0,"group":"type"},{"id":"km_kaki","label":"ขาหมูคากิ","price":0,"group":"type"},{"id":"kaki_guts","label":"คากิไส้","price":0,"group":"type"},{"id":"km_kaki_guts","label":"ขาหมูคากิไส้","price":0,"group":"type"},{"id":"egg","label":"+ ไข่เป็ดต้ม","price":10,"group":"add"}]'::jsonb),
(26, 'ขาหมู', 'ชุดไส้พะโล้เตาถ่าน', 100, 'guts_palo', NULL, 'ไส้พะโล้เตาถ่านเคี่ยวจนเข้าเนื้อ หอมเครื่อง นุ่มหนึบ สูตรต้นตำรับ', '[{"id":"size100","label":"ชุด 100 บาท","price":0,"group":"size"},{"id":"size150","label":"ชุด 150 บาท","price":50,"group":"size"},{"id":"guts_only","label":"ไส้ล้วน","price":0,"group":"type"},{"id":"km_guts","label":"ขาหมูไส้","price":0,"group":"type"},{"id":"kaki_guts","label":"คากิไส้","price":0,"group":"type"},{"id":"km_kaki_guts","label":"ขาหมูคากิไส้","price":0,"group":"type"},{"id":"egg","label":"+ ไข่เป็ดต้ม","price":10,"group":"add"}]'::jsonb),
(4, 'ข้าวขาหมู', 'ข้าวขาหมูพะโล้เตาถ่าน', 60, 'rice_khaomoo', 'Best Seller', 'ข้าวขาหมูสูตรเตาถ่าน เสิร์ฟพร้อมน้ำจิ้มและผักกาดดอง', '[{"id":"normal","label":"ธรรมดา","price":0,"group":"size"},{"id":"special","label":"พิเศษ","price":10,"group":"size"},{"id":"jumbo","label":"จัมโบ้","price":20,"group":"size"},{"id":"meat_only","label":"เนื้อล้วน","price":0,"group":"type"},{"id":"skin","label":"เนื้อหนัง","price":0,"group":"type"},{"id":"kaki","label":"ขาหมู + คากิ","price":0,"group":"type"},{"id":"guts","label":"ขาหมู + ไส้","price":0,"group":"type"},{"id":"kaki_guts","label":"ขาหมู คากิ ไส้","price":0,"group":"type"},{"id":"skin_heavy","label":"เน้นหนัง","price":0,"group":"type"},{"id":"egg","label":"+ ไข่เป็ดต้ม","price":10,"group":"add"},{"id":"mantou","label":"+ หมั่นโถว","price":10,"group":"add"}]'::jsonb),
(5, 'ข้าวขาหมู', 'ข้าวคากิพะโล้เตาถ่าน', 60, 'rice_kaki', 'ขายดี', 'คากินุ่มละลายในปาก เสิร์ฟพร้อมข้าวหอมร้อนๆ', '[{"id":"normal","label":"ธรรมดา","price":0,"group":"size"},{"id":"special","label":"พิเศษ","price":10,"group":"size"},{"id":"jumbo","label":"จัมโบ้","price":20,"group":"size"},{"id":"kaki_only","label":"คากิล้วน","price":0,"group":"type"},{"id":"kaki_km","label":"ขาหมู + คากิ","price":0,"group":"type"},{"id":"kaki_guts","label":"คากิ + ไส้","price":0,"group":"type"},{"id":"all3","label":"ขาหมู คากิ ไส้","price":0,"group":"type"},{"id":"egg","label":"+ ไข่เป็ดต้ม","price":10,"group":"add"},{"id":"mantou","label":"+ หมั่นโถว","price":10,"group":"add"}]'::jsonb),
(6, 'เครื่องเคียง', 'ข้าวเปล่า', 10, 'rice_plain', NULL, 'ข้าวสวยร้อนๆ หอมนุ่ม', '[]'::jsonb),
(7, 'เครื่องเคียง', 'หมั่นโถว (1 ลูก)', 10, 'mantou_new', 'Best Seller', 'หมั่นโถวนึ่งเนื้อนุ่ม ทานคู่พะโล้', '[]'::jsonb),
(19, 'เครื่องเคียง', 'ผักกาดดอง', 20, 'pickle_cab', NULL, 'ผักกาดดองรสเปรี้ยวหวาน ทานคู่ขาหมูลงตัว', '[]'::jsonb),
(20, 'เครื่องเคียง', 'ไชเท้า', 20, 'daikon', NULL, 'ไชเท้าดองกรอบหวาน เคียงขาหมู', '[]'::jsonb),
(21, 'เครื่องเคียง', 'ไข่เป็ดต้ม', 10, 'duck_egg', NULL, 'ไข่เป็ดต้มสดใหม่ เนื้อนุ่มหอม', '[]'::jsonb),
(22, 'เครื่องเคียง', 'หมั่นโถววอฟเฟิล', 15, 'waffle_mantou', NULL, 'หมั่นโถววอฟเฟิลอบกรอบ หอมหวาน', '[]'::jsonb),
(23, 'เครื่องเคียง', 'น้ำจิ้มพริกส้ม', 20, 'orange_sauce', NULL, 'น้ำจิ้มพริกส้มสูตรร้าน รสจัดจ้าน', '[]'::jsonb),
(24, 'เครื่องเคียง', 'พริกกระเทียม', 10, 'chili_garlic', NULL, 'พริกกระเทียมสดๆ เข้มข้น กลมกล่อม', '[]'::jsonb),
(25, 'เครื่องเคียง', 'น้ำเปล่า', 10, 'water', NULL, 'น้ำดื่มสิงห์ ขวดเย็น สะอาด', '[]'::jsonb),
(27, 'เครื่องเคียง', 'ไอศกรีมลุงชม', 45, 'icecream_lungchom', NULL, 'ไอศกรีมลุงชมเชียงราย รสกะทิ หอมมะพร้าวแท้', '[]'::jsonb),
(8, 'กาแฟ Premium', 'กาแฟขี้ชะมดร้อน', 199, 'civet_hot', 'Signature', 'Hot Civet Coffee หอมเข้ม รสนุ่มละมุน จากเชียงราย', '[{"id":"espresso","label":"Espresso","price":0,"group":"style"},{"id":"americano","label":"Americano","price":0,"group":"style"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"}]'::jsonb),
(9, 'กาแฟ Premium', 'กาแฟขี้ชะมดเย็น', 299, 'civet_iced', 'Signature', 'Iced Civet Coffee หอมเข้ม สดชื่น ดื่มเพลิน', '[{"id":"espresso","label":"Espresso","price":0,"group":"style"},{"id":"americano","label":"Americano","price":0,"group":"style"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"nomilk","label":"ไม่ใส่นม","price":0,"group":"sweet"}]'::jsonb),
(10, 'เครื่องดื่ม', 'Espresso', 40, 'espresso_new', NULL, 'เอสเพรสโซ่เข้มข้น | ร้อน 30฿', '[{"id":"cold","label":"เย็น","price":0,"group":"temp"},{"id":"hot","label":"ร้อน","price":-10,"group":"temp"},{"id":"blend","label":"ปั่น","price":5,"group":"temp"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"normal","label":"หวานปกติ","price":0,"group":"sweet"}]'::jsonb),
(11, 'เครื่องดื่ม', 'Americano', 40, 'americano', NULL, 'อเมริกาโน่รสนุ่ม | ร้อน 30฿', '[{"id":"cold","label":"เย็น","price":0,"group":"temp"},{"id":"hot","label":"ร้อน","price":-10,"group":"temp"},{"id":"blend","label":"ปั่น","price":5,"group":"temp"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"normal","label":"หวานปกติ","price":0,"group":"sweet"}]'::jsonb),
(12, 'เครื่องดื่ม', 'Cappuccino', 40, 'latte', NULL, 'คาปูชิโน่ฟองนมนุ่ม | ร้อน 30฿', '[{"id":"cold","label":"เย็น","price":0,"group":"temp"},{"id":"hot","label":"ร้อน","price":-10,"group":"temp"},{"id":"blend","label":"ปั่น","price":5,"group":"temp"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"normal","label":"หวานปกติ","price":0,"group":"sweet"}]'::jsonb),
(13, 'เครื่องดื่ม', 'Coffee Latte', 40, 'latte', NULL, 'ลาเต้นมหอมละมุน | ร้อน 30฿', '[{"id":"cold","label":"เย็น","price":0,"group":"temp"},{"id":"hot","label":"ร้อน","price":-10,"group":"temp"},{"id":"blend","label":"ปั่น","price":5,"group":"temp"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"normal","label":"หวานปกติ","price":0,"group":"sweet"}]'::jsonb),
(14, 'เครื่องดื่ม', 'Mocha Coffee', 40, 'mocha', NULL, 'มอคค่าช็อกโกแลต | ร้อน 30฿', '[{"id":"cold","label":"เย็น","price":0,"group":"temp"},{"id":"hot","label":"ร้อน","price":-10,"group":"temp"},{"id":"blend","label":"ปั่น","price":5,"group":"temp"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"normal","label":"หวานปกติ","price":0,"group":"sweet"}]'::jsonb),
(15, 'เครื่องดื่ม', 'ชาไทย', 40, 'thai_tea', NULL, 'ชาไทยหอมนมสด | ร้อน 30฿', '[{"id":"cold","label":"เย็น","price":0,"group":"temp"},{"id":"hot","label":"ร้อน","price":-10,"group":"temp"},{"id":"blend","label":"ปั่น","price":5,"group":"temp"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"normal","label":"หวานปกติ","price":0,"group":"sweet"}]'::jsonb),
(16, 'เครื่องดื่ม', 'ชาเขียว', 40, 'green_tea', NULL, 'ชาเขียวญี่ปุ่นนมสด | ร้อน 30฿', '[{"id":"cold","label":"เย็น","price":0,"group":"temp"},{"id":"hot","label":"ร้อน","price":-10,"group":"temp"},{"id":"blend","label":"ปั่น","price":5,"group":"temp"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"normal","label":"หวานปกติ","price":0,"group":"sweet"}]'::jsonb),
(17, 'เครื่องดื่ม', 'นมเย็น', 40, 'milk_cold', NULL, 'นมสดเย็นสดชื่น | ร้อน 30฿', '[{"id":"cold","label":"เย็น","price":0,"group":"temp"},{"id":"hot","label":"ร้อน","price":-10,"group":"temp"},{"id":"blend","label":"ปั่น","price":5,"group":"temp"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"normal","label":"หวานปกติ","price":0,"group":"sweet"}]'::jsonb),
(18, 'เครื่องดื่ม', 'โกโก้', 40, 'cocoa_new', NULL, 'โกโก้ครีมท็อป ช็อกโกแลตแท้ | ร้อน 30฿', '[{"id":"cold","label":"เย็น","price":0,"group":"temp"},{"id":"hot","label":"ร้อน","price":-10,"group":"temp"},{"id":"blend","label":"ปั่น","price":5,"group":"temp"},{"id":"nosweet","label":"ไม่หวาน","price":0,"group":"sweet"},{"id":"less","label":"หวานน้อย","price":0,"group":"sweet"},{"id":"normal","label":"หวานปกติ","price":0,"group":"sweet"}]'::jsonb),
(28, 'เครื่องดื่ม', 'น้ำอัดลม', 15, 'soda', NULL, 'น้ำอัดลม (โค้ก/เป๊ปซี่/สไปรท์)', '[]'::jsonb)
ON CONFLICT (id) DO UPDATE SET
  cat=EXCLUDED.cat, name=EXCLUDED.name, price=EXCLUDED.price,
  img=EXCLUDED.img, badge=EXCLUDED.badge, description=EXCLUDED.description,
  opts=EXCLUDED.opts;
