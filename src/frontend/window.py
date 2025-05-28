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
from page.opening.opening import OpeningPage
from page.search.search import SearchPage
from page.result.result import ResultPage

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
        
        # Create sidebar (will be hidden for opening and search pages)
        self.sidebar = Sidebar(self.main_container, self.navigate_to_page)
        self.sidebar.pack(side="left", fill="y")
        
        # Create content frame
        self.content_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color="#1B2B4C",
            corner_radius=0
        )
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Start with home page
        self.navigate_to_page("home")
    
    def navigate_to_page(self, page_name):
        """Navigate to different pages and manage sidebar visibility"""
        # Clear current content first
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Handle layout based on page type
        if page_name in ["opening", "search", "result"]:
            # Hide sidebar and reconfigure for full screen
            self.sidebar.pack_forget()
            self.content_frame.pack_forget()
            self.content_frame.pack(fill="both", expand=True)
        else:
            # Ensure proper layout for pages with sidebar
            self.content_frame.pack_forget()
            self.sidebar.pack_forget()
            
            # Repack in correct order
            self.sidebar.pack(side="left", fill="y")
            self.content_frame.pack(side="right", fill="both", expand=True)
            
            # Update sidebar active state
            self.sidebar.set_active_page(page_name)
        
        # Force layout update before creating page
        self.main_container.update_idletasks()
        
        # Create the appropriate page
        if page_name == "home":
            self.current_page = HomePage(self.content_frame, self.navigate_to_page)
        elif page_name == "about":
            self.current_page = AboutPage(self.content_frame, self.navigate_to_page)
        elif page_name == "creator":
            self.current_page = CreatorPage(self.content_frame, self.navigate_to_page)
        elif page_name == "opening":
            self.current_page = OpeningPage(self.content_frame, self.navigate_to_page)
        elif page_name == "search":
            self.current_page = SearchPage(self.content_frame, self.navigate_to_page)
        elif page_name == "result":
            self.current_page = ResultPage(self.content_frame, self.navigate_to_page)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VitaeLangXWindow()
    app.run()