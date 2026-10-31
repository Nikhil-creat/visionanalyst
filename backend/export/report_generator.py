import io
import json


def to_json(df, summary: str) -> bytes:
    return json.dumps({"summary": summary, "data": json.loads(df.to_json(orient="records"))}, indent=2).encode()


def to_excel(df) -> bytes:
    b = io.BytesIO()
    df.to_excel(b, index=False, sheet_name="Insights")
    return b.getvalue()


def to_pdf(title: str, summary: str, df) -> bytes:
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table
    b, s = io.BytesIO(), getSampleStyleSheet()
    rows = [list(df.columns)] + df.head(20).astype(str).values.tolist()
    SimpleDocTemplate(b).build([Paragraph(title, s["Title"]), Paragraph(summary, s["BodyText"]), Spacer(1, 12), Table(rows)])
    return b.getvalue()


def to_pptx(title: str, summary: str, df) -> bytes:
    from pptx import Presentation
    p = Presentation()
    s = p.slides.add_slide(p.slide_layouts[1])
    s.shapes.title.text = title
    s.placeholders[1].text = summary
    s2 = p.slides.add_slide(p.slide_layouts[5])
    s2.shapes.title.text = "Data"
    t = s2.shapes.add_table(min(len(df), 8) + 1, len(df.columns), 0, 1500000, 9000000, 3000000).table
    for j, c in enumerate(df.columns):
        t.cell(0, j).text = str(c)
        for i in range(min(len(df), 8)):
            t.cell(i + 1, j).text = str(df.iloc[i, j])
    b = io.BytesIO()
    p.save(b)
    return b.getvalue()
