# src/frontend/page/summary/summary.py
import customtkinter as ctk
from PIL import Image
import os
# Ensure Settings is available if needed for display, though not directly used for fetching here
# from backend import Settings 

class SummaryPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager, applicant_id, **kwargs):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0,
            **kwargs
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager
        self.applicant_id = applicant_id
        self.summary_data = None # Initialize
        
        self.pack(fill="both", expand=True)
        
        self._load_data_and_setup_ui()

    def _load_data_and_setup_ui(self):
        if self.applicant_id is None:
            print("ERROR (SummaryPage): Applicant ID is None.")
            self._display_error_message("No applicant information available.")
            return

        self.summary_data = self.backend_manager.get_cv_summary(self.applicant_id)

        if not self.summary_data or "error" in self.summary_data:
            error_msg = self.summary_data.get("error", "Failed to load summary data.") if self.summary_data else "Failed to load summary data."
            print(f"ERROR (SummaryPage): {error_msg}")
            self._display_error_message(error_msg)
            return
        
        self.setup_summary_page()

    def _display_error_message(self, message):
        # Clear existing widgets if any before showing error
        for widget in self.winfo_children():
            widget.destroy()
        
        error_label = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=18),
            text_color="tomato"
        )
        error_label.pack(expand=True, padx=20, pady=20)
        
        back_button = ctk.CTkButton(
            self,
            text="← Back to Results",
            font=ctk.CTkFont(size=16),
            width=150,
            height=40,
            corner_radius=8,
            command=lambda: self.navigate_callback("result") 
        )
        back_button.pack(pady=20)

    def setup_summary_page(self):
        # If setup_summary_page was already called by _load_data_and_setup_ui
        # and it succeeded, self.summary_data is populated.
        # Clear any potential error message widgets if we are re-setting up UI
        for widget in self.winfo_children():
            widget.destroy()
            
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=50, pady=30)
        
        self.create_back_button(main_container)
        self.create_header_section(main_container)
        self.create_summary_content(main_container)
    
    def create_back_button(self, parent):
        back_button = ctk.CTkButton(
            parent,
            text="←",
            font=ctk.CTkFont(size=20, weight="bold"),
            width=60,
            height=40,
            corner_radius=8,
            border_width=2,
            border_color="#DFCFC2", 
            fg_color="#334D7A",
            hover_color="#1B2B4C", 
            text_color="#DFCFC2",
            command=lambda: self.navigate_callback("result") # Ensure it goes back to results if that's the previous page
        )
        back_button.pack(anchor="nw", pady=(0, 15))
    
    def create_header_section(self, parent):
        header_container = ctk.CTkFrame(parent, fg_color="transparent")
        header_container.pack(fill="x", pady=(0, 20))
        
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
        header_content.pack(expand=True)
        
        left_image = ctk.CTkFrame(header_content, fg_color="transparent")
        left_image.pack(side="left", padx=(0, 25))
        self.create_bearlock_confuse_image(left_image) # This can stay as is
        
        center_content = ctk.CTkFrame(header_content, fg_color="transparent")
        center_content.pack(side="left", expand=True)

        profile = self.summary_data.get('applicant_profile', {})
        first_name = profile.get('first_name', 'N/A')
        last_name = profile.get('last_name', '')
        candidate_name = f"{first_name} {last_name}".strip()

        title_label = ctk.CTkLabel(
            center_content,
            text=f"Summary Report: {candidate_name}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack()
        
        description_text = """Bearlock Holmes has highlighted what matters most. Use this snapshot to
assess compatibility at a glance."""
        
        description_label = ctk.CTkLabel(
            center_content,
            text=description_text,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            justify="center"
        )
        description_label.pack(pady=(8, 0))
        
        right_image = ctk.CTkFrame(header_content, fg_color="transparent")
        right_image.pack(side="right", padx=(25, 0))
        self.create_asset4_image(right_image) # This can stay as is
    
    def create_summary_content(self, parent):
        scrollable_container = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            corner_radius=0
        )
        scrollable_container.pack(fill="both", expand=True)
        
        if not self.summary_data or "error" in self.summary_data:
             # Error already handled by _display_error_message, content won't be created
            return

        self.create_personal_info_section(scrollable_container)
        self.create_skills_section(scrollable_container)
        self.create_job_history_section(scrollable_container)
        self.create_education_section(scrollable_container)
    
    def create_personal_info_section(self, parent):
        profile = self.summary_data.get('applicant_profile', {})
        first_name = profile.get('first_name', 'N/A')
        last_name = profile.get('last_name', '')
        candidate_name = f"{first_name} {last_name}".strip()
        
        info_card = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=15,
            border_width=3,
            border_color="#DFCFC2"
        )
        info_card.pack(fill="x", pady=(0, 20))
        
        header_frame = ctk.CTkFrame(info_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=3, pady=(3, 0))
        
        header_label = ctk.CTkLabel(
            header_frame,
            text=candidate_name, # Dynamic name
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        header_label.pack(anchor="w", padx=20, pady=8)
        
        content_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        details = [
            f"Birthdate: {profile.get('date_of_birth', 'N/A')}",
            f"Address: {profile.get('address', 'N/A')}",
            f"Phone: {profile.get('phone_number', 'N/A')}"
        ]
        
        for detail_text in details:
            detail_label = ctk.CTkLabel(
                content_frame,
                text=detail_text,
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C"
            )
            detail_label.pack(anchor="w", pady=2)
    
    def create_skills_section(self, parent):
        extracted_info = self.summary_data.get('extracted_info', {})
        skills = extracted_info.get('skills', [])

        skills_card = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=15,
            border_width=3,
            border_color="#DFCFC2"
        )
        skills_card.pack(fill="x", pady=(0, 20))
        
        header_frame = ctk.CTkFrame(skills_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=3, pady=(3, 0))
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="Skills", # Static title
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        header_label.pack(anchor="w", padx=20, pady=8)
        
        content_frame = ctk.CTkFrame(skills_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        if skills:
            skills_text = ", ".join(skills)
            skills_display_label = ctk.CTkLabel(
                content_frame,
                text=skills_text,
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C",
                wraplength=parent.winfo_width() - 60 # Adjust wraplength
            )
            skills_display_label.pack(anchor="w")
        else:
            no_skills_label = ctk.CTkLabel(
                content_frame,
                text="No skills extracted.",
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C"
            )
            no_skills_label.pack(anchor="w")

    def create_job_history_section(self, parent):
        extracted_info = self.summary_data.get('extracted_info', {})
        job_history = extracted_info.get('job_history', [])

        job_card = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=15,
            border_width=3,
            border_color="#DFCFC2"
        )
        job_card.pack(fill="x", pady=(0, 20))
        
        header_frame = ctk.CTkFrame(job_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=3, pady=(3, 0))
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="Job History",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        header_label.pack(anchor="w", padx=20, pady=8)
        
        content_frame = ctk.CTkFrame(job_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)

        if not job_history:
            no_job_label = ctk.CTkLabel(content_frame, text="No job history extracted.", font=ctk.CTkFont(size=14), text_color="#1B2B4C")
            no_job_label.pack(anchor="w")
            return

        for job in job_history:
            job_entry_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            job_entry_frame.pack(fill="x", pady=(0,10))

            job_title_text = f"{job.get('title', 'N/A')} at {job.get('company', 'N/A')}"
            job_title = ctk.CTkLabel(
                job_entry_frame,
                text=job_title_text,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#1B2B4C"
            )
            job_title.pack(anchor="w")
            
            job_period_text = f"({job.get('dates', 'N/A')})"
            job_period = ctk.CTkLabel(
                job_entry_frame,
                text=job_period_text,
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C"
            )
            job_period.pack(anchor="w", pady=(2, 5))
            
            job_desc_text = job.get('description', 'No description provided.')
            job_desc = ctk.CTkLabel(
                job_entry_frame,
                text=job_desc_text,
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C",
                wraplength=parent.winfo_width() - 70, # Adjust wraplength
                justify="left"
            )
            job_desc.pack(anchor="w")
    
    def create_education_section(self, parent):
        extracted_info = self.summary_data.get('extracted_info', {})
        education_history = extracted_info.get('education', [])

        edu_card = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=15,
            border_width=3,
            border_color="#DFCFC2"
        )
        edu_card.pack(fill="x", pady=(0, 20))
        
        header_frame = ctk.CTkFrame(edu_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=3, pady=(3, 0))
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="Education",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        header_label.pack(anchor="w", padx=20, pady=8)
        
        content_frame = ctk.CTkFrame(edu_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)

        if not education_history:
            no_edu_label = ctk.CTkLabel(content_frame, text="No education history extracted.", font=ctk.CTkFont(size=14), text_color="#1B2B4C")
            no_edu_label.pack(anchor="w")
            return

        for edu in education_history:
            edu_entry_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            edu_entry_frame.pack(fill="x", pady=(0,10))

            degree_text = f"{edu.get('degree', 'N/A')}"
            if edu.get('university'):
                degree_text += f" from {edu.get('university')}"

            edu_program = ctk.CTkLabel(
                edu_entry_frame,
                text=degree_text,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#1B2B4C"
            )
            edu_program.pack(anchor="w")
            
            edu_period_text = f"({edu.get('dates', 'N/A')})"
            if edu.get('gpa'):
                 edu_period_text += f" - GPA: {edu.get('gpa')}"

            edu_period = ctk.CTkLabel(
                edu_entry_frame,
                text=edu_period_text,
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C"
            )
            edu_period.pack(anchor="w", pady=(2, 0))

    # --- Image creation methods (can remain largely the same) ---
    def create_bearlock_confuse_image(self, parent):
        # ... (implementation as provided, consider centralizing asset paths if used in many places)
        # For robustness, ensure paths are relative to the script or use absolute paths
        try:
            # Try a path relative to the current file's directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "bearlock-confuse.png") # Adjusted path
            
            if not os.path.exists(image_path): # Fallback to original path if not found
                 image_path = "./assets/bearlock-confuse.png"

            if os.path.exists(image_path):
                bearlock_image = Image.open(image_path)
                bearlock_ctk_image = ctk.CTkImage(
                    light_image=bearlock_image,
                    dark_image=bearlock_image,
                    size=(120, 120)
                )
                image_label = ctk.CTkLabel(
                    parent,
                    image=bearlock_ctk_image,
                    text=""
                )
                image_label.pack()
            else:
                raise FileNotFoundError("Bearlock confuse image not found")
        except Exception as e:
            print(f"Error loading bearlock-confuse.png: {e}")
            placeholder = ctk.CTkLabel(
                parent, text="🐻🤔", font=ctk.CTkFont(size=50), text_color="#DFCFC2"
            )
            placeholder.pack()
    
    def create_asset4_image(self, parent):
        # ... (implementation as provided, consider centralizing asset paths)
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset4.png")

            if not os.path.exists(image_path):
                 image_path = "./assets/asset4.png"

            if os.path.exists(image_path):
                asset_image = Image.open(image_path)
                asset_ctk_image = ctk.CTkImage(
                    light_image=asset_image,
                    dark_image=asset_image,
                    size=(80, 80)
                )
                image_label = ctk.CTkLabel(
                    parent,
                    image=asset_ctk_image,
                    text=""
                )
                image_label.pack()
            else:
                raise FileNotFoundError("Asset4 image not found")
        except Exception as e:
            print(f"Error loading asset4.png: {e}")
            placeholder = ctk.CTkLabel(
                parent, text="📚", font=ctk.CTkFont(size=50), text_color="#DFCFC2"
            )
            placeholder.pack()