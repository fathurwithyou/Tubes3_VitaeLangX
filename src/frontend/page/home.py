import customtkinter as ctk
from PIL import Image
import os

class HomePage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback):
        super().__init__(
            parent,
            fg_color="#1B2B4C", 
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.pack(fill="both", expand=True)
        
        self.setup_home_page()
    
    def setup_home_page(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(expand=True, fill="both")
        
        hero_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        hero_frame.pack(expand=True)
        
        self.create_hero_content(hero_frame)
    
    def create_hero_content(self, parent):
        self.create_hero_logo(parent)
        
        title_label = ctk.CTkLabel(
            parent,
            text="VitaeLangX",
            font=ctk.CTkFont(size=40, weight="bold"),
            text_color="#F9DFDC"  
        )
        title_label.pack(pady=(10, 10)) 
        
        subtitle_label = ctk.CTkLabel(
            parent,
            text="From Keywords to Candidates",
            font=ctk.CTkFont(size=14),
            text_color="#FFFFFF"
        )
        subtitle_label.pack(pady=(0, 20))
        
        self.create_search_button(parent)
    
    def create_hero_logo(self, parent):
        """Create hero logo (bigger version) - THIS FUNCTION WAS MISSING"""
        logo_container = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        logo_container.pack(pady=(20, 0))
        
        logo_widget = self.create_logo_widget(logo_container, size=(200, 200))  # Big logo for hero
        if logo_widget:
            logo_widget.pack()
    
    def create_logo_widget(self, parent, size=(200, 200)):
        
        try:
            logo_paths_to_try = [
                "assets/logo.png",  
                os.path.join(".", "assets", "logo.png"),
                os.path.join("..", "assets", "logo.png"),
                os.path.join("frontend", "assets", "logo.png"),
            ]
            
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                logo_paths_to_try.extend([
                    os.path.join(current_dir, "assets", "logo.png"),
                    os.path.join(current_dir, "..", "assets", "logo.png"),
                    os.path.join(current_dir, "..", "..", "assets", "logo.png"),
                ])
            except:
                pass
            
            for logo_path in logo_paths_to_try:
                
                if os.path.exists(logo_path):
                    
                    logo_image = Image.open(logo_path)
                    
                    logo_ctk_image = ctk.CTkImage(
                        light_image=logo_image,
                        dark_image=logo_image,
                        size=size 
                    )
                    
                    logo_label = ctk.CTkLabel(
                        parent,
                        image=logo_ctk_image,
                        text=""  
                    )
                    
                    return logo_label
            
            raise FileNotFoundError(f"Logo not found at any expected locations")
                
        except Exception as e:
            logo_label = ctk.CTkLabel(
                parent,
                text="VitaeLangX",
                font=ctk.CTkFont(size=48) 
            )
            return logo_label
    
    def create_search_button(self, parent):
        search_button = ctk.CTkButton(
            parent,
            text="Start the Search",
            font=ctk.CTkFont(size=16, weight="normal"),
            width=200,
            height=45,
            corner_radius=8,
            border_width=2,
            border_color="#F9DFDC", 
            fg_color="#334D7A",
            hover_color="#1B2B4C", 
            text_color="#F9DFDC", 
            command=self.start_search
        )
        search_button.pack(pady=20)
        
        self.bind_button_hover_effects(search_button)
    
    def bind_button_hover_effects(self, button):
        def on_enter(event):
            button.configure(text_color="#FFFFFF")
        
        def on_leave(event):
            button.configure(text_color="#F9DFDC")
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def start_search(self):
        self.navigate_callback("opening")