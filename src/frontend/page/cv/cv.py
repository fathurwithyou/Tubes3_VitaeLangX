# src/frontend/page/cv/cv.py
import customtkinter as ctk
from PIL import Image
import os

class CVPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager, applicant_id, cv_path=None, **kwargs): # Add cv_path
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0,
            **kwargs
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager
        self.applicant_id = applicant_id # Still needed for profile info like name
        self.cv_path_to_load = cv_path   # Store the specific CV path
        self.candidate_name = "N/A" 
        self.cv_content_text = "CV content not available."
        
        self.pack(fill="both", expand=True)
        
        self._load_data_and_setup_ui()

    def _load_data_and_setup_ui(self):
        if self.applicant_id is None and self.cv_path_to_load is None: # Adjusted condition
            print("ERROR (CVPage): Applicant ID and CV Path are None.")
            self._display_error_message("No applicant or CV information to display.")
            return

        # Fetch applicant profile for name (still uses applicant_id if available)
        if self.applicant_id:
            profile_data = self.backend_manager._get_applicant_profile(self.applicant_id) #
            if profile_data and "error" not in profile_data:
                first_name = profile_data.get('first_name', '')
                last_name = profile_data.get('last_name', '')
                self.candidate_name = f"{first_name} {last_name}".strip() if (first_name or last_name) else "Candidate"
            else:
                error_msg = profile_data.get('error', 'Unknown error') if profile_data else 'Unknown error fetching profile'
                print(f"Error fetching profile for CVPage: {error_msg}")
                self.candidate_name = "Candidate (Profile Error)"
        else:
             self.candidate_name = "Candidate (Unknown Profile)"


        # Fetch CV text USING THE PASSED CV_PATH
        cv_text_result = ""
        if self.cv_path_to_load:
            print(f"CVPage: Loading CV from specific path: {self.cv_path_to_load}")
            if not os.path.exists(self.cv_path_to_load): #
                cv_text_result = f"CV file not found at specified path: {self.cv_path_to_load}"
            else:
                # Use the cv_processor directly from backend_manager to load text from a specific path
                cv_text_result = self.backend_manager.cv_processor.extract_text_from_pdf(self.cv_path_to_load) #
        elif self.applicant_id: # Fallback if cv_path_to_load wasn't passed but applicant_id was
            print(f"CVPage: No specific CV path provided, falling back to applicant_id {self.applicant_id} to derive path.")
            cv_text_result = self.backend_manager.get_full_cv_text(self.applicant_id) #
        else:
            cv_text_result = "Cannot load CV: No CV path or Applicant ID provided."
            
        # Updated error checking
        if not cv_text_result or \
           "CV file not found" in cv_text_result or \
           ("Could not extract text" in cv_text_result and not cv_text_result.strip() == "Could not extract text from CV.") : # Be more specific if backend returns this exact string for failure
            
            error_message_to_display = cv_text_result if cv_text_result else "CV content is empty or could not be loaded."
            print(f"ERROR/Warning (CVPage): {error_message_to_display}")
            self._display_error_message(f"Failed to load CV: {error_message_to_display}")
            return
        else:
            self.cv_content_text = cv_text_result

        self.setup_cv_page()

    # ... (rest of CVPage methods: _display_error_message, setup_cv_page, create_back_button, create_header_section, create_cv_content, image loading) ...
    # Ensure create_header_section uses self.candidate_name
    # Ensure create_cv_content uses self.cv_content_text

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
        for widget in self.winfo_children(): 
            widget.destroy()
            
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
        header_container.pack(fill="x", pady=(0, 20)) 
        
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
        cv_scrollable.pack(fill="both", expand=True, padx=20, pady=20) 
        
        cv_text_label = ctk.CTkLabel(
            cv_scrollable,
            text=self.cv_content_text, 
            font=ctk.CTkFont(size=12), 
            text_color="#000000",
            justify="left",
            anchor="nw",
        )
        # Update wraplength after the widget is drawn and has a width
        cv_scrollable.update_idletasks() 
        cv_text_label.configure(wraplength=cv_scrollable.winfo_width() - 40) # -40 for padding
        cv_text_label.pack(fill="both", expand=True)
   
    def create_bearlock_happy_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "bearlock-happy.png")
            if not os.path.exists(image_path): image_path = "./assets/bearlock-happy.png"
            if os.path.exists(image_path):
                bearlock_image = Image.open(image_path)
                bearlock_ctk_image = ctk.CTkImage(light_image=bearlock_image, dark_image=bearlock_image, size=(120, 120))
                image_label = ctk.CTkLabel(parent, image=bearlock_ctk_image, text="")
                image_label.pack()
            else: raise FileNotFoundError("Bearlock happy image not found")
        except Exception as e:
            print(f"Error loading bearlock-happy.png: {e}")
            ctk.CTkLabel(parent, text="🐻😊", font=ctk.CTkFont(size=50), text_color="#DFCFC2").pack()
    
    def create_asset1_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset1.png")
            if not os.path.exists(image_path): image_path = "./assets/asset1.png"
            if os.path.exists(image_path):
                asset_image = Image.open(image_path)
                asset_ctk_image = ctk.CTkImage(light_image=asset_image, dark_image=asset_image, size=(80, 80))
                image_label = ctk.CTkLabel(parent, image=asset_ctk_image, text="")
                image_label.pack()
            else: raise FileNotFoundError("Asset1 image not found")
        except Exception as e:
            print(f"Error loading asset1.png: {e}")
            ctk.CTkLabel(parent, text="📄", font=ctk.CTkFont(size=50), text_color="#DFCFC2").pack()