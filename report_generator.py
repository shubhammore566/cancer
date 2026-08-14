"""
report_generator.py
Builds a professional PDF diagnosis report using ReportLab.
"""
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable
)
from reportlab.lib.enums import TA_CENTER


def build_pdf_report(output_path, patient, diagnosis, ai_summary=""):
    """
    patient: sqlite3.Row or dict with name, age, gender, contact
    diagnosis: sqlite3.Row or dict with prediction, confidence, created_at,
               original_image_path, deblurred_image_path, gradcam_image_path
    """
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=18 * mm, bottomMargin=18 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCustom", parent=styles["Title"], fontSize=20, textColor=colors.HexColor("#0F4C5C"),
        alignment=TA_CENTER, spaceAfter=2,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"], fontSize=10, textColor=colors.HexColor("#5A5A5A"),
        alignment=TA_CENTER, spaceAfter=14,
    )
    heading_style = ParagraphStyle(
        "HeadingCustom", parent=styles["Heading2"], textColor=colors.HexColor("#0F4C5C"),
        spaceBefore=14, spaceAfter=6,
    )
    body_style = ParagraphStyle("BodyCustom", parent=styles["Normal"], fontSize=10.5, leading=15)
    disclaimer_style = ParagraphStyle(
        "Disclaimer", parent=styles["Normal"], fontSize=8.5, textColor=colors.HexColor("#8A8A8A"),
        alignment=TA_CENTER,
    )

    elements = []
    elements.append(Paragraph("Esophageal Screening Report", title_style))
    elements.append(Paragraph("AI-Assisted Endoscopic Image Analysis", subtitle_style))
    elements.append(HRFlowable(width="100%", color=colors.HexColor("#0F4C5C"), thickness=1.2))
    elements.append(Spacer(1, 10))

    def g(obj, key, default=""):
        try:
            return obj[key] if obj[key] is not None else default
        except Exception:
            return getattr(obj, key, default)

    patient_table_data = [
        ["Patient Name", g(patient, "name")],
        ["Age", str(g(patient, "age"))],
        ["Gender", g(patient, "gender")],
        ["Contact", g(patient, "contact")],
        ["Report Date", datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")],
    ]
    pt = Table(patient_table_data, colWidths=[45 * mm, 110 * mm])
    pt.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0F4C5C")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#E0E0E0")),
    ]))
    elements.append(Paragraph("Patient Information", heading_style))
    elements.append(pt)

    prediction = g(diagnosis, "prediction", "N/A")
    confidence = g(diagnosis, "confidence", 0)
    try:
        confidence_pct = f"{float(confidence) * 100:.2f}%"
    except Exception:
        confidence_pct = "N/A"

    result_color = colors.HexColor("#C0392B") if prediction == "Esophagitis" else colors.HexColor("#1E8449")
    result_table = Table(
        [["AI Screening Result", prediction], ["Model Confidence", confidence_pct],
         ["Analysis Date", str(g(diagnosis, "created_at"))[:19].replace("T", " ")]],
        colWidths=[45 * mm, 110 * mm],
    )
    result_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, 0), (1, 0), result_color),
        ("FONTNAME", (1, 0), (1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#E0E0E0")),
    ]))
    elements.append(Paragraph("AI Screening Result", heading_style))
    elements.append(result_table)

    # Images
    img_paths = [
        ("Original Image", g(diagnosis, "original_image_path")),
        ("Deblurred Image", g(diagnosis, "deblurred_image_path")),
        ("Grad-CAM Heatmap", g(diagnosis, "gradcam_image_path")),
    ]
    valid_imgs = [(label, p) for label, p in img_paths if p]
    if valid_imgs:
        elements.append(Paragraph("Image Analysis", heading_style))
        row_imgs, row_labels = [], []
        for label, path in valid_imgs:
            try:
                row_imgs.append(RLImage(path, width=52 * mm, height=52 * mm))
                row_labels.append(Paragraph(f"<para alignment='center'>{label}</para>", body_style))
            except Exception:
                continue
        if row_imgs:
            img_table = Table([row_imgs, row_labels], colWidths=[54 * mm] * len(row_imgs))
            img_table.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(img_table)

    if ai_summary:
        elements.append(Paragraph("AI Assistant Notes", heading_style))
        elements.append(Paragraph(ai_summary.replace("\n", "<br/>"), body_style))

    doctor_notes = g(diagnosis, "doctor_notes")
    if doctor_notes:
        elements.append(Paragraph("Doctor / Clinician Notes", heading_style))
        elements.append(Paragraph(doctor_notes.replace("\n", "<br/>"), body_style))

    elements.append(Spacer(1, 18))
    elements.append(HRFlowable(width="100%", color=colors.HexColor("#E0E0E0"), thickness=0.8))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "This report is generated by an AI-assisted screening tool for research/educational "
        "purposes. It is NOT a certified medical diagnosis. Please consult a licensed "
        "gastroenterologist or oncologist for clinical confirmation and treatment.",
        disclaimer_style,
    ))

    doc.build(elements)
    return output_path
