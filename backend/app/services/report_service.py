from __future__ import annotations

from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.config import settings


class ReportService:
    def __init__(self) -> None:
        self.base_dir = Path(settings.storage_dir) / "reports"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf(self, report_data: dict) -> Path:
        file_path = self.base_dir / f"report_{report_data['interview_id']}.pdf"
        document = SimpleDocTemplate(str(file_path), pagesize=A4)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="TitleCustom", parent=styles["Title"], textColor=colors.HexColor("#0f172a")))
        story = [
            Paragraph("AI Interviewer 5.0 - Interview Report", styles["TitleCustom"]),
            Spacer(1, 12),
            Paragraph(f"Candidate: {report_data.get('candidate_name', 'Candidate')}", styles["Normal"]),
            Paragraph(f"Company: {report_data.get('company', 'N/A')}", styles["Normal"]),
            Paragraph(f"Date: {report_data.get('created_at', datetime.utcnow()).strftime('%Y-%m-%d')}", styles["Normal"]),
            Spacer(1, 12),
        ]
        summary_table = Table(
            [
                ["Technical Score", report_data.get("technical_score", 0)],
                ["Communication Score", report_data.get("communication_score", 0)],
                ["Strong Areas", ", ".join(report_data.get("strong_areas", []))],
                ["Weak Areas", ", ".join(report_data.get("weak_areas", []))],
                ["Recommendations", ", ".join(report_data.get("recommendations", []))],
            ],
            colWidths=[160, 320],
        )
        summary_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e2e8f0")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("PADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(summary_table)
        story.append(Spacer(1, 16))
        story.append(Paragraph("Feedback", styles["Heading2"]))
        story.append(Paragraph(report_data.get("feedback", "No feedback available."), styles["BodyText"]))
        document.build(story)
        return file_path


report_service = ReportService()
