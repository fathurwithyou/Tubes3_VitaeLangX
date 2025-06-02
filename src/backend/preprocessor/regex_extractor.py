import re


class RegexExtractor:
    """
    Extracts specific information from CV text using Regular Expressions.
    The extraction process first splits the CV into logical sections
    (e.g., Summary, Experience, Skills) and then applies specific regex
    patterns within those sections for more accurate parsing.
    """

    def __init__(self):

        self.section_headers = [
            'Summary', 'Highlights', 'Experience', 'Education', 'Skills',
            'Certifications', 'Interests', 'Additional Information', 'Accomplishments',
            'Profile', 'Overview', 'About Me', 'Introduction', 'Technical Skills',
            'Key Skills', 'Core Competencies', 'Professional Experience',
            'Work Experience', 'Academic Background', 'Professional Development', 'Education and Training',
        ]

        self.section_pattern = re.compile(
            r'(?i)(?:^|\n)\s*(' + '|'.join(self.section_headers) + r')\s*:?\s*\n',
            re.MULTILINE
        )

    def _split_into_sections(self, text: str) -> dict:
        """
        Splits the CV text into a dictionary of sections based on predefined headers.
        Keys are standardized section names (e.g., 'Summary', 'Experience'),
        values are their extracted content.
        """
        sections = {}

        matches = list(self.section_pattern.finditer(text))

        if not matches:

            sections['Main'] = text
            return sections

        for i, match in enumerate(matches):
            header_name_found = match.group(1).strip()

            standardized_header = next(
                (h for h in self.section_headers if h.lower()
                 == header_name_found.lower()),
                header_name_found
            )

            start_index = match.end()

            end_index = matches[i+1].start() if i + \
                1 < len(matches) else len(text)

            content = text[start_index:end_index].strip()
            sections[standardized_header] = content
        return sections

    def extract_summary(self, text: str) -> str:
        """
        Extracts a general summary/overview from the CV text.
        It first splits the text into sections and then looks for the summary section.
        """
        sections = self._split_into_sections(text)

        summary_section_content = sections.get('Summary') or \
            sections.get('Profile') or \
            sections.get('Overview') or \
            sections.get('About Me') or \
            sections.get('Introduction')

        if summary_section_content:

            summary = re.sub(r'\s*\n\s*', ' ', summary_section_content).strip()

            return summary[:500] + "..." if len(summary) > 500 else summary
        return "Summary not found."

    def extract_skills(self, text: str) -> list[str]:
        """
        Extracts a list of skills from the CV text.
        It first splits the text into sections and then looks for the skills section.
        """
        sections = self._split_into_sections(text)

        skills_section_content = sections.get('Skills') or \
            sections.get('Technical Skills') or \
            sections.get('Key Skills') or \
            sections.get('Core Competencies')

        if skills_section_content:

            skills = re.split(r'[,;\n\t\r-]\s*', skills_section_content)

            skills = [s.strip() for s in skills if s.strip()]

            skills = [s for s in skills if len(s) > 2 and not s.isdigit()]
            return list(set(skills))
        return []

    def extract_job_history(self, text: str) -> list[dict]:
        """
        Extracts job history (e.g., dates, titles, locations, companies).
        It processes the experience section by splitting into blocks and
        extracting "general" job information from even-indexed blocks.
        """
        sections = self._split_into_sections(text)

        experience_section_content = sections.get('Experience') or \
            sections.get('Professional Experience') or \
            sections.get('Work Experience')

        job_history = []
        if experience_section_content:

            job_blocks = re.split(
                r'\n{2,}', experience_section_content.strip())

            for i in range(0, len(job_blocks), 2):
                general_info_block = job_blocks[i].strip()

                general_pattern = re.compile(
                    r'([A-Z][a-zA-Z\s,&\.-]+(?:\s*Intern)?)\s*\n'
                    r'([A-Z][a-zA-Z\s,&\.-]+)\s*,\s*'
                    r'([A-Z][a-zA-Z\s,&\.-]+)\s+'
                    r'([A-Z][a-zA-Z\s,&\.-]+)\s*/\s*'
                    r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s*to\s*(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}|Present))'
                )

                match = general_pattern.search(general_info_block)
                if match:
                    title = match.group(1).strip()
                    city = match.group(2).strip()
                    state = match.group(3).strip()
                    company = match.group(4).strip()
                    dates = match.group(5).strip()

                    description = ""
                    if i + 1 < len(job_blocks):
                        description = job_blocks[i+1].strip()

                        description = re.sub(
                            r'\s*\n\s*', ' ', description).strip()

                    job_history.append({
                        "title": title,
                        "company": company,
                        "location": f"{city}, {state}",
                        "dates": dates,
                        "description": description
                    })
        return job_history

    def extract_education(self, text: str) -> dict:
        """
        Extracts education history (e.g., dates, university, degree) and the full raw text of the education section.
        It first splits the text into sections and then processes the education section.
        Returns a dictionary containing 'entries' (list of dicts) and 'full_text' (str).
        """
        sections = self._split_into_sections(text)
    
        education_section_content = sections.get(
            'Education') or sections.get('Academic Background') or sections.get('Education and Training')

        education_entries = []
        if education_section_content:

            edu_lines = [
                line.strip() for line in education_section_content.split('\n')
                if line.strip() and not re.search(r'\b(wk|hrs|school|training|professional)\b', line, re.IGNORECASE)
            ]

            for line in edu_lines:
                university = None
                degree = None
                dates = None
                gpa = None

                match1 = re.search(
                    r'([A-Z][a-zA-Z\s,&\.-]+?)\s+(\d{4})\s+((?:Associate|Associates|Bachelors|Masters|PhD|Degree|Diploma):\s*[A-Z][a-zA-Z\s,&\.-]+)(?:.*GPA:\s*([\d\.]+))?',
                    line, re.IGNORECASE
                )
                if match1:
                    university = match1.group(1).strip()
                    dates = match1.group(2).strip()
                    degree = match1.group(3).strip()
                    gpa = match1.group(4).strip() if match1.group(4) else None
                else:

                    match2 = re.search(
                        r'(\d{4})\s+((?:Associate|Associates|Bachelors|Masters|PhD|Degree|Diploma):\s*[A-Z][a-zA-Z\s,&\.-]+?)\s+([A-Z][a-zA-Z\s,&\.-]+?)(?:.*GPA:\s*([\d\.]+))?',
                        line, re.IGNORECASE
                    )
                    if match2:
                        dates = match2.group(1).strip()
                        degree = match2.group(2).strip()
                        university = match2.group(3).strip()
                        gpa = match2.group(4).strip(
                        ) if match2.group(4) else None

                        if university and ('City, State' in university or 'USA' in university):

                            uni_match_in_line = re.search(
                                r'(Northern Maine Community College|Husson College)', line)
                            if uni_match_in_line:
                                university = uni_match_in_line.group(1)
                            else:
                                university = None
                    else:

                        match3 = re.search(
                            r'(?i)Attended\s+([A-Z][a-zA-Z\s,&\.-]+),\s*major\s+([A-Z][a-zA-Z\s,&\.-]+)(?:.*toward\s+([A-Z][a-zA-Z\s,&\.-]+))?',
                            line, re.IGNORECASE
                        )
                        if match3:
                            university = match3.group(1).strip()
                            major = match3.group(2).strip()
                            degree_type_suffix = match3.group(
                                3).strip() if match3.group(3) else ""
                            degree = f"{major} {degree_type_suffix}".strip()
                            dates = "Not specified"

                if university or degree:
                    education_entries.append({
                        "university": university,
                        "degree": degree,
                        "dates": dates,
                        "gpa": gpa
                    })
        # print(education_section_content)
        return {
            "entries": education_entries,
            "full_text": education_section_content if education_section_content else ""
        }
