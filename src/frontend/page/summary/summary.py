import customtkinter as ctk
from PIL import Image
import os

class SummaryPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, candidate_name="Fathur"):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.candidate_name = candidate_name
        self.pack(fill="both", expand=True)
        
        self.setup_summary_page()
    
    def setup_summary_page(self):
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
        back_button.pack(anchor="nw", pady=(0, 15))
    
    def create_header_section(self, parent):
        header_container = ctk.CTkFrame(parent, fg_color="transparent")
        header_container.pack(fill="x", pady=(0, 20))
        
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
        header_content.pack(expand=True)
        
        left_image = ctk.CTkFrame(header_content, fg_color="transparent")
        left_image.pack(side="left", padx=(0, 25))
        self.create_bearlock_confuse_image(left_image)
        
        center_content = ctk.CTkFrame(header_content, fg_color="transparent")
        center_content.pack(side="left", expand=True)
        
        title_label = ctk.CTkLabel(
            center_content,
            text=f"Summary Report: {self.candidate_name}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack()
        
        description_text = """Bearlock Holmes has highlighted what matters most.Use this snapshot to
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
        self.create_asset4_image(right_image)
    
    def create_summary_content(self, parent):
        scrollable_container = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            corner_radius=0
        )
        scrollable_container.pack(fill="both", expand=True)
        
        self.create_personal_info_section(scrollable_container)
        
        self.create_skills_section(scrollable_container)
        
        self.create_job_history_section(scrollable_container)
        
        self.create_education_section(scrollable_container)
    
    def create_personal_info_section(self, parent):
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
            text=self.candidate_name,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        header_label.pack(anchor="w", padx=20, pady=8)
        
        content_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        details = [
            "Birthdate: 05-19-2025",
            "Address: Masjid Salman ITB",
            "Phone: 0812 3456 7890"
        ]
        
        for detail in details:
            detail_label = ctk.CTkLabel(
                content_frame,
                text=detail,
                font=ctk.CTkFont(size=14),
                text_color="#1B2B4C"
            )
            detail_label.pack(anchor="w", pady=2)
    
    def create_skills_section(self, parent):
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
            text="Skill",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        header_label.pack(anchor="w", padx=20, pady=8)
        
        content_frame = ctk.CTkFrame(skills_card, fg_color="transparent")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        spacer = ctk.CTkLabel(content_frame, text="", height=30)
        spacer.pack()
    
    def create_job_history_section(self, parent):
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
        
        job_title = ctk.CTkLabel(
            content_frame,
            text="CTO",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#1B2B4C"
        )
        job_title.pack(anchor="w")
        
        job_period = ctk.CTkLabel(
            content_frame,
            text="2023 - 2024",
            font=ctk.CTkFont(size=14),
            text_color="#1B2B4C"
        )
        job_period.pack(anchor="w", pady=(2, 5))
        
        job_desc = ctk.CTkLabel(
            content_frame,
            text="Leading the organization's technology strategies",
            font=ctk.CTkFont(size=14),
            text_color="#1B2B4C"
        )
        job_desc.pack(anchor="w")
    
    def create_education_section(self, parent):
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
        
        edu_program = ctk.CTkLabel(
            content_frame,
            text="Informatics Engineering (Institut Teknologi Bandung)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1B2B4C"
        )
        edu_program.pack(anchor="w")
        
        edu_period = ctk.CTkLabel(
            content_frame,
            text="2022 - 2026",
            font=ctk.CTkFont(size=14),
            text_color="#1B2B4C"
        )
        edu_period.pack(anchor="w", pady=(2, 0))
    
    def create_bearlock_confuse_image(self, parent):
        try:
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
        except Exception as e:
            placeholder = ctk.CTkLabel(
                parent,
                text="🐻🤔",
                font=ctk.CTkFont(size=50),
                text_color="#DFCFC2"
            )
            placeholder.pack()
    
    def create_asset4_image(self, parent):
        try:
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
        except Exception as e:
            placeholder = ctk.CTkLabel(
                parent,
                text="📚",
                font=ctk.CTkFont(size=50),
                text_color="#DFCFC2"
            )
            placeholder.pack()