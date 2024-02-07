import pdfplumber
import spacy
import re

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    # Extract text from a PDF file using pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_entities(doc, label):
    # Extract entities of a specific label
    return [ent.text for ent in doc.ents if ent.label_ == label]

def extract_education(text):
    # Extract education information
    education_matches = re.finditer(r"\b(education|degree[s]?)\b", text, flags=re.IGNORECASE)
    education_start_positions = [match.end() for match in education_matches]
    
    education_entities = []
    for start_pos in education_start_positions:
        education_entities.append(text[start_pos:].split('\n', 1)[1].strip())
    
    return education_entities

def extract_skills(text):
    # Extract skills information
    skills_matches = re.finditer(r"\b(skills|technologies)\b", text, flags=re.IGNORECASE)
    skills_start_positions = [match.end() for match in skills_matches]
    
    skills_entities = []
    for start_pos in skills_start_positions:
        skills_entities.append(text[start_pos:].split('\n', 1)[1].strip())
    
    return skills_entities

def extract_experience(text):
    # Extract experience information
    experience_matches = re.finditer(r"\b(experience|work)\b", text, flags=re.IGNORECASE)
    experience_start_positions = [match.end() for match in experience_matches]
    
    experience_entities = []
    for start_pos in experience_start_positions:
        experience_entities.append(text[start_pos:].split('\n', 1)[1].strip())
    
    return experience_entities

def parse_resume_from_pdf(pdf_path):
    # Extract text from the PDF
    resume_text = extract_text_from_pdf(pdf_path)

    # Process the resume text with spaCy
    doc = nlp(resume_text)

    # Extract relevant information
    entities = {
        "Name": extract_entities(doc, "PERSON"),
        "Email": extract_entities(doc, "EMAIL"),
        "Phone": extract_entities(doc, "PHONE"),
        "Education": extract_education(resume_text),
        "Skills": extract_skills(resume_text),
        "Experience": extract_experience(resume_text)
    }

    return entities

# Example usage
pdf_path = "path/to/your/resume.pdf"
parsed_data = parse_resume_from_pdf(pdf_path)
print(parsed_data)
