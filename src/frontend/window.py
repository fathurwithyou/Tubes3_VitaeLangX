import customtkinter as ctk

from backend import BackendManager, Settings

from .components import *
from .page import *

class VitaeLangXWindow:
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("VitaeLangX")
        self.root.attributes("-fullscreen", True)
        self.root.configure(fg_color="#1B2B4C")
        
        self.current_page = None 
        
        self.backend_manager = None
        self.initialize_app_backend() 
        self.setup_layout() 
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) #

        

    def initialize_app_backend(self):
        print("Initializing ATS Backend for GUI...") 
        self.backend_manager = BackendManager() 
    
        if self.backend_manager:
            self.backend_manager.initialize_backend() 
            print("Backend for GUI initialized.") 
        else:
            print("CRITICAL ERROR: BackendManager could not be instantiated in initialize_app_backend.")

    

    def on_closing(self):
        if self.backend_manager:
            print("Shutting down backend...")
            self.backend_manager.shutdown_backend()
        self.root.destroy()

    def setup_layout(self):
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
    
    def navigate_to_page(self, page_name, **kwargs):
        if self.backend_manager is None:
            print("ERROR in navigate_to_page: backend_manager is None. Initialization might have failed.")
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            error_label = ctk.CTkLabel(self.content_frame, text="Critical Error: Backend not available.", font=ctk.CTkFont(size=20))
            error_label.pack(expand=True, padx=20, pady=20)
            return
           
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if page_name in ["opening", "search", "result", "cv", "summary"]:
            self.sidebar.pack_forget()
            self.content_frame.pack_forget()
            self.content_frame.pack(fill="both", expand=True)
        else:
            self.content_frame.pack_forget()
            self.sidebar.pack_forget()
            
            self.sidebar.pack(side="left", fill="y")
            self.content_frame.pack(side="right", fill="both", expand=True)
            
            self.sidebar.set_active_page(page_name)
        
        self.main_container.update_idletasks()

        common_args = {"parent": self.content_frame, "navigate_callback": self.navigate_to_page, "backend_manager": self.backend_manager} #
        page_specific_args = kwargs 
        current_page_args = {**common_args, **page_specific_args} 

        if page_name == "home":
            self.current_page = HomePage(self.content_frame, self.navigate_to_page)
        elif page_name == "about":
            self.current_page = AboutPage(self.content_frame, self.navigate_to_page)
        elif page_name == "creator":
            self.current_page = CreatorPage(self.content_frame, self.navigate_to_page)
        elif page_name == "opening":
            self.current_page = OpeningPage(self.content_frame, self.navigate_to_page)
        elif page_name == "search":
            self.current_page = SearchPage(**current_page_args)
        elif page_name == "result":
            self.current_page = ResultPage(**current_page_args)
        elif page_name == "cv":
            self.current_page = CVPage(**current_page_args)
        elif page_name == "summary":
            self.current_page = SummaryPage(**current_page_args)
        else:
            print(f"Warning: Unknown page name '{page_name}' in navigate_to_page.")
            self.current_page = HomePage(self.content_frame, self.navigate_to_page)
            if self.sidebar.winfo_ismapped(): 
                self.sidebar.set_active_page("home")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VitaeLangXWindow()
    app.run()