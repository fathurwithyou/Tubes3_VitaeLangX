import customtkinter as ctk
import os
import sys

print(f"--- window.py ---")
print(f"Initial sys.path in window.py: {sys.path}")
print(f"Current Working Directory (from window.py): {os.getcwd()}")

# Dapatkan path absolut ke direktori 'src'
src_directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if src_directory_path not in sys.path:
    sys.path.insert(0, src_directory_path)

print(f"Modified sys.path in window.py (src should be first): {sys.path}")
print(f"--- end window.py sys.path debug ---")

# Impor backend setelah sys.path dimodifikasi
from backend import BackendManager, Settings

from components.sidebar import Sidebar
from page.home import HomePage
from page.about import AboutPage
from page.creator import CreatorPage
from page.opening.opening import OpeningPage
from page.search.search import SearchPage
from page.result.result import ResultPage
from page.cv.cv import CVPage
from page.summary.summary import SummaryPage

class VitaeLangXWindow:
    
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("VitaeLangX")
        self.root.attributes("-fullscreen", True)
        self.root.configure(fg_color="#1B2B4C")
        
        self.current_page = None #
        
        # 1. Inisialisasi atribut self.backend_manager ke None
        self.backend_manager = None
        
        # 2. Panggil metode untuk membuat dan menugaskan instance BackendManager
        self.initialize_app_backend() # Pastikan metode ini ada dan melakukan: self.backend_manager = BackendManager()
        
        # 3. SEKARANG baru panggil setup_layout, karena backend_manager sudah ada (atau None jika inisialisasi gagal)
        self.setup_layout() #
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing) #

        

    def initialize_app_backend(self):
        print("Initializing ATS Backend for GUI...") #
        
        # Path ke direktori data, relatif terhadap direktori 'src'
        # src_directory_path sudah didefinisikan di scope global modul ini
        project_root_data_dir = os.path.abspath(os.path.join(src_directory_path, 'tubes2/data')) #
        
        os.makedirs(project_root_data_dir, exist_ok=True) #
        
        # >>> BARIS KRUSIAL: Membuat instance dan menugaskannya ke self.backend_manager <<<
        self.backend_manager = BackendManager() #
        
        # Sekarang self.backend_manager adalah objek BackendManager
        # Anda bisa memanggil metodenya
        if self.backend_manager:
            self.backend_manager.initialize_backend(data_directory=project_root_data_dir) #
            print("Backend for GUI initialized.") #
        else:
            # Ini seharusnya tidak terjadi jika BackendManager() berhasil
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
            # Anda mungkin ingin menangani ini lebih lanjut, mis. dengan menampilkan error di UI
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
        page_specific_args = kwargs #
        current_page_args = {**common_args, **page_specific_args} #

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
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VitaeLangXWindow()
    app.run()