import customtkinter as ctk
from PIL import Image
import os

class Sidebar(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback):
        super().__init__(
            parent,
            width=250,
            fg_color="#DFCFC2",  
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.current_active = "home"
        self.nav_buttons = {}
        
        self.pack_propagate(False)
        
        self.setup_sidebar()
    
    def setup_sidebar(self):
        """Setup sidebar header and navigation"""
        self.create_header()
        self.create_navigation()
    
    def create_header(self):
        """Create sidebar header with logo and title"""
        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=15, pady=(20, 20)) 

        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(anchor="w", fill="x")
        
        # Logo widget (no fallback)
        logo_widget = self.create_logo_widget(title_container)
        logo_widget.pack(side="left", padx=(0, 8))
        
        # App title
        title_label = ctk.CTkLabel(
            title_container,
            text="VitaeLangX",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#000000"  
        )
        title_label.pack(side="left")
    
    def create_logo_widget(self, parent):
        """Create logo widget from assets/logo.png"""
        # Try multiple paths for logo
        logo_paths = [
            "assets/logo.png",
            os.path.join(".", "assets", "logo.png"),
            os.path.join("..", "assets", "logo.png"),
            os.path.join("frontend", "assets", "logo.png"),
        ]
        
        # Add absolute paths
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logo_paths.extend([
                os.path.join(current_dir, "assets", "logo.png"),
                os.path.join(current_dir, "..", "assets", "logo.png"),
                os.path.join(current_dir, "..", "..", "assets", "logo.png"),
            ])
        except:
            pass
        
        # Try each path
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                
                logo_ctk_image = ctk.CTkImage(
                    light_image=logo_image,
                    dark_image=logo_image,
                    size=(32, 32)
                )
                
                logo_label = ctk.CTkLabel(
                    parent,
                    image=logo_ctk_image,
                    text=""
                )
                
                return logo_label
    
    def create_navigation(self):
        """Create navigation buttons"""
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, padx=15, pady=(0, 20))
        
        nav_container = ctk.CTkFrame(nav_frame, fg_color="transparent")
        nav_container.pack(anchor="n", fill="x")
        
        nav_items = [
            ("Home", "home"),
            ("About", "about"),
            ("Creator", "creator")
        ]
        
        for text, page_name in nav_items:
            self.create_nav_button(nav_container, text, page_name)
    
    def create_nav_button(self, parent, text, page_name):
        """Create individual navigation button"""
        is_active = page_name == self.current_active
        
        if is_active:
            button = ctk.CTkButton(
                parent,
                text=text,
                font=ctk.CTkFont(size=16, weight="normal"),
                height=45,
                corner_radius=10,
                border_width=2,
                border_color="#F9DFDC",
                fg_color="#334D7A",
                hover_color="#334D7A",
                text_color="#FFFFFF",
                command=lambda p=page_name: self.on_nav_click(p),
                anchor="w"
            )
        else:
            button = ctk.CTkButton(
                parent,
                text=text,
                font=ctk.CTkFont(size=16, weight="normal"),
                height=45,
                corner_radius=10,
                border_width=0,
                fg_color="transparent",
                hover_color="#334D7A",
                text_color="#000000",
                command=lambda p=page_name: self.on_nav_click(p),
                anchor="w"
            )
        
        button.pack(fill="x", pady=3)
        self.nav_buttons[page_name] = button
        
        self.bind_hover_effects(button, page_name)
    
    def bind_hover_effects(self, button, page_name):
        """Add hover effects to navigation buttons"""
        def on_enter(event):
            if page_name != self.current_active:
                button.configure(text_color="#334D7A")
        
        def on_leave(event):
            if page_name != self.current_active:
                button.configure(text_color="#000000")
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def on_nav_click(self, page_name):
        """Handle navigation button click"""
        self.current_active = page_name
        self.navigate_callback(page_name)
    
    def set_active_page(self, page_name):
        """Set active page and update button styles"""
        self.current_active = page_name
        
        for btn_page, button in self.nav_buttons.items():
            is_active = btn_page == page_name
            
            if is_active:
                button.configure(
                    border_width=2,
                    border_color="#F9DFDC",
                    fg_color="#334D7A",
                    text_color="#FFFFFF"
                )
            else:
                button.configure(
                    border_width=0,
                    fg_color="transparent",
                    text_color="#000000"
                )