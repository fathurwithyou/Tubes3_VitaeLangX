import customtkinter as ctk
from PIL import Image
import os

class CVPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, candidate_name="Fathur"):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.candidate_name = candidate_name
        self.pack(fill="both", expand=True)
        
        self.setup_cv_page()
    
    def setup_cv_page(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=50, pady=30)
        
        self.create_back_button(main_container)
        
        self.create_header_section(main_container)
        
        self.create_cv_content(main_container)
    
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
        header_container.pack(fill="x", pady=(0, 30))
        
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
        header_content.pack(expand=True)
        
        left_image = ctk.CTkFrame(header_content, fg_color="transparent")
        left_image.pack(side="left", padx=(0, 25))
        self.create_bearlock_happy_image(left_image)
        
        center_content = ctk.CTkFrame(header_content, fg_color="transparent")
        center_content.pack(side="left", expand=True)
        
        title_label = ctk.CTkLabel(
            center_content,
            text=f"Full Case File: {self.candidate_name}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack()
        
        description_text = """This is the original CV as submitted by the candidate, no filters, no edits. Review
every detail, just as they wrote it."""
        
        description_label = ctk.CTkLabel(
            center_content,
            text=description_text,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            justify="center"
        )
        description_label.pack(pady=(10, 0))
        
        right_image = ctk.CTkFrame(header_content, fg_color="transparent")
        right_image.pack(side="right", padx=(25, 0))
        self.create_asset1_image(right_image)
    
    def create_cv_content(self, parent):
        cv_container = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=15,
            border_width=3,
            border_color="#DFCFC2"
        )
        cv_container.pack(fill="both", expand=True)
        
        cv_scrollable = ctk.CTkScrollableFrame(
            cv_container,
            fg_color="transparent",
            corner_radius=0
        )
        cv_scrollable.pack(fill="both", expand=True, padx=30, pady=30)
        
        cv_content = self.get_cv_content()
        
        cv_text_label = ctk.CTkLabel(
            cv_scrollable,
            text=cv_content,
            font=ctk.CTkFont(size=13),
            text_color="#000000",
            justify="left",
            anchor="nw"
        )
        cv_text_label.pack(fill="both", expand=True)
    
    def get_cv_content(self):
        return """Paragraph 1 - Overview:
John Doe is a data analyst with over 4 years of experience specializing in transforming raw datasets into actionable business insights. With a strong foundation in Python, SQL, and Excel, he has worked across e-commerce and logistics industries, delivering reports that improved operational efficiency by up to 30%.

Paragraph 2 - Skills & Strengths:
He brings a solid command of data visualization tools such as Tableau and Power BI, combined with the ability to communicate complex findings in simple terms. His work often intersects with automation and ETL pipeline development, making him a versatile asset for data-driven teams.

Paragraph 3 - Recent Achievements:
Most recently, John led a predictive analytics project that helped forecast customer churn with 92% accuracy, contributing directly to a 12% increase in retention. He's now seeking opportunities where he can apply his analytical mindset to solve real-world business problems at scale.

Paragraph 1 - Overview:
John Doe is a data analyst with over 4 years of experience specializing in transforming raw datasets into actionable business insights. With a strong foundation in Python, SQL, and Excel, he has worked across e-commerce and logistics industries, delivering reports that improved operational efficiency by up to 30%.

Paragraph 2 - Skills & Strengths:
He brings a solid command of data visualization tools such as Tableau and Power BI, combined with the ability to communicate complex findings in simple terms. His work often intersects with automation and ETL pipeline development, making him a versatile asset for data-driven teams.

Paragraph 3 - Recent Achievements:
Most recently, John led a predictive analytics project that helped forecast customer churn with 92% accuracy, contributing directly to a 12% increase in retention. He's now seeking opportunities where he can apply his analytical mindset to solve real-world business problems at scale.

Paragraph 1 - Overview:
John Doe is a data analyst with over 4 years of experience specializing in transforming raw datasets into actionable business insights. With a strong foundation in Python, SQL, and Excel, he has worked across e-commerce and logistics industries, delivering reports that improved operational efficiency by up to 30%.

Paragraph 2 - Skills & Strengths:
He brings a solid command of data visualization tools such as Tableau and Power BI, combined with the ability to communicate complex findings in simple terms. His work often intersects with automation and ETL pipeline development, making him a versatile asset for data-driven teams."""
    
    def create_bearlock_happy_image(self, parent):
        try:
            image_path = "./assets/bearlock-happy.png"
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
                text="Bear",
                font=ctk.CTkFont(size=50),
                text_color="#DFCFC2"
            )
            placeholder.pack()
    
    def create_asset1_image(self, parent):
        try:
            image_path = "./assets/asset1.png"
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
                text="📄",
                font=ctk.CTkFont(size=50),
                text_color="#DFCFC2"
            )
            placeholder.pack()