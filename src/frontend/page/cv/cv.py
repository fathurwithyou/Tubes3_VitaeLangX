# src/frontend/page/cv/cv.py
import customtkinter as ctk
from PIL import Image
import os

class CVPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager, applicant_id, **kwargs):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0,
            **kwargs
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager
        self.applicant_id = applicant_id
        self.candidate_name = "N/A" # Default before loading
        self.cv_content_text = "CV content not available." # Default before loading
        
        self.pack(fill="both", expand=True)
        
        self._load_data_and_setup_ui()

    def _load_data_and_setup_ui(self):
        if self.applicant_id is None:
            print("ERROR (CVPage): Applicant ID is None.")
            self._display_error_message("No applicant information to display CV.")
            return

        # Fetch applicant profile for name
        profile_data = self.backend_manager._get_applicant_profile(self.applicant_id) #
        if profile_data and "error" not in profile_data:
            first_name = profile_data.get('first_name', '')
            last_name = profile_data.get('last_name', '')
            self.candidate_name = f"{first_name} {last_name}".strip() if (first_name or last_name) else "Candidate"
        else:
            self.candidate_name = "Candidate (Error)"
            print(f"Error fetching profile for CVPage: {profile_data.get('error') if profile_data else 'Unknown error'}")
            
        # Fetch CV text
        self.cv_content_text = self.backend_manager.get_full_cv_text(self.applicant_id) #
        if not self.cv_content_text or "Could not extract text" in self.cv_content_text or "CV file not found" in self.cv_content_text :
             print(f"Warning/Error (CVPage): {self.cv_content_text}")
             # Keep the default error message or the one from backend

        self.setup_cv_page()

    def _display_error_message(self, message):
        for widget in self.winfo_children():
            widget.destroy()
        
        error_label = ctk.CTkLabel(
            self,
            text=message,
            font=ctk.CTkFont(size=18),
            text_color="tomato"
        )
        error_label.pack(expand=True, padx=20, pady=20)

        back_button = ctk.CTkButton(
            self,
            text="← Back to Results",
            font=ctk.CTkFont(size=16),
            width=150,
            height=40,
            command=lambda: self.navigate_callback("result")
        )
        back_button.pack(pady=20)
            
    def setup_cv_page(self):
        for widget in self.winfo_children(): # Clear previous content if any (e.g. error message)
            widget.destroy()
            
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=50, pady=30)
        
        self.create_back_button(main_container)
        self.create_header_section(main_container) # This will now use the loaded candidate_name
        self.create_cv_content(main_container)   # This will now use the loaded cv_content_text
    
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
        back_button.pack(anchor="nw", pady=(0, 0)) # Removed extra pady
    
    def create_header_section(self, parent):
        header_container = ctk.CTkFrame(parent, fg_color="transparent")
        header_container.pack(fill="x", pady=(0, 20)) # Adjusted padding
        
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
        header_content.pack(expand=True)
        
        left_image = ctk.CTkFrame(header_content, fg_color="transparent")
        left_image.pack(side="left", padx=(0, 25))
        self.create_bearlock_happy_image(left_image) # This can stay
        
        center_content = ctk.CTkFrame(header_content, fg_color="transparent")
        center_content.pack(side="left", expand=True)
        
        title_label = ctk.CTkLabel(
            center_content,
            text=f"Full Case File: {self.candidate_name}", # Dynamic name
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
        self.create_asset1_image(right_image) # This can stay
    
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
            fg_color="transparent", # Or "#FFFFFF" for white background for text
            corner_radius=0
        )
        cv_scrollable.pack(fill="both", expand=True, padx=20, pady=20) # Adjusted padding
        
        # cv_content is now self.cv_content_text fetched in _load_data_and_setup_ui
        
        cv_text_label = ctk.CTkLabel(
            cv_scrollable,
            text=self.cv_content_text, # Dynamic CV content
            font=ctk.CTkFont(size=12), # Adjusted size
            text_color="#000000",
            justify="left",
            anchor="nw",
            wraplength=cv_scrollable.winfo_width() - 20 # Make it wrap within the scrollable frame
        )
        cv_text_label.pack(fill="both", expand=True)

    # --- Image creation methods (can remain largely the same) ---
    def create_bearlock_happy_image(self, parent):
        # ... (implementation as provided, consider centralizing asset paths)
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "bearlock-happy.png")

            if not os.path.exists(image_path):
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
            else:
                raise FileNotFoundError("Bearlock happy image not found")
        except Exception as e:
            print(f"Error loading bearlock-happy.png: {e}")
            placeholder = ctk.CTkLabel(
                parent, text="🐻😊", font=ctk.CTkFont(size=50), text_color="#DFCFC2"
            )
            placeholder.pack()
    
    def create_asset1_image(self, parent):
        # ... (implementation as provided, consider centralizing asset paths)
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset1.png")
            
            if not os.path.exists(image_path):
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
            else:
                raise FileNotFoundError("Asset1 image not found")
        except Exception as e:
            print(f"Error loading asset1.png: {e}")
            placeholder = ctk.CTkLabel(
                parent, text="📄", font=ctk.CTkFont(size=50), text_color="#DFCFC2"
            )
            placeholder.pack()