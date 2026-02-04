from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf(
    career,
    avg_score,
    duration,
    skills,
    user_scores,
    roadmap,
    final_verdict
):
    filename = f"{career}_AI_Career_Roadmap.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 50

    # ===============================
    # PAGE 1: ROADMAP OVERVIEW
    # ===============================
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"{career} – AI Career Roadmap")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Average Skill Score: {avg_score} / 10")
    y -= 20

    c.drawString(50, y, f"Recommended Duration: {duration} Months")
    y -= 30

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Skill Overview")
    y -= 20

    c.setFont("Helvetica", 10)
    for key, label in skills.items():
        c.drawString(60, y, f"{label}: {user_scores[key]}/10")
        y -= 14
        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

    # Roadmap pages
    for phase, details in roadmap.items():
        c.showPage()
        y = height - 50

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, phase)
        y -= 25

        c.setFont("Helvetica", 10)
        for category, items in details.items():
            c.drawString(60, y, f"{category}:")
            y -= 15
            for item in items:
                c.drawString(80, y, f"- {item}")
                y -= 14
                if y < 80:
                    c.showPage()
                    y = height - 50
                    c.setFont("Helvetica", 10)

    # ===============================
    # FINAL PAGE: AI CAREER VERDICT
    # ===============================
    c.showPage()
    y = height - 60

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "Final AI Career Verdict")
    y -= 40

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, f"Verdict Level: {final_verdict['level']}")
    y -= 25

    c.setFont("Helvetica", 11)
    verdict_text = final_verdict["text"].split("\n")

    for line in verdict_text:
        c.drawString(50, y, line)
        y -= 16
        if y < 80:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

    c.save()
    return filename
