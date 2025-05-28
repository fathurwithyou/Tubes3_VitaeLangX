import customtkinter as ctk
from PIL import Image
import os

class ResultPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.pack(fill="both", expand=True)
        
        self.setup_result_page()
    
    def setup_result_page(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        self.create_back_button(main_container)
        
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.create_header_section(content_container)
        
        self.create_results_grid(content_container)
    
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
            command=lambda: self.navigate_callback("search")
        )
        back_button.place(x=50, y=30) 
    
    def create_header_section(self, parent):
        header_container = ctk.CTkFrame(parent, fg_color="transparent")
        header_container.pack(pady=(0, 20))
        
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
        header_content.pack()
        
        left_image = ctk.CTkFrame(header_content, fg_color="transparent")
        left_image.pack(side="left", padx=(0, 20))
        self.create_hat_image(left_image)
        
        center_content = ctk.CTkFrame(header_content, fg_color="transparent")
        center_content.pack(side="left")
        
        title_label = ctk.CTkLabel(
            center_content,
            text="Results",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#DFCFC2"
        )
        title_label.pack()
        
        description_text = """The search is complete! Bearlock Holmes has scanned 100 CVs in just 100 ms and uncovered
candidates that match your clues. Whether it's an exact keyword hit or a fuzzy match, the most
promising profiles are now on your desk."""
        
        description_label = ctk.CTkLabel(
            center_content,
            text=description_text,
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF",
            justify="center"
        )
        description_label.pack(pady=(10, 0))
        
        right_image = ctk.CTkFrame(header_content, fg_color="transparent")
        right_image.pack(side="right", padx=(20, 0))
        self.create_book_image(right_image)
    
    def create_results_grid(self, parent):
        results_container = ctk.CTkFrame(parent, fg_color="transparent")
        results_container.pack(pady=(0, 0))
        
        cards_frame = ctk.CTkFrame(results_container, fg_color="transparent")
        cards_frame.pack()  
        
        dummy_results = [
            {
                "name": "Fathur",
                "total_matches": 4,
                "keywords": {
                    "React": 1,
                    "Express": 2,
                    "HTML": 1
                }
            },
            {
                "name": "Fathur", 
                "total_matches": 4,
                "keywords": {
                    "React": 1,
                    "Express": 2,
                    "HTML": 1
                }
            },
            {
                "name": "Fathur",
                "total_matches": 4,
                "keywords": {
                    "React": 1,
                    "Express": 2,
                    "HTML": 1
                }
            }
        ]
        
        for i, result in enumerate(dummy_results):
            card_frame = ctk.CTkFrame(
                cards_frame,
                fg_color="#DFCFC2",
                corner_radius=15,
                width=300, 
                height=280 
            )
            card_frame.pack(side="left", padx=25, pady=10) 
            card_frame.pack_propagate(False)
            
            self.create_result_card(card_frame, result)
    
    def create_result_card(self, parent, result):
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=result["name"],
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#1B2B4C"
        )
        name_label.pack(side="left")
        
        matches_label = ctk.CTkLabel(
            header_frame,
            text=f"{result['total_matches']} matches",
            font=ctk.CTkFont(size=16),
            text_color="#1B2B4C"
        )
        matches_label.pack(side="right")
        
        keywords_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        keywords_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        keywords_title = ctk.CTkLabel(
            keywords_frame,
            text="Matched keywords:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1B2B4C"
        )
        keywords_title.pack(anchor="w", pady=(0, 8))
        
        for i, (keyword, count) in enumerate(result["keywords"].items(), 1):
            keyword_text = f"{i}. {keyword}: {count} occurrence"
            if count > 1:
                keyword_text += "s"
                
            keyword_label = ctk.CTkLabel(
                keywords_frame,
                text=keyword_text,
                font=ctk.CTkFont(size=13),
                text_color="#1B2B4C"
            )
            keyword_label.pack(anchor="w", pady=2)
        
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(5, 0))  
        
        summary_button = ctk.CTkButton(
            buttons_frame,
            text="Summary",
            font=ctk.CTkFont(size=14, weight="normal"),
            width=100,
            height=32, 
            corner_radius=6,
            border_width=2,
            border_color="#F9DFDC", 
            fg_color="#334D7A",
            hover_color="#1B2B4C", 
            text_color="#DFCFC2",
            command=lambda: self.show_summary(result["name"])
        )
        summary_button.pack(side="left", padx=(0, 10))
        
        view_cv_button = ctk.CTkButton(
            buttons_frame,
            text="View CV",
            font=ctk.CTkFont(size=14, weight="normal"),
            width=100,
            height=32, 
            corner_radius=6,
            border_width=2,
            border_color="#F9DFDC", 
            fg_color="#334D7A",
            hover_color="#1B2B4C", 
            text_color="#DFCFC2",
            command=lambda: self.view_cv(result["name"])
        )
        view_cv_button.pack(side="right")
    
    def create_hat_image(self, parent):
        try:
            image_path = "./assets/asset2.png"
            if os.path.exists(image_path):
                hat_image = Image.open(image_path)
                hat_ctk_image = ctk.CTkImage(
                    light_image=hat_image,
                    dark_image=hat_image,
                    size=(100, 95)
                )
                image_label = ctk.CTkLabel(
                    parent,
                    image=hat_ctk_image,
                    text=""
                )
                image_label.pack()
        except Exception as e:
            placeholder = ctk.CTkLabel(
                parent,
                text="Hat",
                font=ctk.CTkFont(size=40),
                text_color="#DFCFC2"
            )
            placeholder.pack()
    
    def create_book_image(self, parent):
        try:
            image_path = "./assets/asset4.png"
            if os.path.exists(image_path):
                book_image = Image.open(image_path)
                book_ctk_image = ctk.CTkImage(
                    light_image=book_image,
                    dark_image=book_image,
                    size=(90, 100)
                )
                image_label = ctk.CTkLabel(
                    parent,
                    image=book_ctk_image,
                    text=""
                )
                image_label.pack()
        except Exception as e:
            placeholder = ctk.CTkLabel(
                parent,
                text="Book",
                font=ctk.CTkFont(size=50),
                text_color="#DFCFC2"
            )
            placeholder.pack()
    
    def show_summary(self, name):
            print(f"Showing summary for {name}")
            self.navigate_callback("summary")
            
    def view_cv(self, name):
        print(f"Viewing CV for {name}")
        self.navigate_callback("cv")