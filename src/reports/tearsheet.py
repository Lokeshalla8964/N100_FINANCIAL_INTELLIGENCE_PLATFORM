from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

doc = SimpleDocTemplate("sample_tearsheet.pdf")

styles = getSampleStyleSheet()

elements = []

elements.append(Paragraph("<b>Company Tearsheet</b>", styles["Title"]))
elements.append(Paragraph("Company: ABB", styles["Heading2"]))
elements.append(Paragraph("This is a sample financial tearsheet generated using ReportLab.", styles["BodyText"]))

doc.build(elements)

print("PDF Created Successfully!")