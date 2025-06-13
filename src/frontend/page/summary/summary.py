# src/frontend/page/summary/summary.py
import customtkinter as ctk
from PIL import Image
import os
 
class SummaryPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager, applicant_id, cv_path=None, **kwargs):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0,
            **kwargs
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager
        self.applicant_id = applicant_id
        self.cv_path_for_extraction = cv_path
        self.summary_data = None
        
        self.pack(fill="both", expand=True)
        
        # Bind to configure event to handle window resizing
        self.bind("<Configure>", self._on_window_configure)
        
        self._load_data_and_setup_ui()

    def _on_window_configure(self, event):
        """Handle window resize events to update text wrapping"""
        if event.widget == self:
            self.after_idle(self._update_text_wrapping)
    
    def _update_text_wrapping(self):
        """Update text wrapping for all text widgets based on current window size"""
        try:
            current_width = self.winfo_width()
            if current_width > 1:  # Ensure window is properly initialized
                # Update wrapping for any stored text widgets
                if hasattr(self, '_text_widgets_to_wrap'):
                    for widget_info in self._text_widgets_to_wrap:
                        widget = widget_info['widget']
                        padding = widget_info.get('padding', 100)
                        if widget.winfo_exists():
                            new_wrap_length = max(200, current_width - padding)
                            widget.configure(wraplength=new_wrap_length)
        except Exception as e:
            print(f"Error updating text wrapping: {e}")

    def _load_data_and_setup_ui(self):
        if self.applicant_id is None:
            print("ERROR (SummaryPage): Applicant ID is None.")
            self._display_error_message("No applicant information available.")
            return

        # Get profile information using applicant_id
        profile_info = self.backend_manager._get_applicant_profile(self.applicant_id)
        if not profile_info or "error" in profile_info:
            error_msg = profile_info.get("error", "Failed to load applicant profile.") if profile_info else "Failed to load applicant profile."
            print(f"ERROR (SummaryPage Profile): {error_msg}")
            self._display_error_message(error_msg)
            return
        
        cv_text_to_extract = ""
        path_used_for_extraction = ""

        # Determine which CV path to use for text extraction
        if self.cv_path_for_extraction and os.path.exists(self.cv_path_for_extraction):
            print(f"SummaryPage: Using specific CV path for extraction: {self.cv_path_for_extraction}")
            path_used_for_extraction = self.cv_path_for_extraction
        elif self.applicant_id:
            print(f"SummaryPage: No specific CV path, deriving from applicant_id: {self.applicant_id}")
            derived_path = self.backend_manager.get_raw_cv_path(self.applicant_id)
            if derived_path and os.path.exists(derived_path):
                path_used_for_extraction = derived_path
            else:
                print(f"SummaryPage: Could not derive a valid CV path for applicant_id {self.applicant_id}")
        
        if not path_used_for_extraction:
            self._display_error_message(f"No valid CV path found for applicant {self.applicant_id} for summary extraction.")
            return

        cv_text = self.backend_manager.cv_processor.extract_text_from_pdf(path_used_for_extraction)
        
        if not cv_text or not cv_text.strip():
            self._display_error_message(f"CV content is empty or could not be extracted from {os.path.basename(path_used_for_extraction)}")
            return
        
        cv_text_to_extract = cv_text

        try:
            extracted_info = {
                "skills": self.backend_manager.regex_extractor.extract_skills(cv_text_to_extract),
                "job_history": self.backend_manager.regex_extractor.extract_job_history(cv_text_to_extract),
                "education": self.backend_manager.regex_extractor.extract_education(cv_text_to_extract)
            }
            
            print(f"DEBUG: Extracted job history: {extracted_info['job_history']}")
            print(f"DEBUG: Job history type: {type(extracted_info['job_history'])}")
            
        except Exception as e:
            print(f"ERROR during regex extraction: {e}")
            self._display_error_message(f"Failed to extract information from CV: {str(e)}")
            return

        self.summary_data = {
            "applicant_profile": profile_info,
            "extracted_info": extracted_info
        }
        
        self.setup_summary_page()

    def _display_error_message(self, message):
        for widget in self.winfo_children():
            widget.destroy()
        
        # Initialize text widgets tracking
        self._text_widgets_to_wrap = []
        
        error_label = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=18),
            text_color="tomato",
            wraplength=400,
            justify="center"
        )
        error_label.pack(expand=True, padx=20, pady=20)
        
        # Track this widget for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': error_label,
            'padding': 40
        })
        
        back_button = ctk.CTkButton(
            self,
            text="← Back to Results",
            font=ctk.CTkFont(size=16),
            width=150,
            height=40,
            fg_color="#334D7A",
            hover_color="#273A5C",
            text_color="#DFCFC2",
            command=lambda: self.navigate_callback("result")
        )
        back_button.pack(pady=20)

    def setup_summary_page(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        # Initialize text widgets tracking
        self._text_widgets_to_wrap = []
        
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
            command=lambda: self.navigate_callback("result")
        )
        back_button.pack(anchor="nw", pady=(0, 0)) 
    
    def create_header_section(self, parent):
        header_container = ctk.CTkFrame(parent, fg_color="transparent")
        header_container.pack(fill="x", pady=(0, 20))
        
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
        header_content.pack(expand=True)
        
        center_content = ctk.CTkFrame(header_content, fg_color="transparent")
        center_content.pack(side="left", expand=True)
        
        profile = self.summary_data.get('applicant_profile', {})
        candidate_name = f"{profile.get('first_name', 'N/A')} {profile.get('last_name', '')}".strip()
        
        title_label = ctk.CTkLabel(
            center_content,
            text=f"Summary Report: {candidate_name}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2",
            wraplength=800
        )
        title_label.pack()
        
        # Track title for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': title_label,
            'padding': 100
        })
        
        description_label = ctk.CTkLabel(
            center_content,
            text="""Bearlock Holmes has highlighted what matters most. Use this snapshot to
assess compatibility at a glance.""",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            justify="center",
            wraplength=600
        )
        description_label.pack(pady=(8, 0))
        
        # Track description for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': description_label,
            'padding': 100
        })
    
    def create_summary_content(self, parent):
        scrollable_container = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color="#334D7A",
            scrollbar_button_hover_color="#4A5D8A"
        )
        scrollable_container.pack(fill="both", expand=True)
        
        if not self.summary_data or "error" in self.summary_data:
            return
        
        self.create_personal_info_section(scrollable_container)
        self.create_skills_section(scrollable_container)
        self.create_job_history_section(scrollable_container)
        self.create_education_section(scrollable_container)
    
    def create_personal_info_section(self, parent):
        profile = self.summary_data.get('applicant_profile', {})
        candidate_name = f"{profile.get('first_name', 'N/A')} {profile.get('last_name', '')}".strip()
        
        info_card = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=15,
            border_width=0
        )
        info_card.pack(fill="x", pady=(0, 20), padx=5)
        
        header_frame = ctk.CTkFrame(info_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text=candidate_name,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C",
            wraplength=400
        )
        header_label.pack(anchor="w", padx=20, pady=8)
        
        # Track header for responsive wrapping
        self._text_widgets_to_wrap.append({
            'widget': header_label,
            'padding': 40
        })
        
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
                text_color="#1B2B4C",
                wraplength=500,
                anchor="w",
                justify="left"
            )
            detail_label.pack(anchor="w", pady=2, fill="x")
            
            # Track detail labels for responsive wrapping
            self._text_widgets_to_wrap.append({
                'widget': detail_label,
                'padding': 80
            })
    
    def create_skills_section(self, parent):
        extracted_info = self.summary_data.get('extracted_info', {})
        skills = extracted_info.get('skills', [])
        
        skills_card = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=15,
            border_width=0
        )
        skills_card.pack(fill="x", pady=(0, 20), padx=5)
        
        header_frame = ctk.CTkFrame(skills_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="Skills",
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
                wraplength=500,
                anchor="w",
                justify="left"
            )
            skills_display_label.pack(anchor="w", fill="x")
            
            # Track skills label for responsive wrapping
            self._text_widgets_to_wrap.append({
                'widget': skills_display_label,
                'padding': 80
            })
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
        
        print(f"DEBUG: Creating job history section with data: {job_history}")
        print(f"DEBUG: Job history type: {type(job_history)}")
        
        job_card = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=15,
            border_width=0
        )
        job_card.pack(fill="x", pady=(0, 20), padx=5)
        
        header_frame = ctk.CTkFrame(job_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="Job History",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        header_label.pack(anchor="w", padx=20, pady=8)
        
        content_frame = ctk.CTkFrame(job_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        # FIXED: Handle different job history formats
        if not job_history:
            no_history_label = ctk.CTkLabel(
                content_frame,
                text="No job history extracted.",
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C"
            )
            no_history_label.pack(anchor="w")
            return
        
        # Handle string/text format
        if isinstance(job_history, str):
            job_history_label = ctk.CTkLabel(
                content_frame,
                text=job_history,
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C",
                wraplength=500,
                anchor="w",
                justify="left"
            )
            job_history_label.pack(fill="x", padx=0, pady=0)
            self._text_widgets_to_wrap.append({
                'widget': job_history_label,
                'padding': 90
            })
            return
        
        # Handle tuple format (text, type_indicator)
        if isinstance(job_history, tuple) and len(job_history) == 2:
            job_text, format_type = job_history
            print(f"DEBUG: Tuple format - text: {job_text}, type: {format_type}")
            
            job_history_label = ctk.CTkLabel(
                content_frame,
                text=str(job_text),
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C",
                wraplength=500,
                anchor="w",
                justify="left"
            )
            job_history_label.pack(fill="x", padx=0, pady=0)
            self._text_widgets_to_wrap.append({
                'widget': job_history_label,
                'padding': 90
            })
            return
        
        # Handle list of dictionaries (structured data)
        if isinstance(job_history, list) and all(isinstance(job, dict) for job in job_history):
            for job in job_history:
                job_entry_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                job_entry_frame.pack(fill="x", pady=(0, 10))
                
                # Job title and company
                job_title_text = f"{job.get('title', 'N/A')} at {job.get('company', 'N/A')}"
                job_title_label = ctk.CTkLabel(
                    job_entry_frame,
                    text=job_title_text,
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#1B2B4C",
                    wraplength=500,
                    anchor="w",
                    justify="left"
                )
                job_title_label.pack(anchor="w", fill="x")
                
                # Track job title for responsive wrapping
                self._text_widgets_to_wrap.append({
                    'widget': job_title_label,
                    'padding': 90
                })
                
                # Job dates
                job_dates_label = ctk.CTkLabel(
                    job_entry_frame,
                    text=f"({job.get('dates', 'N/A')})",
                    font=ctk.CTkFont(size=14),
                    text_color="#1B2B4C"
                )
                job_dates_label.pack(anchor="w", pady=(2, 5))
                
                # Job description
                job_description = job.get('description', 'No description provided.')
                if job_description and job_description.strip():
                    job_desc_label = ctk.CTkLabel(
                        job_entry_frame,
                        text=job_description,
                        font=ctk.CTkFont(size=14),
                        text_color="#1B2B4C",
                        wraplength=500,
                        anchor="w",
                        justify="left"
                    )
                    job_desc_label.pack(anchor="w", fill="x")
                    
                    # Track job description for responsive wrapping
                    self._text_widgets_to_wrap.append({
                        'widget': job_desc_label,
                        'padding': 90
                    })
            return
        
        # Handle any other format - convert to string
        fallback_text = str(job_history)
        print(f"DEBUG: Fallback format - displaying as string: {fallback_text}")
        
        job_history_label = ctk.CTkLabel(
            content_frame,
            text=fallback_text,
            font=ctk.CTkFont(size=14),
            text_color="#1B2B4C",
            wraplength=500,
            anchor="w",
            justify="left"
        )
        job_history_label.pack(fill="x", padx=0, pady=0)
        self._text_widgets_to_wrap.append({
            'widget': job_history_label,
            'padding': 90
        })
    
    def create_education_section(self, parent):
        extracted_info = self.summary_data.get('extracted_info', {})
        education_history = extracted_info.get('education', [])
        
        edu_card = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=15,
            border_width=0
        )
        edu_card.pack(fill="x", pady=(0, 20), padx=5)
        
        header_frame = ctk.CTkFrame(edu_card, fg_color="#B8A398", corner_radius=12)
        header_frame.pack(fill="x", padx=0, pady=0)
        
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
            no_edu_label = ctk.CTkLabel(
                content_frame,
                text="No education history extracted.",
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C"
            )
            no_edu_label.pack(anchor="w")
            return
        
        if education_history and isinstance(education_history, list) and all(isinstance(edu, dict) for edu in education_history):
            # Display structured education entries
            for edu in education_history:
                edu_entry_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                edu_entry_frame.pack(fill="x", pady=(0, 10))

                degree_text = f"{edu.get('degree', 'N/A')}"
                if edu.get('university'):
                    degree_text += f" from {edu.get('university')}"
                
                degree_label = ctk.CTkLabel(
                    edu_entry_frame,
                    text=degree_text,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color="#1B2B4C",
                    wraplength=500,
                    anchor="w",
                    justify="left"
                )
                degree_label.pack(anchor="w", fill="x")
                
                # Track degree label for responsive wrapping
                self._text_widgets_to_wrap.append({
                    'widget': degree_label,
                    'padding': 90
                })

                edu_period_text = f"({edu.get('dates', 'N/A')})"
                if edu.get('gpa'):
                    edu_period_text += f" - GPA: {edu.get('gpa')}"
                
                period_label = ctk.CTkLabel(
                    edu_entry_frame,
                    text=edu_period_text,
                    font=ctk.CTkFont(size=14),
                    text_color="#1B2B4C",
                    wraplength=500,
                    anchor="w",
                    justify="left"
                )
                period_label.pack(anchor="w", pady=(2, 0), fill="x")
                
                # Track period label for responsive wrapping
                self._text_widgets_to_wrap.append({
                    'widget': period_label,
                    'padding': 90
                })
        else:
            # Handle non-structured education data
            edu_text = education_history.get('full_text', str(education_history))
            edu_text_label = ctk.CTkLabel(
                content_frame,
                text=edu_text,
                font=ctk.CTkFont(size=13),
                text_color="#1B2B4C",
                wraplength=500,
                anchor="w",
                justify="left"
            )
            edu_text_label.pack(anchor="w", fill="x")
            
            # Track education text for responsive wrapping
            self._text_widgets_to_wrap.append({
                'widget': edu_text_label,
                'padding': 90
            })

    def create_bearlock_confuse_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "bearlock-confuse.png") 
            if not os.path.exists(image_path):
                image_path = "./assets/bearlock-confuse.png"
            if os.path.exists(image_path):
                bearlock_image = Image.open(image_path)
                bearlock_ctk_image = ctk.CTkImage(light_image=bearlock_image, dark_image=bearlock_image, size=(120, 120))
                image_label = ctk.CTkLabel(parent, image=bearlock_ctk_image, text="")
                image_label.pack()
            else:
                raise FileNotFoundError("Bearlock confuse image not found")
        except Exception as e:
            print(f"Error loading bearlock-confuse.png: {e}")
            ctk.CTkLabel(parent, text="🐻🤔", font=ctk.CTkFont(size=50), text_color="#DFCFC2").pack()
    
    def create_asset4_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset4.png")
            if not os.path.exists(image_path):
                image_path = "./assets/asset4.png"
            if os.path.exists(image_path):
                asset_image = Image.open(image_path)
                asset_ctk_image = ctk.CTkImage(light_image=asset_image, dark_image=asset_image, size=(80, 80))
                image_label = ctk.CTkLabel(parent, image=asset_ctk_image, text="")
                image_label.pack()
            else:
                raise FileNotFoundError("Asset4 image not found")
        except Exception as e:
            print(f"Error loading asset4.png: {e}")
            ctk.CTkLabel(parent, text="📚", font=ctk.CTkFont(size=50), text_color="#DFCFC2").pack()