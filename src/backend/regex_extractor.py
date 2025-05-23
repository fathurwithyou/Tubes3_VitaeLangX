import re


class RegexExtractor:
    """
    Extracts specific information from CV text using Regular Expressions.
    """

    def __init__(self):
        pass

    def extract_summary(self, text: str) -> str:
        """Extracts a general summary/overview from the CV text."""
        match = re.search(
            r'(?i)(summary|profile|overview|about me|introduction)[:\n\s]*(.*?)(?:\n\n|\n[A-Z][a-zA-Z\s]+:|Skills:|Experience:|Education:|$)', text, re.DOTALL)
        if match:
            summary = match.group(2).strip()
            summary = re.sub(r'\s*\n\s*', ' ', summary)
            return summary[:500] + "..." if len(summary) > 500 else summary
        return "Summary not found."

    def extract_skills(self, text: str) -> list[str]:
        """Extracts a list of skills from the CV text."""

        match = re.search(
            r'(?i)(skills|technical skills|key skills|core competencies)[:\n\s]*(.*?)(?:\n\n|\n[A-Z][a-zA-Z\s]+:|Experience:|Education:|$)', text, re.DOTALL)
        if match:
            skills_raw = match.group(2).strip()

            skills = re.split(r'[,;\n\t\r-]\s*', skills_raw)
            skills = [s.strip() for s in skills if s.strip()]

            skills = [s for s in skills if len(s) > 2 and not s.isdigit()]
            return list(set(skills))
        return []

    def extract_job_history(self, text: str) -> list[dict]:
        """Extracts job history (e.g., dates, titles, descriptions)."""

        job_pattern = re.compile(
            r'(?i)(?:^|\n)\s*'
            r'([A-Z][a-zA-Z\s,&\.-]+)\s*(?:at|@)\s*([A-Z][a-zA-Z\s,&\.-]+)\s*\n'
            r'(\d{4}(?:-\d{2})?(?:\s*-\s*|\s*to\s*|Present)?(?:\s*\d{4}(?:-\d{2})?)?)\s*\n'
            r'(.*?)(?=\n[A-Z][a-zA-Z\s,&\.-]+(?:\s*at|@)|Education:|Skills:|$)',
            re.DOTALL | re.MULTILINE
        )
        job_history = []
        for match in job_pattern.finditer(text):
            title = match.group(1).strip()
            company = match.group(2).strip()
            dates = match.group(3).strip()
            description = match.group(4).strip()

            description = re.sub(r'\s*\n\s*', ' ', description)
            job_history.append({
                "title": title,
                "company": company,
                "dates": dates,
                "description": description
            })
        return job_history

    def extract_education(self, text: str) -> list[dict]:
        """Extracts education history (e.g., dates, university, degree)."""

        education_pattern = re.compile(
            r'(?i)(?:^|\n)\s*(education|academic background)[:\n\s]*\n'
            r'(.*?)(?=\n[A-Z][a-zA-Z\s]+:|Skills:|Experience:|$)',
            re.DOTALL
        )
        edu_section_match = education_pattern.search(text)

        education_entries = []
        if edu_section_match:
            edu_text = edu_section_match.group(2)

            entry_pattern = re.compile(
                r'([A-Z][a-zA-Z\s,&-]+)\s*,\s*([A-Z][a-zA-Z\s,&-]+)\s*\n'
                r'(\d{4}(?:-\d{2})?(?:\s*-\s*|\s*to\s*)?\s*\d{4})'
            )
            for match in entry_pattern.finditer(edu_text):
                degree = match.group(1).strip()
                university = match.group(2).strip()
                dates = match.group(3).strip()
                education_entries.append({
                    "degree": degree,
                    "university": university,
                    "dates": dates
                })
        return education_entries
