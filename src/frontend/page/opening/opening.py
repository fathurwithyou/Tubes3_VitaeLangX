import customtkinter as ctk
from PIL import Image
import os

class OpeningPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.pack(fill="both", expand=True)
        
        self.setup_opening_page()
    
    def setup_opening_page(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=50, pady=30)
        
        self.create_back_button(main_container)
        
        center_container = ctk.CTkFrame(main_container, fg_color="transparent")
        center_container.pack(expand=True)
        
        self.create_opening_content(center_container)
    
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
            command=lambda: self.navigate_callback("home")
        )
        back_button.pack(anchor="nw", pady=(0, 0)) 
    
    def create_opening_content(self, parent):
        content_frame = ctk.CTkFrame(
            parent,
            fg_color="#DFCFC2",
            corner_radius=20,
            border_width=3,
            border_color="#DFCFC2"
        )
        content_frame.pack(expand=True, fill="both", padx=50, pady=(50, 20))
        
        inner_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        inner_container.pack(expand=True, fill="both", padx=70, pady=50)
        
        content_section = ctk.CTkFrame(inner_container, fg_color="transparent")
        content_section.pack(expand=True, fill="both")
        
        left_section = ctk.CTkFrame(content_section, fg_color="transparent")
        left_section.pack(side="left", fill="both", expand=True)
        
        self.create_bearlock_image(left_section)
        
        right_section = ctk.CTkFrame(content_section, fg_color="transparent")
        right_section.pack(side="right", fill="both", expand=True, padx=(20, 0))
        
        text_container = ctk.CTkFrame(right_section, fg_color="transparent")
        text_container.pack(expand=True)
        
        title_label = ctk.CTkLabel(
            text_container,
            text="Find the Perfect Match in a Snap!",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#334D7A"
        )
        title_label.pack(pady=(0, 20), expand=True)
        
        description_text = """Welcome to your intelligent assistant for keyword-based CV matching. Whether you're a recruiter or a researcher, this is your starting point for smart talent discovery."""
        
        description_label = ctk.CTkLabel(
            text_container,
            text=description_text,
            font=ctk.CTkFont(size=14),
            text_color="#000000",
            wraplength=400,
            justify="center"
        )
        description_label.pack(expand=True)
        
        self.create_action_button(parent)
    
    def create_bearlock_image(self, parent):
        image_container = ctk.CTkFrame(parent, fg_color="transparent")
        image_container.pack(expand=True)
        
        bearlock_image = self.load_bearlock_image(image_container)
        if bearlock_image:
            bearlock_image.pack(expand=True)
        else:
            placeholder = ctk.CTkFrame(
                image_container,
                width=250,
                height=300,
                fg_color="#2D3E5F",
                corner_radius=15
            )
            placeholder.pack(expand=True)
            placeholder.pack_propagate(False)
            
            placeholder_label = ctk.CTkLabel(
                placeholder,
                text="Bearlock\nHolmes",
                font=ctk.CTkFont(size=24),
                text_color="#FFFFFF",
                justify="center"
            )
            placeholder_label.pack(expand=True)
    

    
    def create_action_button(self, parent):
        button_container = ctk.CTkFrame(parent, fg_color="transparent")
        button_container.pack(pady=(20, 0))
        
        action_button = ctk.CTkButton(
            button_container,
            text="Rawwwwrrr",
            font=ctk.CTkFont(size=16, weight="normal"),
            width=200,
            height=45,
            corner_radius=8,
            border_width=2,
            border_color="#DFCFC2", 
            fg_color="#334D7A",
            hover_color="#1B2B4C", 
            text_color="#DFCFC2",
            command=self.proceed_to_search
        )
        action_button.pack()
    
    def load_bearlock_image(self, parent):
        try:
            image_path = "./assets/bearlock.png"
            
            if os.path.exists(image_path):
                bearlock_image = Image.open(image_path)
                
                bearlock_ctk_image = ctk.CTkImage(
                    light_image=bearlock_image,
                    dark_image=bearlock_image,
                    size=(200, 200)
                )
                
                image_label = ctk.CTkLabel(
                    parent,
                    image=bearlock_ctk_image,
                    text=""
                )
                
                return image_label
                
        except Exception as e:
            print(f"Error loading bearlock image: {e}")
            
        return None
    
    def proceed_to_search(self):
        print("Proceeding to main search interface...")
        self.navigate_callback("search")