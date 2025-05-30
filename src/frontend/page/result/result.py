# src/frontend/page/result/result.py
import customtkinter as ctk
from PIL import Image
import os

class ResultPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager, search_results=None, **kwargs): # Added **kwargs
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0,
            **kwargs # Pass kwargs to super
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager 
        self.search_results_data = search_results if search_results else {"results": []} 
        self.pack(fill="both", expand=True)
        
        self.setup_result_page()
    
    def setup_result_page(self):
       
        page_main_container = ctk.CTkFrame(self, fg_color="transparent")
        page_main_container.pack(fill="both", expand=True, padx=30, pady=20) # 
        
        back_button_frame = ctk.CTkFrame(page_main_container, fg_color="transparent")
        back_button_frame.pack(fill="x", pady=(0, 10)) 
        self.create_back_button(back_button_frame)

        
        self.header_display_frame = ctk.CTkFrame(page_main_container, fg_color="transparent")
        self.header_display_frame.pack(fill="x", pady=(0, 15)) 
        self.create_header_section(self.header_display_frame) 

       
        self.scrollable_results_area = ctk.CTkScrollableFrame(
            page_main_container, 
            fg_color="transparent", 
            scrollbar_button_color="#334D7A", 
            scrollbar_button_hover_color="#4A5D8A"
        )
        self.scrollable_results_area.pack(fill="both", expand=True)

        
        self.create_results_grid(self.scrollable_results_area)
    
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
        back_button.pack(anchor="nw") # Tombol kembali di kiri atas frame-nya
    
    def create_header_section(self, parent): 

        
        header_content = ctk.CTkFrame(parent, fg_color="transparent") 
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
        
        num_results = len(self.search_results_data.get("results", []))
        exact_time = self.search_results_data.get("exact_match_time_ms", 0)
        fuzzy_time = self.search_results_data.get("fuzzy_match_time_ms", 0)

        description_text = (f"The search is complete! {num_results} candidate(s) found.\n"
                            f"Exact match time: {exact_time:.2f} ms, Fuzzy match time: {fuzzy_time:.2f} ms.\n"
                            "The most promising profiles are now on your desk.")

        if num_results == 0:
            description_text = "No candidates found matching your criteria."

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

    def create_results_grid(self, parent_scrollable_frame): 

        results_organizer = ctk.CTkFrame(parent_scrollable_frame, fg_color="transparent")
        results_organizer.pack(fill="x", expand=False, padx=10, pady=5) 

        actual_results = self.search_results_data.get("results", [])

        if not actual_results:
            no_results_label = ctk.CTkLabel(
                results_organizer, 
                text="No matching CVs found.",
                font=ctk.CTkFont(size=18),
                text_color="#FFFFFF"
            )
            no_results_label.pack(pady=50, expand=True) 
            return
        
        max_cols = 3
        

        cards_grid_container = ctk.CTkFrame(results_organizer, fg_color="transparent")
        cards_grid_container.pack(anchor="n") # Anchor ke atas

        row_frame = None
        for i, result_item in enumerate(actual_results):
            if i % max_cols == 0:
                
                row_frame = ctk.CTkFrame(cards_grid_container, fg_color="transparent")
                row_frame.pack(fill="x", pady=5, anchor="n") 
                
                for col_idx in range(max_cols):
                    
                    row_frame.grid_columnconfigure(col_idx, weight=1, minsize=280) 

            card_frame = ctk.CTkFrame(
                row_frame, # Tambahkan kartu ke row_frame saat ini
                fg_color="#DFCFC2",
                corner_radius=15,
                width=280,  # Lebar kartu bisa disesuaikan
                height=280  # Tinggi kartu bisa disesuaikan
            )
            
            card_frame.grid(row=0, column=(i % max_cols), padx=10, pady=10, sticky="nsew") # sticky agar mengisi sel grid
            card_frame.pack_propagate(False) 
            
            self.create_result_card(card_frame, result_item)
    


    def create_result_card(self, parent, result):
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15) # Adjusted padding
        
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10)) # Adjusted padding
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=result.get("name", "N/A"),
            font=ctk.CTkFont(size=16, weight="bold"), # Adjusted font size
            text_color="#1B2B4C"
        )
        name_label.pack(side="left", anchor="w") # Anchor to west
        
        total_occurrences = result.get("total_occurrences", 0) 
        matches_text = f"{total_occurrences} exact matches"
        if total_occurrences == 0 and result.get('fuzzy_keywords'):
            highest_similarity = result.get('highest_fuzzy_similarity', 0.0)
            matches_text = f"~{highest_similarity:.0f}% fuzzy" # Shorter text
        elif total_occurrences == 0 and not result.get('fuzzy_keywords') and not result.get('matched_keywords'): 
            matches_text = "No matches"

        matches_label = ctk.CTkLabel(
            header_frame,
            text=matches_text,
            font=ctk.CTkFont(size=12), # Adjusted font size
            text_color="#334D7A" # Different color for emphasis
        )
        matches_label.pack(side="right", anchor="e") # Anchor to east

        keywords_outer_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        keywords_outer_frame.pack(fill="both", expand=True, pady=(0,10))
        
        
        keywords_scroll_frame = ctk.CTkScrollableFrame(keywords_outer_frame, fg_color="#F0F0F0", height=80, corner_radius=6) # Lighter background for scroll area
        keywords_scroll_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        exact_keywords = result.get("matched_keywords", {})
        if exact_keywords:
            exact_title = ctk.CTkLabel(keywords_scroll_frame, text="Exact:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#1B2B4C")
            exact_title.pack(anchor="w", padx=5)
            for keyword, count in exact_keywords.items():
                keyword_text = f"- {keyword} ({count})"
                keyword_label = ctk.CTkLabel(keywords_scroll_frame, text=keyword_text, font=ctk.CTkFont(size=10), text_color="#1B2B4C") # Smaller font
                keyword_label.pack(anchor="w", padx=10)

        fuzzy_keywords_info = result.get("fuzzy_keywords", {})
        if fuzzy_keywords_info:
            fuzzy_threshold_display = "N/A" 
            try:
                from backend import Settings 
                fuzzy_threshold_display = Settings.FUZZY_THRESHOLD
            except ImportError:
                pass # Silently fail or use a default

            fuzzy_title = ctk.CTkLabel(keywords_scroll_frame, text=f"Fuzzy (> {fuzzy_threshold_display}%):", font=ctk.CTkFont(size=11, weight="bold"), text_color="#1B2B4C")
            fuzzy_title.pack(anchor="w", pady=(5,0), padx=5)
            for keyword, similarity in fuzzy_keywords_info.items():
                keyword_text = f"- {keyword} (~{similarity:.0f}%)"
                keyword_label = ctk.CTkLabel(keywords_scroll_frame, text=keyword_text, font=ctk.CTkFont(size=10), text_color="#1B2B4C") # Smaller font
                keyword_label.pack(anchor="w", padx=10)

        if not exact_keywords and not fuzzy_keywords_info:
            no_keywords_label = ctk.CTkLabel(keywords_scroll_frame, text="No specific keywords matched.", font=ctk.CTkFont(size=10), text_color="#1B2B4C")
            no_keywords_label.pack(anchor="center", expand=True) # Center if no keywords

        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", side="bottom", pady=(5,0)) # Ensure it's at the bottom
                
        summary_button = ctk.CTkButton(
            buttons_frame, text="Summary", font=ctk.CTkFont(size=12, weight="normal"), # Adjusted size
            width=90, height=28, corner_radius=6, border_width=1, border_color="#334D7A", 
            fg_color="#334D7A", hover_color="#1B2B4C", text_color="#DFCFC2",
            command=lambda app_id=result.get("applicant_id"): self.show_summary(app_id)
            )
        summary_button.pack(side="left", expand=True, padx=(0,5))
                
        view_cv_button = ctk.CTkButton(
            buttons_frame, text="View CV", font=ctk.CTkFont(size=12, weight="normal"), # Adjusted size
            width=90, height=28, corner_radius=6, border_width=1, border_color="#334D7A", 
            fg_color="#334D7A", hover_color="#1B2B4C", text_color="#DFCFC2",
            command=lambda app_id=result.get("applicant_id"): self.view_cv(app_id)
            )
        view_cv_button.pack(side="right", expand=True, padx=(5,0))

    def show_summary(self, applicant_id):
            if applicant_id is None:
                print("Error: Applicant ID is None for summary.")
                return
            print(f"Showing summary for Applicant ID: {applicant_id}")
            self.navigate_callback("summary", applicant_id=applicant_id)
            
    def view_cv(self, applicant_id):
        if applicant_id is None:
            print("Error: Applicant ID is None for CV view.")
            return
        print(f"Viewing CV for Applicant ID: {applicant_id}")
        self.navigate_callback("cv", applicant_id=applicant_id)

    def create_hat_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset2.png")
            if not os.path.exists(image_path): image_path = "./assets/asset2.png" # Fallback

            if os.path.exists(image_path):
                hat_image = Image.open(image_path)
                hat_ctk_image = ctk.CTkImage(light_image=hat_image, dark_image=hat_image, size=(100, 95))
                image_label = ctk.CTkLabel(parent, image=hat_ctk_image, text="")
                image_label.pack()
            else: raise FileNotFoundError("Hat image not found")
        except Exception as e:
            print(f"Error loading asset2.png (hat): {e}")
            ctk.CTkLabel(parent, text="🎩", font=ctk.CTkFont(size=40), text_color="#DFCFC2").pack()
    
    def create_book_image(self, parent):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "..", "..", "assets", "asset4.png")
            if not os.path.exists(image_path): image_path = "./assets/asset4.png" # Fallback

            if os.path.exists(image_path):
                book_image = Image.open(image_path)
                book_ctk_image = ctk.CTkImage(light_image=book_image, dark_image=book_image, size=(90, 100))
                image_label = ctk.CTkLabel(parent, image=book_ctk_image, text="")
                image_label.pack()
            else: raise FileNotFoundError("Book image not found")
        except Exception as e:
            print(f"Error loading asset4.png (book): {e}")
            ctk.CTkLabel(parent, text="📖", font=ctk.CTkFont(size=50), text_color="#DFCFC2").pack()


    def show_summary(self, applicant_id):
            if applicant_id is None:
                print("Error: Applicant ID is None for summary.")
                return
            print(f"Showing summary for Applicant ID: {applicant_id}")
            self.navigate_callback("summary", applicant_id=applicant_id)
            
    def view_cv(self, applicant_id):
        if applicant_id is None:
            print("Error: Applicant ID is None for CV view.")
            return
        print(f"Viewing CV for Applicant ID: {applicant_id}")
        self.navigate_callback("cv", applicant_id=applicant_id) # Pass applicant_id