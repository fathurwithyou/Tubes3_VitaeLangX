from pdfminer.high_level import extract_text
import os
import concurrent.futures
import time
from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict, Tuple, Optional


def extract_text_from_pdf_worker(
    pdf_path: str,
) -> Tuple[str, str, float, Optional[str]]:
    """
    Standalone worker function for process pool execution.
    Returns (pdf_path, extracted_text, processing_time, error_message).
    """
    start_time = time.time()

    if not os.path.exists(pdf_path):
        processing_time = time.time() - start_time
        return pdf_path, "", processing_time, f"File not found: {pdf_path}"

    try:
        text = extract_text(pdf_path)
        processing_time = time.time() - start_time
        return pdf_path, text.strip(), processing_time, None
    except Exception as e:
        processing_time = time.time() - start_time
        return pdf_path, "", processing_time, f"PDF extraction error: {str(e)}"


class CVProcessor:
    """
    Optimized CV processor using process-based parallelism for maximum performance.
    """

    def __init__(self):
        self.stats = {
            "total_processing_time": 0,
            "total_files_processed": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
        }
        self.error_details = []

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extracts all text from a given PDF file.
        Returns a single long string containing the entire text content.
        """
        if not os.path.exists(pdf_path):
            print(f"Error: PDF file not found at {pdf_path}")
            return ""
        try:
            print(f"Extracting text from {pdf_path}...")
            text = extract_text(pdf_path)
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
            return ""

    def get_optimal_process_count(self, num_files: int) -> int:
        """
        Calculate optimal number of processes based on benchmark results and system resources.
        Based on benchmark: 16 processes performed best with 10.27 CVs/second.
        """
        cpu_count = os.cpu_count() or 1

        if num_files < 4:
            return num_files
        elif num_files < 20:
            return min(cpu_count, num_files)
        else:
            return min(16, num_files)

    def process_cv_for_pattern_matching(
        self, cv_paths: List[str], max_workers: Optional[int] = None
    ) -> Dict[str, str]:
        """
        Optimized process-based CV processing for pattern matching.
        Based on benchmark results: Uses 16 processes for optimal performance.
        """
        if not cv_paths:
            return {}

        if max_workers is None:
            max_workers = min(16, len(cv_paths))

        start_time = time.time()
        in_memory_cv_texts = {}
        processed_count = 0

        self.error_details = []

        print(
            f"Processing {len(cv_paths)} CVs using {max_workers} Processes"
        )

        try:
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                future_to_path = {
                    executor.submit(extract_text_from_pdf_worker, cv_path): cv_path
                    for cv_path in cv_paths
                }

                for future in concurrent.futures.as_completed(future_to_path):
                    try:
                        path, text, proc_time, error = future.result()
                        processed_count += 1
                        self.stats["total_processing_time"] += proc_time

                        if error:
                            print(
                                f"Error processing {os.path.basename(path)}: {error}")
                            self.error_details.append(
                                {
                                    "file": path,
                                    "error": error,
                                    "processing_time": proc_time,
                                }
                            )
                            self.stats["failed_extractions"] += 1
                        elif text and text.strip():
                            in_memory_cv_texts[path] = text
                            self.stats["successful_extractions"] += 1
                        else:
                            error_msg = "No text extracted (empty result)"
                            print(
                                f"Warning for {os.path.basename(path)}: {error_msg}")
                            self.error_details.append(
                                {
                                    "file": path,
                                    "error": error_msg,
                                    "processing_time": proc_time,
                                }
                            )
                            self.stats["failed_extractions"] += 1

                        progress_interval = max(
                            1, min(20, len(cv_paths) // 10))
                        if (
                            processed_count % progress_interval == 0
                            or processed_count == len(cv_paths)
                        ):
                            progress_percent = (
                                processed_count / len(cv_paths)) * 100
                            elapsed = time.time() - start_time
                            rate = processed_count / elapsed if elapsed > 0 else 0
                            cpu_efficiency = (
                                (self.stats["total_processing_time"] / elapsed)
                                if elapsed > 0
                                else 0
                            )
                            print(
                                f"Progress: {processed_count}/{len(cv_paths)} ({progress_percent:.1f}%) | "
                                f"Rate: {rate:.2f} CVs/sec | CPU Efficiency: {cpu_efficiency:.1f}x"
                            )

                    except Exception as e:
                        processed_count += 1
                        error_msg = f"Process execution error: {str(e)}"
                        print(f"Error: {error_msg}")
                        self.error_details.append(
                            {
                                "file": "Unknown (process error)",
                                "error": error_msg,
                                "processing_time": 0,
                            }
                        )
                        self.stats["failed_extractions"] += 1

        except Exception as e:
            error_msg = f"ProcessPoolExecutor error: {str(e)}"
            print(error_msg)
            self.error_details.append(
                {
                    "file": "ProcessPoolExecutor",
                    "error": error_msg,
                    "processing_time": 0,
                }
            )

        total_time = time.time() - start_time
        self.stats["total_files_processed"] = len(cv_paths)

        cpu_efficiency = (
            (self.stats["total_processing_time"] /
             total_time) if total_time > 0 else 0
        )

        print(
            f"CV text extraction for pattern matching complete. "
            f"Successfully processed {len(in_memory_cv_texts)} out of {len(cv_paths)} CVs."
        )
        print(f"Total processing time: {total_time:.2f} seconds")

        if self.error_details:
            print(f"\nError Summary ({len(self.error_details)} failed):")

            display_errors = self.error_details[:10]
            for i, error_info in enumerate(display_errors, 1):
                filename = os.path.basename(error_info["file"])
                print(f"  {i}. {filename}: {error_info['error']}")

            if len(self.error_details) > 10:
                print(f"  ... and {len(self.error_details) - 10} more errors")

            error_types = {}
            for error_info in self.error_details:
                error_type = error_info["error"].split(":")[0]
                error_types[error_type] = error_types.get(error_type, 0) + 1

            print("\nError breakdown:")
            for error_type, count in sorted(
                error_types.items(), key=lambda x: x[1], reverse=True
            ):
                print(
                    f"  • {error_type}: {count} files ({count / len(self.error_details) * 100:.1f}%)"
                )

        return in_memory_cv_texts
