from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .prompt import AIPrompt
from .models import Details
from openai import OpenAI
from . import db
import smtplib
from io import BytesIO
from reportlab.lib.pagesizes import letter
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
from .config import Config

views = Blueprint('views', __name__)

class AITesting:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.GPT_MODEL = "gpt-4o-mini"
        
    def get_response(self, prompt):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.GPT_MODEL,
                temperature=0.7
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"there is a problem getting the answer: {str(e)}")
            return "Entschuldigung, bei der Bearbeitung Ihrer Anfrage ist ein Fehler aufgetreten."

ai_assistant = AITesting()

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/api/ai', methods=['POST'])
@login_required
def ai():
    try:
        data = request.get_json()
        form_data = data.get('formData', {})
        is_complete = data.get('isComplete', False)

        if not form_data:
            return jsonify({'error': 'Form data is required'}), 400

        prompt = AIPrompt.HEALTH_ASSESSMENT.format(
            name=form_data.get('Name', 'Keine'),
            pflegegrad=form_data.get('Pflegegrad', 'Keine'),
            mobilität=form_data.get('Mobilität', 'Keine'),
            einschränkungen=form_data.get('Einschränkungen', 'Keine'),
            hilfsmittel=form_data.get('Hilfsmittel', 'Keine'),
            geräte=form_data.get('Geräte', 'Keine'),
            treppen=form_data.get('Treppen', 'Keine'),
            stürze=form_data.get('Stürze', 'Keine'),
            kommunikation=form_data.get('Kommunikation', 'Keine'),
            schlaf=form_data.get('Schlaf', 'Keine'),
            schlafprobleme=form_data.get('Schlafprobleme', 'Keine'),
            unterstützung=form_data.get('Unterstützung', 'Keine'),
            atmung=form_data.get('Atmung', 'Keine'),
            vergessen=form_data.get('Vergessen', 'Keine'),
            hobbys=form_data.get('Hobbys', 'Keine'),
            weitere_infos=form_data.get('WeitereInfos', 'Keine')
        )

        existing_detail = Details.query.filter_by(user_id=current_user.id, is_complete=False).first()

        response = ai_assistant.get_response(prompt)

        if existing_detail:
            existing_detail.prompt = prompt
            existing_detail.form_data = form_data
            existing_detail.is_complete = is_complete
            existing_detail.saved_choices = form_data
            existing_detail.response = response
            db.session.commit()
        else:
            new_details = Details(
                prompt=prompt,
                form_data=form_data,
                user_id=current_user.id,
                is_complete=is_complete,
                saved_choices=form_data,
                response=response
            )
            db.session.add(new_details)
            db.session.commit()

        return jsonify({'success': True, 'isComplete': is_complete, 'response': response})

    except Exception as e:
        print(f"Error in route: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@views.route('/api/saved-choices', methods=['GET'])
@login_required
def get_saved_choices():
    saved_detail = Details.query.filter_by(user_id=current_user.id, is_complete=False).first()
    if saved_detail and saved_detail.saved_choices:
        return jsonify({'savedChoices': saved_detail.saved_choices})
    return jsonify({'savedChoices': {}})

def generate_pdf(details):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    content_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceBefore=6,
        spaceAfter=6
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=14,
        leading=16,
        textColor=colors.HexColor('#2b5797'),
        spaceBefore=12,
        spaceAfter=6
    )

    content = []
    
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.gray,
        alignment=1 
    )
    
    disclaimer_text = """
    HAFTUNGSAUSSCHLUSS: Dieser Bericht wurde mit Hilfe von KI erstellt und sollte nicht als professionelle medizinische Beratung angesehen werden. 
    Bitte wenden Sie sich bei medizinischen Entscheidungen an qualifiziertes medizinisches Fachpersonal.
    """
    
    content.append(Paragraph(disclaimer_text, disclaimer_style))
    content.append(Spacer(1, 10))

    title = Paragraph("Pflegeassistenz Report", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 15))
    
    date_string = datetime.now().strftime("%B %d, %Y")
    date = Paragraph(f"Erzeugt am: {date_string}", content_style)
    content.append(date)
    content.append(Spacer(1, 10))
    
    content.append(Paragraph("KI Analyse und Empfehlungen:", header_style))
    if details.response:
        paragraphs = details.response.split('\n')
        for para in paragraphs:
            if para.strip():
                content.append(Paragraph(para, content_style))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Formular Antworten:", header_style))
    if isinstance(details.saved_choices, dict):
        for key, value in details.saved_choices.items():
            formatted_text = f"<b>{key}:</b> {value}"
            content.append(Paragraph(formatted_text, content_style))
    else:
        content.append(Paragraph(str(details.saved_choices), content_style))
        content.append(Spacer(1, 12))

    doc.build(content)
    pdf_buffer.seek(0)
    return pdf_buffer

@views.route('/send_pdf', methods=['POST'])
@login_required
def send_pdf():
    try:
        details = Details.query.filter_by(user_id=current_user.id).order_by(Details.date.desc()).first()
        if not details:
            return jsonify({'error': 'Keine Details gefunden'}), 404

        pdf_buffer = generate_pdf(details)

        smtp_server = 'smtp.gmail.com'
        smtp_port = 465
        smtp_username = Config.MAIL_USERNAME
        smtp_password = Config.MAIL_PASSWORD
        subject = "Ihr medizinischer Analysebericht"
        to_email = current_user.email

        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = to_email
        message['Subject'] = subject
        
        email_body = """
        Sehr geehrter Benutzer,

        im Anhang finden Sie Ihren medizinischen Analysebericht im PDF-Format.
        
        Bitte beachten Sie, dass es sich um einen automatisch erstellten Bericht handelt, der auf den von Ihnen angegebenen Informationen basiert.
        Für eine medizinische Beratung wenden Sie sich bitte an qualifiziertes medizinisches Fachpersonal.

        Mit freundlichen Grüßen,
        HealthAI-Team
        """
        message.attach(MIMEText(email_body, "plain"))

        pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
        pdf_attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=f"Medizinische_Analyse_Bericht_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        message.attach(pdf_attachment)

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(smtp_username, to_email, message.as_string())
            
        return jsonify({'message': 'PDF erfolgreich gesendet!'})
        
    except Exception as e:
        print(f"Fehler beim Erzeugen/Senden von PDF: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@views.route('/impressum', methods=['GET'])
def impressum():
    return render_template("Impressum.html")

@views.route('/datenschutz', methods=['GET'])
def datenschutz():
    return render_template("datenschutz.html")