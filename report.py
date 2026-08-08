import os

from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.enums import TA_CENTER


REPORT_FOLDER = "reports"


def generate_report(
    filename,
    score,
    matched,
    missing,
    suggestions,
    category_scores
):

    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )

    base_name = os.path.splitext(
        filename
    )[0]

    report_filename = (
        base_name
        + "_analysis_report.pdf"
    )

    report_path = os.path.join(
        REPORT_FOLDER,
        report_filename
    )


    document = SimpleDocTemplate(
        report_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22
    )


    score_style = ParagraphStyle(
        "ScoreStyle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=32
    )


    story = []


    story.append(
        Paragraph(
            "AI Resume Analyzer",
            title_style
        )
    )


    story.append(
        Spacer(1, 10)
    )


    story.append(
        Paragraph(
            "Resume Analysis Report",
            styles["Heading2"]
        )
    )


    story.append(
        Paragraph(
            f"Resume: {filename}",
            styles["Normal"]
        )
    )


    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            f"{score}%",
            score_style
        )
    )


    story.append(
        Paragraph(
            "Overall Job Match Score",
            styles["Heading2"]
        )
    )


    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            "Category Analysis",
            styles["Heading2"]
        )
    )


    category_data = [
        ["Category", "Score"],
        [
            "Technical Skills",
            f"{category_scores['technical']}%"
        ],
        [
            "Soft Skills",
            f"{category_scores['soft']}%"
        ]
    ]


    category_table = Table(
        category_data,
        colWidths=[250, 150]
    )


    category_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                1,
                colors.grey
            ),

            (
                "ALIGN",
                (1, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )
        ])
    )


    story.append(
        category_table
    )


    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            "Matched Skills",
            styles["Heading2"]
        )
    )


    if matched:

        for skill in matched:

            story.append(
                Paragraph(
                    "✓ " + skill,
                    styles["Normal"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No matching skills found.",
                styles["Normal"]
            )
        )


    story.append(
        Spacer(1, 15)
    )


    story.append(
        Paragraph(
            "Missing Skills",
            styles["Heading2"]
        )
    )


    if missing:

        for skill in missing:

            story.append(
                Paragraph(
                    "! " + skill,
                    styles["Normal"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No major missing skills detected.",
                styles["Normal"]
            )
        )


    story.append(
        Spacer(1, 15)
    )


    story.append(
        Paragraph(
            "Recommendations",
            styles["Heading2"]
        )
    )


    for suggestion in suggestions:

        story.append(
            Paragraph(
                "• " + suggestion,
                styles["Normal"]
            )
        )


    document.build(story)


    return report_filename