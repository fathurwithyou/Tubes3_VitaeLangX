import customtkinter as ctk
from PIL import Image
import os

class ResultPage(ctk.CTkFrame):
    
    def __init__(self, parent, navigate_callback, backend_manager, search_results=None):
        super().__init__(
            parent,
            fg_color="#1B2B4C",
            corner_radius=0
        )
        
        self.navigate_callback = navigate_callback
        self.backend_manager = backend_manager # Store backend_manager
        self.search_results_data = search_results if search_results else {"results": []} # Store results, handle None
        self.pack(fill="both", expand=True)
        
        self.setup_result_page()
    
    def setup_result_page(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        self.create_back_button(main_container)
        
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.place(relx=0.5, rely=0.5, anchor="center")
        
        self.create_header_section(content_container)
        
        self.create_results_grid(content_container)
    
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
        back_button.place(x=50, y=30) 
    
    def create_header_section(self, parent):
        header_container = ctk.CTkFrame(parent, fg_color="transparent")
        header_container.pack(pady=(0, 20))
        
        header_content = ctk.CTkFrame(header_container, fg_color="transparent")
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
        
        num_results = len(self.search_results_data.get("results", [])) #
        exact_time = self.search_results_data.get("exact_match_time_ms", 0) #
        fuzzy_time = self.search_results_data.get("fuzzy_match_time_ms", 0) #

        description_text = (f"The search is complete! {num_results} candidate(s) found.\n"
                            f"Exact match time: {exact_time:.2f} ms, Fuzzy match time: {fuzzy_time:.2f} ms.\n"
                            "The most promising profiles are now on your desk.")

        if num_results == 0: #
            description_text = "No candidates found matching your criteria." #

        description_label = ctk.CTkLabel( #
            center_content, #
            text=description_text, #
            # ... sisa parameter ...
        )
        description_label.pack(pady=(10, 0)) #
        
        right_image = ctk.CTkFrame(header_content, fg_color="transparent")
        right_image.pack(side="right", padx=(20, 0))
        self.create_book_image(right_image)
    


    def create_results_grid(self, parent):
        results_container = ctk.CTkFrame(parent, fg_color="transparent")
        results_container.pack(fill="both", expand=True, pady=(0, 20), padx=20)
        
        # cards_frame = ctk.CTkFrame(results_container, fg_color="transparent")
        # cards_frame.pack()  
        
        # dummy_results = [
        #     {
        #         "name": "Fathur",
        #         "total_matches": 4,
        #         "keywords": {
        #             "React": 1,
        #             "Express": 2,
        #             "HTML": 1
        #         }
        #     },
        #     {
        #         "name": "Fathur", 
        #         "total_matches": 4,
        #         "keywords": {
        #             "React": 1,
        #             "Express": 2,
        #             "HTML": 1
        #         }
        #     },
        #     {
        #         "name": "Fathur",
        #         "total_matches": 4,
        #         "keywords": {
        #             "React": 1,
        #             "Express": 2,
        #             "HTML": 1
        #         }
        #     }
        # ]
        
        actual_results = self.search_results_data.get("results", [])

        if not actual_results:
            no_results_label = ctk.CTkLabel(
                results_container,
                text="No matching CVs found.",
                font=ctk.CTkFont(size=18),
                text_color="#FFFFFF"
            )
            no_results_label.pack(pady=50)
            return
        
        max_cols = 3  # Tentukan jumlah kolom maksimal per baris
        row_frame = None #

        for i, result_item in enumerate(actual_results): #
            if i % max_cols == 0: # Sekarang max_cols sudah terdefinisi
                row_frame = ctk.CTkFrame(results_container, fg_color="transparent") #
                row_frame.pack(fill="x", pady=10, anchor="n") # anchor="n" agar baris baru tidak menumpuk di tengah jika tidak penuh
                # Konfigurasi kolom agar kartu di dalamnya memiliki lebar yang sama dan merata
                for col_idx in range(max_cols):
                    row_frame.grid_columnconfigure(col_idx, weight=1, uniform="card_column")


            card_frame = ctk.CTkFrame( #
                row_frame, # Tambahkan kartu ke row_frame saat ini
                fg_color="#DFCFC2", #
                corner_radius=15, #
                width=300,  # Anda bisa atur lebar kartu
                height=300  # Anda bisa atur tinggi kartu
            )
            # Gunakan grid untuk menempatkan kartu di dalam row_frame
            card_frame.grid(row=0, column=(i % max_cols), padx=15, pady=10, sticky="nsew")
            card_frame.pack_propagate(False) #
            
            self.create_result_card(card_frame, result_item) #
    
    def create_result_card(self, parent, result): # Parameter Anda adalah 'result'
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=result.get("name", "N/A"),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#1B2B4C"
        )
        name_label.pack(side="left")
        
        # --- HANYA SATU BLOK LOGIKA UNTUK MENAMPILKAN JUMLAH MATCHES ---
        total_occurrences = result.get("total_occurrences", 0) 
        
        matches_text = f"{total_occurrences} exact matches"
        if total_occurrences == 0 and result.get('fuzzy_keywords'): # Jika tidak ada exact match, tapi ada fuzzy
            highest_similarity = result.get('highest_fuzzy_similarity', 0.0)
            matches_text = f"~{highest_similarity:.0f}% fuzzy match"
        # Perbaiki typo: result_item -> result
        elif total_occurrences == 0 and not result.get('fuzzy_keywords') and not result.get('matched_keywords'): 
            matches_text = "No keywords matched"

        matches_label = ctk.CTkLabel(
            header_frame,
            text=matches_text,  # Menggunakan variabel matches_text yang sudah diproses dengan benar
            font=ctk.CTkFont(size=14), 
            text_color="#1B2B4C"
        )
        matches_label.pack(side="right")
        # --- AKHIR BLOK LOGIKA JUMLAH MATCHES ---
        
        # keywords_frame = ctk.CTkFrame(content_frame, fg_color="transparent") # Ini sepertinya tidak terpakai
        # keywords_frame.pack(fill="both", expand=True, pady=(0, 20)) # Anda menggunakan keywords_outer_frame

        keywords_outer_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        keywords_outer_frame.pack(fill="both", expand=True, pady=(0,10))
        
        keywords_scroll_frame = ctk.CTkScrollableFrame(keywords_outer_frame, fg_color="transparent", height=100)
        keywords_scroll_frame.pack(fill="both", expand=True)
        
        exact_keywords = result.get("matched_keywords", {})
        if exact_keywords:
            exact_title = ctk.CTkLabel(keywords_scroll_frame, text="Exact Keywords:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#1B2B4C")
            exact_title.pack(anchor="w")
            for keyword, count in exact_keywords.items():
                keyword_text = f"- {keyword}: {count} occurrence{'s' if count > 1 else ''}"
                keyword_label = ctk.CTkLabel(keywords_scroll_frame, text=keyword_text, font=ctk.CTkFont(size=11), text_color="#1B2B4C")
                keyword_label.pack(anchor="w", padx=5)

        fuzzy_keywords_info = result.get("fuzzy_keywords", {})
        if fuzzy_keywords_info:
            # Pastikan Settings bisa diimpor jika belum di file ini
            # from backend import Settings # Tambahkan jika perlu, atau teruskan dari __init__
            # Untuk sementara, kita hardcode threshold jika Settings tidak tersedia di scope ini
            fuzzy_threshold_display = "N/A" 
            try:
                from backend import Settings # Coba impor Settings
                fuzzy_threshold_display = Settings.FUZZY_THRESHOLD
            except ImportError:
                print("Warning: Could not import Settings in result.py to display FUZZY_THRESHOLD.")
                # Anda bisa set default atau melewatkannya dari backend_manager jika perlu
                # atau meneruskannya sebagai parameter ke ResultPage jika logic ini tetap di sini

            fuzzy_title = ctk.CTkLabel(keywords_scroll_frame, text=f"Fuzzy (Threshold > {fuzzy_threshold_display}%):", font=ctk.CTkFont(size=12, weight="bold"), text_color="#1B2B4C")
            fuzzy_title.pack(anchor="w", pady=(5,0))
            for keyword, similarity in fuzzy_keywords_info.items():
                keyword_text = f"- {keyword} (~{similarity:.0f}%)"
                keyword_label = ctk.CTkLabel(keywords_scroll_frame, text=keyword_text, font=ctk.CTkFont(size=11), text_color="#1B2B4C")
                keyword_label.pack(anchor="w", padx=5)

        if not exact_keywords and not fuzzy_keywords_info:
            no_keywords_label = ctk.CTkLabel(keywords_scroll_frame, text="No specific keywords matched.", font=ctk.CTkFont(size=11), text_color="#1B2B4C")
            no_keywords_label.pack(anchor="w")

        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(5, 0), side="bottom")
                
        summary_button = ctk.CTkButton(
            buttons_frame, text="Summary", font=ctk.CTkFont(size=13, weight="normal"),
            width=100, height=30, corner_radius=6, border_width=1, border_color="#F9DFDC", 
            fg_color="#334D7A", hover_color="#1B2B4C", text_color="#DFCFC2",
            command=lambda app_id=result.get("applicant_id"): self.show_summary(app_id)
            )
        summary_button.pack(side="left", expand=True, padx=(0,5))
                
        view_cv_button = ctk.CTkButton(
            buttons_frame, text="View CV", font=ctk.CTkFont(size=13, weight="normal"),
            width=100, height=30, corner_radius=6, border_width=1, border_color="#F9DFDC", 
            fg_color="#334D7A", hover_color="#1B2B4C", text_color="#DFCFC2",
            command=lambda app_id=result.get("applicant_id"): self.view_cv(app_id)
            )
        view_cv_button.pack(side="right", expand=True, padx=(5,0))


        # keywords_title = ctk.CTkLabel(
        #     keywords_frame,
        #     text="Matched keywords:",
        #     font=ctk.CTkFont(size=14, weight="bold"),
        #     text_color="#1B2B4C"
        # )
        # keywords_title.pack(anchor="w", pady=(0, 8))
        
        # for i, (keyword, count) in enumerate(result["keywords"].items(), 1):
        #     keyword_text = f"{i}. {keyword}: {count} occurrence"
        #     if count > 1:
        #         keyword_text += "s"
                
        #     keyword_label = ctk.CTkLabel(
        #         keywords_frame,
        #         text=keyword_text,
        #         font=ctk.CTkFont(size=13),
        #         text_color="#1B2B4C"
        #     )
        #     keyword_label.pack(anchor="w", pady=2)
        
        # buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        # buttons_frame.pack(fill="x", pady=(5, 0))  
        
        # summary_button = ctk.CTkButton(
        #     buttons_frame,
        #     text="Summary",
        #     font=ctk.CTkFont(size=14, weight="normal"),
        #     width=100,
        #     height=32, 
        #     corner_radius=6,
        #     border_width=2,
        #     border_color="#F9DFDC", 
        #     fg_color="#334D7A",
        #     hover_color="#1B2B4C", 
        #     text_color="#DFCFC2",
        #     command=lambda: self.show_summary(result["name"])
        # )
        # summary_button.pack(side="left", padx=(0, 10))
        
        # view_cv_button = ctk.CTkButton(
        #     buttons_frame,
        #     text="View CV",
        #     font=ctk.CTkFont(size=14, weight="normal"),
        #     width=100,
        #     height=32, 
        #     corner_radius=6,
        #     border_width=2,
        #     border_color="#F9DFDC", 
        #     fg_color="#334D7A",
        #     hover_color="#1B2B4C", 
        #     text_color="#DFCFC2",
        #     command=lambda: self.view_cv(result["name"])
        # )
        # view_cv_button.pack(side="right")
    
    def create_hat_image(self, parent):
        try:
            image_path = "./assets/asset2.png"
            if os.path.exists(image_path):
                hat_image = Image.open(image_path)
                hat_ctk_image = ctk.CTkImage(
                    light_image=hat_image,
                    dark_image=hat_image,
                    size=(100, 95)
                )
                image_label = ctk.CTkLabel(
                    parent,
                    image=hat_ctk_image,
                    text=""
                )
                image_label.pack()
        except Exception as e:
            placeholder = ctk.CTkLabel(
                parent,
                text="Hat",
                font=ctk.CTkFont(size=40),
                text_color="#DFCFC2"
            )
            placeholder.pack()
    
    def create_book_image(self, parent):
        try:
            image_path = "./assets/asset4.png"
            if os.path.exists(image_path):
                book_image = Image.open(image_path)
                book_ctk_image = ctk.CTkImage(
                    light_image=book_image,
                    dark_image=book_image,
                    size=(90, 100)
                )
                image_label = ctk.CTkLabel(
                    parent,
                    image=book_ctk_image,
                    text=""
                )
                image_label.pack()
        except Exception as e:
            placeholder = ctk.CTkLabel(
                parent,
                text="Book",
                font=ctk.CTkFont(size=50),
                text_color="#DFCFC2"
            )
            placeholder.pack()
    



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