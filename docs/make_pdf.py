"""
Convert E-book HTML files to PDF with proper Thai font rendering.
Injects local fonts as base64, fixes CSS for weasyprint.
"""
import base64, os, re, warnings
warnings.filterwarnings("ignore")

DOCS = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = "/tmp/fonts"

def b64font(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Embed fonts as base64 so weasyprint doesn't need internet
FONT_CSS = f"""
@font-face {{
  font-family: 'Sarabun';
  font-weight: 400;
  src: url('data:font/truetype;base64,{b64font(f"{FONTS_DIR}/Sarabun-Regular.ttf")}') format('truetype');
}}
@font-face {{
  font-family: 'Sarabun';
  font-weight: 500;
  src: url('data:font/truetype;base64,{b64font(f"{FONTS_DIR}/Sarabun-Bold.ttf")}') format('truetype');
}}
@font-face {{
  font-family: 'Sarabun';
  font-weight: 600;
  src: url('data:font/truetype;base64,{b64font(f"{FONTS_DIR}/Sarabun-Bold.ttf")}') format('truetype');
}}
@font-face {{
  font-family: 'Sarabun';
  font-weight: 700;
  src: url('data:font/truetype;base64,{b64font(f"{FONTS_DIR}/Sarabun-Bold.ttf")}') format('truetype');
}}
@font-face {{
  font-family: 'Sarabun';
  font-weight: 800;
  src: url('data:font/truetype;base64,{b64font(f"{FONTS_DIR}/Sarabun-Bold.ttf")}') format('truetype');
}}
@font-face {{
  font-family: 'Noto Serif Thai';
  font-weight: 700;
  src: url('data:font/truetype;base64,{b64font(f"{FONTS_DIR}/NotoSerifThai-Bold.ttf")}') format('truetype');
}}
@font-face {{
  font-family: 'Noto Serif Thai';
  font-weight: 900;
  src: url('data:font/truetype;base64,{b64font(f"{FONTS_DIR}/NotoSerifThai-Bold.ttf")}') format('truetype');
}}
"""

# PDF-specific CSS overrides — fix weasyprint issues
PDF_OVERRIDES = """
/* PDF overrides */
@page {
  size: A4;
  margin: 0;
}

/* Remove absolute-positioned decorative elements that break PDF layout */
.cover-c1, .cover-c2,
.ch-open::after, .ch-open::before {
  display: none !important;
}

/* Replace ch-bg (big watermark number) — absolute pos causes overflow */
.ch-bg {
  display: none !important;
}

/* Fix 100vh — use fixed A4 height equivalent */
.cover, .toc, .thanks {
  min-height: 0 !important;
  height: auto !important;
  page-break-after: always;
}

/* Cover — compact for A4 */
.cover-body {
  padding: 60px 56px 48px !important;
}
.cover h1 {
  font-size: 40px !important;
  line-height: 1.4 !important;
}
.cover-icon {
  font-size: 60px !important;
  margin-bottom: 20px !important;
}

/* TOC */
.toc {
  padding: 64px 56px !important;
}

/* Chapter opener — compact */
.ch-open {
  padding: 48px 56px 44px !important;
  overflow: visible !important;
}
.ch-title {
  font-size: 34px !important;
}

/* Content */
.content {
  padding: 44px 56px 52px !important;
}

/* Page breaks */
.page-break, [class*="page-break"] {
  page-break-before: always !important;
  break-before: page !important;
}

/* Prevent tables/boxes from breaking mid-element */
.prep, .tip, .step, .card, .step-card, .warn, .note-box {
  page-break-inside: avoid !important;
  break-inside: avoid !important;
}

/* Emoji fallback sizing */
.cover-icon, .feat .em, .toc-n, .sn {
  font-size: inherit;
}

/* Remove link underlines */
a { text-decoration: none; color: inherit; }

/* Fix circular elements for PDF */
.toc-n, .sn {
  border-radius: 50% !important;
}
"""


def fix_html_for_pdf(html: str) -> str:
    # Remove Google Fonts link tags (we're embedding fonts instead)
    html = re.sub(r'<link[^>]*fonts\.googleapis[^>]*>', '', html)
    html = re.sub(r'<link[^>]*fonts\.gstatic[^>]*>', '', html)

    # Inject embedded fonts + PDF overrides right before </head>
    injection = f"<style>\n{FONT_CSS}\n{PDF_OVERRIDES}\n</style>"
    html = html.replace("</head>", injection + "\n</head>")

    return html


def convert(src_name, dst_name):
    src = os.path.join(DOCS, src_name)
    dst = os.path.join(DOCS, dst_name)

    with open(src, "r", encoding="utf-8") as f:
        html = f.read()

    html = fix_html_for_pdf(html)

    # Write patched HTML to temp file (weasyprint needs a base URL for relative assets)
    tmp = f"/tmp/pdf_tmp_{src_name}"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Converting {src_name} -> {dst_name} ...")
    import weasyprint
    weasyprint.HTML(filename=tmp).write_pdf(dst)
    size = os.path.getsize(dst) // 1024
    print(f"  Done: {size} KB")
    os.remove(tmp)


if __name__ == "__main__":
    convert("guide-basic.html",    "ebook-basic.pdf")
    convert("guide-standard.html", "ebook-standard.pdf")
    convert("guide-premium.html",  "ebook-premium.pdf")
    print("\nAll PDFs done!")
