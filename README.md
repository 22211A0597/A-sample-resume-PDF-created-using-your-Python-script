import argparse
import requests
from fpdf import FPDF  
def get_resume_data(name="Your Name"):
    """Fetches resume data from the provided API."""
    api_url = f"https://expressjs-api-resume-random.onrender.com/resume?name={name}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None


def generate_resume_pdf(data, output_path="resume.pdf", font_size=12, font_color="#000000", bg_color="#FFFFFF"):
    """Generates a resume PDF with the given data and customization options."""

    pdf = FPDF() 
    pdf.add_page()
    pdf.set_font("Arial", size=font_size)
    pdf.set_fill_color(int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16))
    pdf.rect(0, 0, 210, 297, 'F')  
    pdf.set_text_color(int(font_color[1:3], 16), int(font_color[3:5], 16), int(font_color[5:7], 16))

    if data:
        # Basic Info
        pdf.cell(0, 10, f"{data.get('name', '')}", ln=1, align='C')
        contact = data.get('contact', {})
        pdf.cell(0, 10, f"{contact.get('phone', '')} - {contact.get('email', '')} - {contact.get('website', '')}", ln=1, align='C')
        pdf.cell(0, 10, f"{contact.get('address', '')}", ln=1, align='C')

        # Summary
        pdf.ln(10)
        pdf.cell(0, 10, "SUMMARY", ln=1)
        pdf.multi_cell(0, 5, data.get('summary', ''))

        # Skills
        pdf.ln(10)
        pdf.cell(0, 10, "KEY COMPETENCIES", ln=1)
        for skill in data.get('skills', []):
            pdf.cell(0, 5, f"- {skill}", ln=1)

        # Experience
        pdf.ln(10)
        pdf.cell(0, 10, "PROFESSIONAL EXPERIENCE", ln=1)
        for exp in data.get('experience', []):
            pdf.cell(0, 10, f"{exp.get('company', '')}", ln=1)
            pdf.cell(0, 10, f"{exp.get('position', '')}", align='R', ln=1)
            pdf.cell(0, 5, f"{exp.get('startDate', '')} - {exp.get('endDate', '')}", ln=1)
            pdf.multi_cell(0, 5, exp.get('description', ''))
            pdf.ln(5)

    pdf.output(output_path)
    print(f"Resume generated at {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a customized resume PDF.")
    parser.add_argument("--font-size", type=int, default=12, help="Font size for the resume.")
    parser.add_argument("--font-color", type=str, default="#000000", help="Font color (hex code).")
    parser.add_argument("--background-color", type=str, default="#FFFFFF", help="Background color (hex code).")
    parser.add_argument("--output", type=str, default="resume.pdf", help="Output path for the PDF file.")

    args = parser.parse_args()

    resume_data = get_resume_data()
    if resume_data:
        generate_resume_pdf(resume_data, args.output, args.font_size, args.font_color, args.background_color)
    else:
        print("Failed to generate resume.")
