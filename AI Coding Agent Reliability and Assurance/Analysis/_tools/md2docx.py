"""Convert an analysis Markdown file into a styled Word document.

Stage 1 (this script): build the .docx with python-docx. Each formula is
written as UnicodeMath text inside a bookmark (eq1, eq2, ...) and a JSON map
of the equations is written next to the output. Stage 2 (finalize_docx.ps1) opens the file in Word, turns the
placeholders into real Word equations, inserts the table of contents and
exports a PDF.

Usage: python md2docx.py input.md output.docx [--toc]
"""
import json
import re
import sys

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BODY_FONT = "Calibri"
BANGLA_FONT = "Nirmala UI"
CODE_FONT = "Consolas"
ACCENT = "1F4E79"
HEADER_FILL = "D9E2F3"
QUOTE_FILL = "EEF3FA"
CODE_FILL = "F4F4F4"
PAGE_TEXT_WIDTH_DXA = 9638  # A4 width minus 2 cm margins on each side

# ---------------------------------------------------------------- LaTeX -> UnicodeMath

SYMBOLS = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ϵ", "varepsilon": "ε",
    "zeta": "ζ", "eta": "η", "theta": "θ", "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ",
    "nu": "ν", "xi": "ξ", "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "phi": "ϕ",
    "varphi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω", "Gamma": "Γ", "Delta": "Δ",
    "Theta": "Θ", "Lambda": "Λ", "Pi": "Π", "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
    "cdot": "⋅", "times": "×", "div": "÷", "pm": "±", "land": "∧", "wedge": "∧", "lor": "∨",
    "vee": "∨", "neg": "¬", "forall": "∀", "exists": "∃", "in": "∈", "notin": "∉", "cup": "∪",
    "cap": "∩", "subseteq": "⊆", "subset": "⊂", "supseteq": "⊇", "neq": "≠", "ne": "≠",
    "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "ll": "≪", "gg": "≫", "approx": "≈",
    "sim": "∼", "equiv": "≡", "propto": "∝", "emptyset": "∅", "infty": "∞", "partial": "∂",
    "nabla": "∇", "oplus": "⊕", "otimes": "⊗", "to": "→", "rightarrow": "→", "leftarrow": "←",
    "Rightarrow": "⇒", "iff": "⇔", "prime": "′", "ldots": "…", "dots": "…", "cdots": "⋯",
    "langle": "⟨", "rangle": "⟩", "lfloor": "⌊", "rfloor": "⌋", "lceil": "⌈", "rceil": "⌉",
    # \mid becomes U+2223 so Word does not read it as an unmatched |...| delimiter
    "lvert": "|", "rvert": "|", "vert": "|", "mid": "∣", "star": "⋆", "circ": "∘",
    "top": "⊤", "bot": "⊥", "sum": "∑", "prod": "∏", "int": "∫",
}
NARY = {"∑", "∏", "∫"}
FUNCTIONS = {"ln", "log", "exp", "min", "max", "sin", "cos", "tan", "lim", "det", "sup", "inf"}
BLACKBOARD = {"R": "ℝ", "E": "𝔼", "N": "ℕ", "Z": "ℤ", "Q": "ℚ", "P": "ℙ", "1": "𝟙"}
CALLIGRAPHIC = {"L": "ℒ", "O": "𝒪", "D": "𝒟", "N": "𝒩", "F": "ℱ", "H": "ℋ"}
ACCENTS = {"hat": "̂", "bar": "̅", "tilde": "̃", "vec": "⃗", "dot": "̇"}
SPACES = {",": " ", ";": " ", ":": " ", "!": "", " ": " ",
          "quad": " ", "qquad": "  "}
SKIP = {"left", "right", "big", "Big", "bigg", "Bigg", "bigl", "bigr", "Bigl", "Bigr",
        "displaystyle", "limits", "nolimits"}


def _tokens(s):
    return re.findall(r"\\[A-Za-z]+|\\.|[^\\]", s)


class LatexToUnicodeMath:
    def __init__(self, src):
        self.t = _tokens(src)
        self.i = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self):
        tok = self.peek()
        self.i += 1
        return tok

    def raw_group(self):
        """Return the literal text of the next {...} group."""
        while self.peek() == " ":
            self.take()
        if self.peek() != "{":
            return self.take() or ""
        self.take()
        depth, out = 1, []
        while self.peek() is not None:
            tok = self.take()
            if tok == "{":
                depth += 1
            elif tok == "}":
                depth -= 1
                if depth == 0:
                    break
            out.append(tok)
        return "".join(out)

    def arg(self):
        """Convert the next argument: a {...} group or a single token."""
        while self.peek() == " ":
            self.take()
        if self.peek() == "{":
            self.take()
            return self.seq(stop="}")
        tok = self.take()
        return self.atom(tok) if tok else ""

    @staticmethod
    def wrap(x):
        return x if len(x) == 1 else "(" + x + ")"

    def scripts(self):
        out = ""
        while self.peek() in ("_", "^"):
            op = self.take()
            out += op + self.wrap(self.arg())
        return out

    def atom(self, tok):
        if not tok.startswith("\\"):
            return {"/": "∕", "'": "′", "~": " "}.get(tok, tok)
        name = tok[1:]
        if name in SPACES:
            return SPACES[name]
        if name in ("{", "}", "%", "#", "&", "_", "$"):
            return name
        if name == "|":
            return "‖"
        if name in SKIP:
            nxt = self.take()
            return "" if nxt in (".", None) else self.atom(nxt)
        if name in ("frac", "dfrac", "tfrac"):
            a, b = self.arg(), self.arg()
            return "(" + a + ")/(" + b + ")"
        if name == "binom":
            a, b = self.arg(), self.arg()
            return "(" + a + "¦" + b + ")"
        if name == "sqrt":
            return "√(" + self.arg() + ")"
        if name in ("text", "mathrm", "operatorname", "textbf", "mbox"):
            # a straight quote would end the UnicodeMath literal early
            # \_ inside text is a literal underscore; a real "_" would read as a
            # subscript to the build-up check, so use the look-alike U+02CD
            text = self.raw_group().replace("\\_", "_").replace("\\%", "%").replace("\\,", " ")
            return '"' + text.replace('"', "”").replace("_", "ˍ") + '"'
        if name == "mathbb":
            g = self.raw_group().strip()
            return BLACKBOARD.get(g, g)
        if name == "mathcal":
            g = self.raw_group().strip()
            return CALLIGRAPHIC.get(g, g)
        if name in ("mathbf", "boldsymbol", "mathit"):
            return self.arg()
        if name in ACCENTS:
            return self.wrap(self.arg()) + ACCENTS[name]
        if name == "arg":
            # bare "arg" + "max" makes Word's build-up swallow the text after
            # the equation; quoted "arg" stays upright and is safe
            return '"arg" '
        if name in FUNCTIONS:
            return name + self.scripts() + "⁡"
        if name == "begin":
            env = self.raw_group()
            body = self.seq(stop="\\end")
            self.raw_group()
            if env == "cases":
                return "{■(" + body + ")┤"
            return "■(" + body + ")"
        if name == "\\":
            return "@"
        if name in SYMBOLS:
            sym = SYMBOLS[name]
            if sym in NARY:
                return sym + self.scripts() + "▒"
            return sym
        print(f"  [warn] unknown LaTeX command \\{name}", file=sys.stderr)
        return name

    def seq(self, stop=None):
        out = []
        while self.peek() is not None:
            tok = self.peek()
            if tok == stop:
                self.take()
                break
            self.take()
            if tok == "{":
                out.append(self.seq(stop="}"))
            elif tok in ("_", "^"):
                script = self.arg()
                # a function name as a script (T_max) makes Word's build-up
                # swallow the following paragraph; quoted text stays upright
                if script in FUNCTIONS:
                    script = '"' + script + '"'
                out.append(tok + self.wrap(script))
                # In UnicodeMath "k_1(1-b)" pulls "(1-b)" into the subscript;
                # a space ends the script and is dropped on build-up.
                if self.peek() not in ("_", "^", " ", None, stop):
                    out.append(" ")
            elif tok in (" ", "\n", "\t"):
                if out and not out[-1].endswith(" "):
                    out.append(" ")
            else:
                out.append(self.atom(tok))
        return "".join(out).strip()


def latex_to_unicodemath(src):
    # an n-ary operator with no operand (a bare \sum_q in prose) cannot keep
    # its trailing operand marker
    return LatexToUnicodeMath(src.strip()).seq().rstrip("▒ ")


# ---------------------------------------------------------------- document helpers


def set_cell_fill(cell, hex_fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tc_pr.append(shd)


def set_paragraph_fill(paragraph, hex_fill):
    p_pr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    p_pr.append(shd)


def set_paragraph_border(paragraph, side, color, size=12, space=4):
    p_pr = paragraph._p.get_or_add_pPr()
    borders = p_pr.find(qn("w:pBdr"))
    if borders is None:
        borders = OxmlElement("w:pBdr")
        p_pr.append(borders)
    el = OxmlElement(f"w:{side}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(size))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    borders.append(el)


def set_run_fonts(rpr, ascii_font, cs_font):
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        fonts.attrib.pop(qn(attr), None)
    fonts.set(qn("w:ascii"), ascii_font)
    fonts.set(qn("w:hAnsi"), ascii_font)
    fonts.set(qn("w:cs"), cs_font)


def setup_styles(doc):
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.2

    spec = {
        "Title": (24, ACCENT), "Heading 1": (16, ACCENT), "Heading 2": (13, "2E74B5"),
        "Heading 3": (12, "2E74B5"),
    }
    for name, (size, color) in spec.items():
        st = styles[name]
        st.font.size = Pt(size)
        st.font.color.rgb = RGBColor.from_string(color)
        st.font.bold = True
    styles["Heading 1"].paragraph_format.space_before = Pt(18)
    styles["Heading 1"].paragraph_format.space_after = Pt(8)
    styles["Heading 2"].paragraph_format.space_before = Pt(12)

    # Bangla is a complex script in Word: it reads the w:cs font, so every style
    # gets an explicit Bangla-capable cs font instead of the theme fallback.
    for st in styles:
        if st.type != 1:  # paragraph styles only
            continue
        rpr = st.element.get_or_add_rPr()
        set_run_fonts(rpr, BODY_FONT, BANGLA_FONT)
    defaults = doc.styles.element.find(qn("w:docDefaults"))
    rpr_default = defaults.find(qn("w:rPrDefault")).find(qn("w:rPr"))
    set_run_fonts(rpr_default, BODY_FONT, BANGLA_FONT)
    lang = rpr_default.find(qn("w:lang"))
    if lang is None:
        lang = OxmlElement("w:lang")
        rpr_default.append(lang)
    lang.set(qn("w:bidi"), "bn-BD")


def mirror_complex_script_props(root):
    """Word only applies w:b / w:i / w:sz to complex scripts via bCs / iCs / szCs."""
    for rpr in root.iter(qn("w:rPr")):
        for base, cs in (("b", "bCs"), ("i", "iCs"), ("sz", "szCs")):
            el = rpr.find(qn(f"w:{base}"))
            if el is not None and rpr.find(qn(f"w:{cs}")) is None:
                twin = OxmlElement(f"w:{cs}")
                if el.get(qn("w:val")) is not None:
                    twin.set(qn("w:val"), el.get(qn("w:val")))
                el.addnext(twin)


def add_page_number_footer(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    p._p.append(fld)


def add_header_text(section, text):
    p = section.header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run(text)
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x7F, 0x7F, 0x7F)


# ---------------------------------------------------------------- markdown parsing

INLINE_RE = re.compile(
    r"(`[^`]+`)|(\$[^$]+\$)|(\*\*[^*]+\*\*)|(\*[^*\s][^*]*\*)|(\[[^\]]+\]\([^)]+\))"
)


class Builder:
    def __init__(self, toc):
        self.doc = Document()
        self.eqs = {}
        self.toc = toc
        self.toc_done = False
        self.first_h1 = True
        sec = self.doc.sections[0]
        sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(sec, side, Cm(2))
        setup_styles(self.doc)
        add_page_number_footer(sec)

    def eq(self, paragraph, latex, display):
        """Write the UnicodeMath text wrapped in a bookmark; Word builds it up later.

        A bookmark gives Word the exact extent of each equation even when it
        normalises characters, so neighbouring text is never pulled in.
        """
        n = len(self.eqs) + 1
        name = f"eq{n}"
        um = latex_to_unicodemath(latex)
        start = OxmlElement("w:bookmarkStart")
        start.set(qn("w:id"), str(n))
        start.set(qn("w:name"), name)
        paragraph._p.append(start)
        paragraph.add_run(um)
        end = OxmlElement("w:bookmarkEnd")
        end.set(qn("w:id"), str(n))
        paragraph._p.append(end)
        self.eqs[name] = {"um": um, "display": display, "latex": latex}

    def inline(self, paragraph, text, bold=False, size=None, color=None):
        pos = 0
        for m in INLINE_RE.finditer(text):
            if m.start() > pos:
                self._run(paragraph, text[pos:m.start()], bold=bold, size=size, color=color)
            tok = m.group(0)
            if m.group(1):
                r = self._run(paragraph, tok[1:-1], bold=bold, size=size, color=color)
                r.font.name = CODE_FONT
                r.font.color.rgb = RGBColor(0xC7, 0x25, 0x4E)
            elif m.group(2):
                self.eq(paragraph, tok[1:-1], display=False)
            elif m.group(3):
                self.inline(paragraph, tok[2:-2], bold=True, size=size, color=color)
            elif m.group(4):
                r = self._run(paragraph, tok[1:-1], bold=bold, size=size, color=color)
                r.italic = True
            else:
                label = re.match(r"\[([^\]]+)\]", tok).group(1)
                r = self._run(paragraph, label, bold=bold, size=size)
                r.font.color.rgb = RGBColor(0x05, 0x63, 0xC1)
                r.underline = True
            pos = m.end()
        if pos < len(text):
            self._run(paragraph, text[pos:], bold=bold, size=size, color=color)

    @staticmethod
    def _run(paragraph, text, bold=False, size=None, color=None):
        r = paragraph.add_run(text)
        if bold:
            r.bold = True
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        return r

    def maybe_toc(self):
        if not self.toc or self.toc_done:
            return
        self.toc_done = True
        p = self.doc.add_paragraph()
        self._run(p, "সূচিপত্র (Table of Contents)", bold=True, size=14, color=ACCENT)
        self.doc.add_paragraph("@@TOC@@")
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def heading(self, level, text):
        text = text.strip()
        if level == 1 and self.first_h1:
            self.first_h1 = False
            p = self.doc.add_paragraph(style="Title")
            self.inline(p, text)
            add_header_text(self.doc.sections[0], re.sub(r"[*`$]", "", text)[:90])
            return
        if level == 2:
            self.maybe_toc()
        style = {1: "Heading 1", 2: "Heading 1", 3: "Heading 2"}.get(level, "Heading 3")
        p = self.doc.add_paragraph(style=style)
        self.inline(p, text)

    def paragraph(self, text):
        p = self.doc.add_paragraph()
        self.inline(p, text)

    def display_math(self, latex):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self.eq(p, latex, display=True)

    def bullet(self, text, level):
        style = "List Bullet" if level == 0 else "List Bullet 2"
        p = self.doc.add_paragraph(style=style)
        p.paragraph_format.space_after = Pt(3)
        self.inline(p, text)

    def numbered(self, number, text, level):
        p = self.doc.add_paragraph()
        indent = 0.75 + 0.75 * level
        p.paragraph_format.left_indent = Cm(indent)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.space_after = Pt(3)
        self._run(p, f"{number}.\t", bold=True, color=ACCENT)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(indent))
        self.inline(p, text)

    def quote(self, lines):
        for line in lines:
            p = self.doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.4)
            p.paragraph_format.space_after = Pt(0)
            set_paragraph_fill(p, QUOTE_FILL)
            set_paragraph_border(p, "left", "2E74B5", size=24, space=8)
            self.inline(p, line)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(0)

    def code(self, lines, lang):
        for line in lines or [""]:
            p = self.doc.add_paragraph()
            pf = p.paragraph_format
            pf.space_after = Pt(0)
            pf.line_spacing = 1.0
            pf.left_indent = Cm(0.3)
            set_paragraph_fill(p, CODE_FILL)
            r = p.add_run(line if line else " ")
            r.font.name = CODE_FONT
            r.font.size = Pt(9.5)
            if lang == "diff" and line.startswith("+"):
                r.font.color.rgb = RGBColor(0x1E, 0x7B, 0x34)
            elif lang == "diff" and line.startswith("-"):
                r.font.color.rgb = RGBColor(0xB3, 0x1D, 0x28)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(0)

    def rule(self):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        set_paragraph_border(p, "bottom", "BFBFBF", size=6, space=1)

    def table(self, rows):
        header, body = rows[0], rows[1:]
        ncols = len(header)
        table = self.doc.add_table(rows=1 + len(body), cols=ncols)
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        # column widths proportional to content length, with a floor
        def width(text):
            text = re.sub(r"\$[^$]+\$", "xxxx", text)
            # emoji/symbols (stars, ticks) render about three characters wide
            return len(text) + sum(2 for ch in text if ord(ch) >= 0x2600)

        lengths = [max(width(r[c]) if c < len(r) else 0 for r in rows) for c in range(ncols)]
        # floor: never narrower than the header's longest word (e.g. "Status")
        floors = [max([len(w) for w in header[c].split()] + [4]) + 5 for c in range(ncols)]
        lengths = [min(max(l, f), 70) for l, f in zip(lengths, floors)]
        total = sum(lengths)
        widths = [int(PAGE_TEXT_WIDTH_DXA * l / total) for l in lengths]
        widths[-1] += PAGE_TEXT_WIDTH_DXA - sum(widths)
        grid = table._tbl.tblGrid
        for gc, w in zip(grid.findall(qn("w:gridCol")), widths):
            gc.set(qn("w:w"), str(w))
        for ri, row in enumerate([header] + body):
            for ci in range(ncols):
                cell = table.rows[ri].cells[ci]
                cell.width = Cm(widths[ci] / 567)
                text = row[ci] if ci < len(row) else ""
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.1
                if ri == 0:
                    set_cell_fill(cell, HEADER_FILL)
                    self.inline(p, text, bold=True, size=10)
                else:
                    self.inline(p, text, size=10)
        # repeat the header row on every page the table spans
        tr_pr = table.rows[0]._tr.get_or_add_trPr()
        hdr = OxmlElement("w:tblHeader")
        tr_pr.append(hdr)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)


def split_row(line):
    line = line.strip().strip("|")
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def convert(md_text, toc):
    b = Builder(toc)
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            lang = s[3:].strip()
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            b.code(block, lang)
            i += 1
            continue
        if s.startswith("$$"):
            if len(s) > 4 and s.endswith("$$"):
                b.display_math(s[2:-2])
                i += 1
                continue
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("$$"):
                block.append(lines[i])
                i += 1
            b.display_math("\n".join(block))
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            b.heading(len(m.group(1)), m.group(2))
            i += 1
            continue
        if re.fullmatch(r"-{3,}|\*{3,}", s):
            b.rule()
            i += 1
            continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            rows = [split_row(s)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            b.table(rows)
            continue
        if s.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            b.quote([x for x in block if x])
            continue
        indent = len(line) - len(line.lstrip(" "))
        level = 1 if indent >= 2 else 0
        m = re.match(r"^[-*]\s+(.*)$", s)
        if m:
            b.bullet(m.group(1), level)
            i += 1
            continue
        m = re.match(r"^(\d+)\.\s+(.*)$", s)
        if m:
            b.numbered(m.group(1), m.group(2), level)
            i += 1
            continue
        # plain paragraph: join soft-wrapped lines
        block = [s]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#|```|\$\$|\||>|[-*]\s|\d+\.\s|-{3,})", lines[i].strip()):
            block.append(lines[i].strip())
            i += 1
        b.paragraph(" ".join(block))
    mirror_complex_script_props(b.doc.element)
    mirror_complex_script_props(b.doc.styles.element)
    return b


def main():
    src, out = sys.argv[1], sys.argv[2]
    toc = "--toc" in sys.argv
    with open(src, encoding="utf-8") as f:
        b = convert(f.read(), toc)
    b.doc.save(out)
    with open(out + ".eq.json", "w", encoding="utf-8") as f:
        json.dump(b.eqs, f, ensure_ascii=False, indent=1)
    print(f"wrote {out} ({len(b.eqs)} equations)")


if __name__ == "__main__":
    main()
