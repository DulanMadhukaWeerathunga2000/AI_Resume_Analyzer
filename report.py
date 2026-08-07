from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    filename,
    score,
    matched,
    missing,
    suggestions
):

    output = f"reports/{filename}_report.pdf"

    document = SimpleDocTemplate(
        output,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Resume Analyzer Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Resume: {filename}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Match Score: {score}%",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "Matched Skills",
            styles["Heading2"]
        )
    )

    matched_items = []

    for skill in matched:

        matched_items.append(
            ListItem(
                Paragraph(skill, styles["Normal"])
            )
        )

    content.append(
        ListFlowable(
            matched_items,
            bulletType="bullet"
        )
    )


    content.append(
        Paragraph(
            "Missing Skills",
            styles["Heading2"]
        )
    )

    missing_items = []

    for skill in missing:

        missing_items.append(
            ListItem(
                Paragraph(skill, styles["Normal"])
            )
        )

    content.append(
        ListFlowable(
            missing_items,
            bulletType="bullet"
        )
    )


    content.append(
        Paragraph(
            "Suggestions",
            styles["Heading2"]
        )
    )

    for suggestion in suggestions:

        content.append(
            Paragraph(
                "• " + suggestion,
                styles["Normal"]
            )
        )

        content.append(Spacer(1, 5))


    document.build(content)

    return output