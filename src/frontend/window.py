import customtkinter as ctk
import os
import sys

current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from components.sidebar import Sidebar
from page.home import HomePage
from page.about import AboutPage
from page.creator import CreatorPage

class VitaeLangXWindow:
    """Main application window for VitaeLangX - Window management only"""
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("VitaeLangX")
        self.root.attributes("-fullscreen", True)
        self.root.configure(fg_color="#1B2B4C")
        
        self.current_page = None
        self.setup_layout()
        
    def setup_layout(self):
        """Setup main layout with sidebar and content area"""
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        self.sidebar = Sidebar(self.main_container, self.navigate_to_page)
        self.sidebar.pack(side="left", fill="y")
        
        self.content_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color="#1B2B4C",
            corner_radius=0
        )
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        self.navigate_to_page("home")
    
    def navigate_to_page(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.sidebar.set_active_page(page_name)
        
        if page_name == "home":
            self.current_page = HomePage(self.content_frame, self.navigate_to_page)
        elif page_name == "about":
            self.current_page = AboutPage(self.content_frame, self.navigate_to_page)
        elif page_name == "creator":
            self.current_page = CreatorPage(self.content_frame, self.navigate_to_page)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VitaeLangXWindow()
    app.run()