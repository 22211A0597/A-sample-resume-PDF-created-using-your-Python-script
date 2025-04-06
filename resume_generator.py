import argparse
import requests
from fpdf import FPDF 
def get_resume_data(name="Your Name"):
    api_url = f"https://expressjs-api-resume-random.onrender.com/resume?name={name}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None
def generate_resume_pdf(data, output_path="resume.pdf", font_size=12, font_color="#000000", bg_color="#FFFFFF"):
    pdf = FPDF()  
    pdf.add_page()
    pdf.set_font("Arial", size=font_size)
    pdf.set_fill_color(int(bg_color[1:3], 16), int(bg_color[3:5], 16), int(bg_color[5:7], 16))
    pdf.rect(0, 0, 210, 297, 'F')  # A4 size

    # Set text color
    pdf.set_text_color(int(font_color[1:3], 16), int(font_color[3:5], 16), int(font_color[5:7], 16))

    if not data:
        return 
    # Basic Info
    pdf.cell(0, 10, f"{data.get('name', 'Henrietta Mitchell')}", ln=1, align='C')
    pdf.cell(0, 10, f"{data.get('contact', {}).get('phone', '+123-456-7890')} - {data.get('contact', {}).get('email', 'hello@reallygreatsite.com')} - {data.get('contact', {}).get('website', '@reallygreatsite')}", ln=1, align='C')
    pdf.cell(0, 10, f"{data.get('contact', {}).get('address', '123 Anywhere St., Any City, ST 12345')}", ln=1, align='C')
    # Summary
    pdf.ln(10)
    pdf.cell(0, 10, "BUSINESS MANAGEMENT & ANALYSIS", ln=1)
    pdf.multi_cell(0, 5, data.get('summary', "Motivated and results-driven Business School graduate seeking a challenging position within a large organisation as a Business Analyst or Project Manager. Offering a strong foundation in business strategy, data analysis, and project management, with a proven ability to drive efficiency, deliver successful outcomes and collaborate within cross-functional teams."))
    # Skills
    pdf.ln(10)
    pdf.cell(0, 10, "KEY COMPETENCIES", ln=1)
    skills = data.get('skills', ["Process improvement", "Data-driven strategic planning", "Cost-benefit analysis", "Report writing and presenting", "Critical thinking skills", "Excellent communication skills", "Strong interpersonal skills", "Proactive and self-motivated", "Exceptional organisational skills"])
    for skill in skills:
        pdf.cell(0, 5, f"- {skill}", ln=1)
    # Experience
    pdf.ln(10)
    pdf.cell(0, 10, "PROFESSIONAL EXPERIENCE", ln=1)
    experiences = data.get('experience', [
        {
            'company': 'Arowwai Industries',
            'position': 'Business Analyst Intern',
            'startDate': 'Oct 2023',
            'endDate': 'Present',
            'description': "Developed and implemented a streamlined process for gathering business requirements, reducing project delivery time by 15%. Developed and implemented a standardised reporting framework, resulting in improved visibility of key performance metrics and enabling data-driven decision-making at all levels of the organisation."
        },
        {
            'company': 'Hanover and Tyke',
            'position': 'Project Management Assistant',
            'startDate': 'Jan 2022',
            'endDate': 'Aug 2023',
            'description': "Assisted project managers in planning and executing various projects, ensuring adherence to project timelines and deliverables. Monitored project budgets, tracked expenses, and prepared financial reports to ensure cost-effectiveness and adherence to financial guidelines."
        }
    ])
    for exp in experiences:
        pdf.cell(0, 10, f"{exp.get('company', '')}", ln=0)
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
    resume_data = {
        "name": "Henrietta Mitchell",
        "contact": {
            "phone": "+123-456-7890",
            "email": "hello@reallygreatsite.com",
            "website": "@reallygreatsite",
            "address": "123 Anywhere St., Any City, ST 12345"
        },
        "summary": "Motivated and results-driven Business School graduate seeking a challenging position within a large organisation as a Business Analyst or Project Manager. Offering a strong foundation in business strategy, data analysis, and project management, with a proven ability to drive efficiency, deliver successful outcomes and collaborate within cross-functional teams.",
        "skills": [
            "Process improvement",
            "Data-driven strategic planning",
            "Cost-benefit analysis",
            "Report writing and presenting",
            "Critical thinking skills",
            "Excellent communication skills",
            "Strong interpersonal skills",
            "Proactive and self-motivated",
            "Exceptional organisational skills"
        ],
        "experience": [
            {
                "company": "Arowwai Industries",
                "position": "Business Analyst Intern",
                "startDate": "Oct 2023",
                "endDate": "Present",
                "description": "Developed and implemented a streamlined process for gathering business requirements, reducing project delivery time by 15%. Developed and implemented a standardised reporting framework, resulting in improved visibility of key performance metrics and enabling data-driven decision-making at all levels of the organisation."
            },
            {
                "company": "Hanover and Tyke",
                "position": "Project Management Assistant",
                "startDate": "Jan 2022",
                "endDate": "Aug 2023",
                "description": "Assisted project managers in planning and executing various projects, ensuring adherence to project timelines and deliverables. Monitored project budgets, tracked expenses, and prepared financial reports to ensure cost-effectiveness and adherence to financial guidelines."
            }
        ]
    }

    generate_resume_pdf(resume_data, args.output, args.font_size, args.font_color, args.background_color)
    
