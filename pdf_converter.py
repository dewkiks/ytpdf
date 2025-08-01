import io
import re
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor, blue, darkgreen, red
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def format_text(text: str) -> str:
    """Applies bold, italic, and inline code formatting using HTML tags."""
    # Process bold first (**text**)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    # Process italics (*text*), avoiding collision with bold
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    # Process inline code (`code`)
    text = re.sub(
        r"`([^`]+)`", r'<font name="Courier" color="#C7254E">\1</font>', text
    )
    return text


def convert_notes_to_pdf(
    markdown_content: str,
    video_title: str = "Educational Notes",
    video_url: str = "",
) -> bytes:
    """
    Converts a markdown string into a PDF file in memory and returns its bytes.
    """
    # Create an in-memory buffer to hold the PDF data
    buffer = io.BytesIO()

    # Create the PDF document template using the buffer
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.2 * inch,
        rightMargin=0.2 * inch,
        topMargin=0.2 * inch,
        bottomMargin=0.2 * inch,
    )

    # --- Define Styles ---
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CustomHeading2",
            parent=styles["Heading2"],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=18,
            textColor=darkgreen,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CustomHeading3",
            parent=styles["Heading3"],
            fontSize=14,
            spaceAfter=10,
            spaceBefore=14,
            textColor=blue,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CustomHeading4",
            parent=styles["Heading4"],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=12,
            textColor=darkgreen,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletPoint",
            parent=styles["Normal"],
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DiagramAlert",
            parent=styles["Normal"],
            textColor=red,
            fontSize=10,
            leftIndent=20,
            spaceAfter=6,
            spaceBefore=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeBlock",
            parent=styles["Normal"],
            fontName="Courier",
            fontSize=9,
            leading=12,
            leftIndent=20,
            rightIndent=20,
            spaceBefore=6,
            spaceAfter=6,
            textColor=HexColor("#333333"),
            backColor=HexColor("#F5F5F5"),
            borderPadding=(5, 5, 5, 5),
            borderColor=HexColor("#CCCCCC"),
            borderWidth=0.5,
        )
    )

    # --- Build PDF Story ---
    story = []

    # Title section
    story.append(Paragraph(video_title, styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"],
        )
    )
    if video_url:
        story.append(
            Paragraph(
                f"Source: <a href='{video_url}' color='blue'>{video_url}</a>",
                styles["Normal"],
            )
        )
    story.append(Spacer(1, 20))

    # --- Parse Markdown Content ---
    lines = markdown_content.split("\n")
    i = 0
    in_code_block = False
    code_buffer = []

    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()

        # Handle fenced code blocks
        if stripped_line.startswith("```"):
            if not in_code_block:
                in_code_block = True
            else:
                in_code_block = False
                code_text = escape("\n".join(code_buffer))
                story.append(
                    Paragraph(code_text.replace("\n", "<br/>"), styles["CodeBlock"])
                )
                code_buffer = []
            i += 1
            continue

        if in_code_block:
            code_buffer.append(line)
            i += 1
            continue

        # Handle other markdown elements
        if not stripped_line:
            story.append(Spacer(1, 6))
        elif stripped_line.startswith("## "):
            story.append(
                Paragraph(format_text(stripped_line[3:]), styles["CustomHeading2"])
            )
        elif stripped_line.startswith("### "):
            story.append(
                Paragraph(format_text(stripped_line[4:]), styles["CustomHeading3"])
            )
        elif stripped_line.startswith("#### "):
            story.append(
                Paragraph(format_text(stripped_line[5:]), styles["CustomHeading4"])
            )
        elif "DIAGRAM ALERT" in stripped_line:
            clean_line = stripped_line.replace("📊 **[DIAGRAM ALERT]**:", "").strip()
            story.append(
                Paragraph(f"📊 <b>DIAGRAM:</b> {clean_line}", styles["DiagramAlert"])
            )
        elif stripped_line.startswith("* "):
            bullet_text = stripped_line[2:]
            story.append(
                Paragraph(f"• {format_text(bullet_text)}", styles["BulletPoint"])
            )
        else:
            story.append(Paragraph(format_text(stripped_line), styles["Normal"]))

        i += 1

    # Build the PDF in the memory buffer
    doc.build(story)

    # Get the byte value of the PDF and close the buffer
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes