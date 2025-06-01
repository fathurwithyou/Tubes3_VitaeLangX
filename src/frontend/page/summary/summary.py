# src/frontend/page/summary/summary.py
import customtkinter as ctk
from PIL import Image
import os
 
class SummaryPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager, applicant_id, cv_path=None, **kwargs): # Add cv_path
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0,
            **kwargs
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager
        self.applicant_id = applicant_id # For profile info
        self.cv_path_for_extraction = cv_path # For CV-specific extractions
        self.summary_data = None
        
        self.pack(fill="both", expand=True)
        self._load_data_and_setup_ui()

    def _load_data_and_setup_ui(self):
        if self.applicant_id is None:
            print("ERROR (SummaryPage): Applicant ID is None.")
            self._display_error_message("No applicant information available.")
            return

        # Get profile information using applicant_id
        profile_info = self.backend_manager._get_applicant_profile(self.applicant_id) #
        if not profile_info or "error" in profile_info:
            error_msg = profile_info.get("error", "Failed to load applicant profile.") if profile_info else "Failed to load applicant profile."
            print(f"ERROR (SummaryPage Profile): {error_msg}")
            self._display_error_message(error_msg)
            return
        
        cv_text_to_extract = ""
        path_used_for_extraction = ""

        # Determine which CV path to use for text extraction
        if self.cv_path_for_extraction and os.path.exists(self.cv_path_for_extraction): #
            print(f"SummaryPage: Using specific CV path for extraction: {self.cv_path_for_extraction}")
            path_used_for_extraction = self.cv_path_for_extraction
        elif self.applicant_id: # Fallback to deriving path from applicant_id
            print(f"SummaryPage: No specific CV path, deriving from applicant_id: {self.applicant_id}")
            derived_path = self.backend_manager.get_raw_cv_path(self.applicant_id) #
            if derived_path and os.path.exists(derived_path):
                path_used_for_extraction = derived_path
            else:
                print(f"SummaryPage: Could not derive a valid CV path for applicant_id {self.applicant_id}")
        
        if not path_used_for_extraction:
            self._display_error_message(f"No valid CV path found for applicant {self.applicant_id} for summary extraction.")
            return

        # Extract text from the determined CV path
        cv_text_to_extract = self.backend_manager.cv_processor.extract_text_from_pdf(path_used_for_extraction) #

        if not cv_text_to_extract or \
           ("Could not extract text" in cv_text_to_extract and not cv_text_to_extract.strip() == "Could not extract text from CV."):
            error_message_to_display = cv_text_to_extract if cv_text_to_extract else "CV content is empty or could not be extracted."
            self._display_error_message(f"Failed to extract text from CV ({os.path.basename(path_used_for_extraction)}): {error_message_to_display}")
            return

        # Perform regex extraction on the obtained text
        extracted_info = {
            "skills": self.backend_manager.regex_extractor.extract_skills(cv_text_to_extract), #
            "job_history": self.backend_manager.regex_extractor.extract_job_history(cv_text_to_extract), #
            "education": self.backend_manager.regex_extractor.extract_education(cv_text_to_extract) #
        }

        self.summary_data = {
            "applicant_profile": profile_info,
            "extracted_info": extracted_info
        }
        
        self.setup_summary_page()
        
    # ... (rest of SummaryPage methods: _display_error_message, setup_summary_page, create_back_button, create_header_section, create_personal_info_section, etc.)
    # Ensure these methods correctly use self.summary_data. The "Skill" header was already addressed previously.

    def _display_error_message(self, message): # Identical to CVPage
        for widget in self.winfo_children():
            widget.destroy()
        error_label = ctk.CTkLabel(self,text=message,font=ctk.CTkFont(size=18),text_color="tomato")
        error_label.pack(expand=True, padx=20, pady=20)
        back_button = ctk.CTkButton(self,text="← Back to Results",font=ctk.CTkFont(size=16),width=150,height=40,fg_color="#334D7A",hover_color="#273A5C",text_color="#DFCFC2",command=lambda: self.navigate_callback("result"))
        back_button.pack(pady=20)

    def setup_summary_page(self): # Identical to previous version
        for widget in self.winfo_children(): widget.destroy()
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=50, pady=30)
        self.create_back_button(main_container)
        self.create_header_section(main_container)
        self.create_summary_content(main_container)
    
    def create_back_button(self, parent): # Identical
        back_button = ctk.CTkButton(parent,text="←",font=ctk.CTkFont(size=20, weight="bold"),width=60,height=40,corner_radius=8,border_width=2,border_color="#DFCFC2", fg_color="#334D7A",hover_color="#1B2B4C", text_color="#DFCFC2",command=lambda: self.navigate_callback("result"))
        back_button.pack(anchor="nw", pady=(0, 15))
    
    def create_header_section(self, parent): # Identical
        header_container = ctk.CTkFrame(parent, fg_color="transparent")
        header_container.pack(fill="x", pady=(0, 20))
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
        header_content.pack(expand=True)
        center_content = ctk.CTkFrame(header_content, fg_color="transparent")
        center_content.pack(side="left", expand=True)
        profile = self.summary_data.get('applicant_profile', {})
        candidate_name = f"{profile.get('first_name', 'N/A')} {profile.get('last_name', '')}".strip()
        title_label = ctk.CTkLabel(center_content,text=f"Summary Report: {candidate_name}",font=ctk.CTkFont(size=32, weight="bold"),text_color="#DFCFC2")
        title_label.pack()
        description_label = ctk.CTkLabel(center_content,text="""Bearlock Holmes has highlighted what matters most. Use this snapshot to
assess compatibility at a glance.""",font=ctk.CTkFont(size=14),text_color="#FFFFFF",justify="center",wraplength=600)
        description_label.pack(pady=(8, 0))
    
    def create_summary_content(self, parent): # Identical
        scrollable_container = ctk.CTkScrollableFrame(parent,fg_color="transparent",corner_radius=0,scrollbar_button_color="#334D7A", scrollbar_button_hover_color="#4A5D8A")
        scrollable_container.pack(fill="both", expand=True)
        if not self.summary_data or "error" in self.summary_data: return
        self.create_personal_info_section(scrollable_container)
        self.create_skills_section(scrollable_container)
        self.create_job_history_section(scrollable_container)
        self.create_education_section(scrollable_container)
    
    def create_personal_info_section(self, parent): # Identical
        profile = self.summary_data.get('applicant_profile', {})
        candidate_name = f"{profile.get('first_name', 'N/A')} {profile.get('last_name', '')}".strip()
        info_card = ctk.CTkFrame(parent,fg_color="#DFCFC2",corner_radius=15,border_width=0)
        info_card.pack(fill="x", pady=(0, 20), padx=5)
        header_frame = ctk.CTkFrame(info_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_label = ctk.CTkLabel(header_frame,text=candidate_name,font=ctk.CTkFont(size=18, weight="bold"),text_color="#1B2B4C")
        header_label.pack(anchor="w", padx=20, pady=8)
        content_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        details = [f"Birthdate: {profile.get('date_of_birth', 'N/A')}", f"Address: {profile.get('address', 'N/A')}", f"Phone: {profile.get('phone_number', 'N/A')}"]
        for detail_text in details:
            detail_label = ctk.CTkLabel(content_frame,text=detail_text,font=ctk.CTkFont(size=14),text_color="#1B2B4C")
            detail_label.pack(anchor="w", pady=2)
    
    def create_skills_section(self, parent): # Header text "Skill" was previous change
        extracted_info = self.summary_data.get('extracted_info', {})
        skills = extracted_info.get('skills', [])
        skills_card = ctk.CTkFrame(parent,fg_color="#DFCFC2",corner_radius=15,border_width=0)
        skills_card.pack(fill="x", pady=(0, 20), padx=5)
        header_frame = ctk.CTkFrame(skills_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_label = ctk.CTkLabel(header_frame,text="Skill",font=ctk.CTkFont(size=18, weight="bold"),text_color="#1B2B4C")
        header_label.pack(anchor="w", padx=20, pady=8)
        content_frame = ctk.CTkFrame(skills_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        if skills:
            skills_display_label = ctk.CTkLabel(content_frame,text=", ".join(skills),font=ctk.CTkFont(size=14),text_color="#1B2B4C",wraplength=parent.winfo_width() - 80)
            skills_display_label.pack(anchor="w")
        else:
            no_skills_label = ctk.CTkLabel(content_frame,text="No skills extracted.",font=ctk.CTkFont(size=14),text_color="#1B2B4C")
            no_skills_label.pack(anchor="w")

    def create_job_history_section(self, parent): # Identical
        extracted_info = self.summary_data.get('extracted_info', {})
        job_history = extracted_info.get('job_history', [])
        job_card = ctk.CTkFrame(parent,fg_color="#DFCFC2",corner_radius=15,border_width=0)
        job_card.pack(fill="x", pady=(0, 20), padx=5)
        header_frame = ctk.CTkFrame(job_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_label = ctk.CTkLabel(header_frame,text="Job History",font=ctk.CTkFont(size=18, weight="bold"),text_color="#1B2B4C")
        header_label.pack(anchor="w", padx=20, pady=8)
        content_frame = ctk.CTkFrame(job_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        if not job_history:
            ctk.CTkLabel(content_frame, text="No job history extracted.", font=ctk.CTkFont(size=14), text_color="#1B2B4C").pack(anchor="w")
            return
        for job in job_history:
            job_entry_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            job_entry_frame.pack(fill="x", pady=(0,10))
            ctk.CTkLabel(job_entry_frame,text=f"{job.get('title', 'N/A')} at {job.get('company', 'N/A')}",font=ctk.CTkFont(size=16, weight="bold"),text_color="#1B2B4C").pack(anchor="w")
            ctk.CTkLabel(job_entry_frame,text=f"({job.get('dates', 'N/A')})",font=ctk.CTkFont(size=14),text_color="#1B2B4C").pack(anchor="w", pady=(2, 5))
            ctk.CTkLabel(job_entry_frame,text=job.get('description', 'No description provided.'),font=ctk.CTkFont(size=14),text_color="#1B2B4C",wraplength=parent.winfo_width() - 90, justify="left").pack(anchor="w")
    
    def create_education_section(self, parent): # Identical
        extracted_info = self.summary_data.get('extracted_info', {})
        education_history = extracted_info.get('education', [])
        edu_card = ctk.CTkFrame(parent,fg_color="#DFCFC2",corner_radius=15,border_width=0)
        edu_card.pack(fill="x", pady=(0, 20), padx=5)
        header_frame = ctk.CTkFrame(edu_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_label = ctk.CTkLabel(header_frame,text="Education",font=ctk.CTkFont(size=18, weight="bold"),text_color="#1B2B4C")
        header_label.pack(anchor="w", padx=20, pady=8)
        content_frame = ctk.CTkFrame(edu_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        if not education_history:
            ctk.CTkLabel(content_frame, text="No education history extracted.", font=ctk.CTkFont(size=14), text_color="#1B2B4C").pack(anchor="w")
            return
        for edu in education_history:
            edu_entry_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            edu_entry_frame.pack(fill="x", pady=(0,10))
            degree_text = f"{edu.get('degree', 'N/A')}"
            if edu.get('university'): degree_text += f" from {edu.get('university')}"
            ctk.CTkLabel(edu_entry_frame,text=degree_text,font=ctk.CTkFont(size=14, weight="bold"),text_color="#1B2B4C").pack(anchor="w")
            edu_period_text = f"({edu.get('dates', 'N/A')})"
            if edu.get('gpa'): edu_period_text += f" - GPA: {edu.get('gpa')}"
            ctk.CTkLabel(edu_entry_frame,text=edu_period_text,font=ctk.CTkFont(size=14),text_color="#1B2B4C").pack(anchor="w", pady=(2, 0))

    # Image loading functions (create_bearlock_confuse_image, create_asset4_image) remain
    def create_bearlock_confuse_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "bearlock-confuse.png") 
            if not os.path.exists(image_path): image_path = "./assets/bearlock-confuse.png"
            if os.path.exists(image_path):
                bearlock_image = Image.open(image_path)
                bearlock_ctk_image = ctk.CTkImage(light_image=bearlock_image, dark_image=bearlock_image, size=(120, 120))
                image_label = ctk.CTkLabel(parent, image=bearlock_ctk_image, text="")
                image_label.pack()
            else: raise FileNotFoundError("Bearlock confuse image not found")
        except Exception as e:
            print(f"Error loading bearlock-confuse.png: {e}")
            ctk.CTkLabel(parent, text="🐻🤔", font=ctk.CTkFont(size=50), text_color="#DFCFC2").pack()
    
    def create_asset4_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset4.png")
            if not os.path.exists(image_path): image_path = "./assets/asset4.png"
            if os.path.exists(image_path):
                asset_image = Image.open(image_path)
                asset_ctk_image = ctk.CTkImage(light_image=asset_image, dark_image=asset_image, size=(80, 80))
                image_label = ctk.CTkLabel(parent, image=asset_ctk_image, text="")
                image_label.pack()
            else: raise FileNotFoundError("Asset4 image not found")
        except Exception as e:
            print(f"Error loading asset4.png: {e}")
            ctk.CTkLabel(parent, text="📚", font=ctk.CTkFont(size=50), text_color="#DFCFC2").pack()