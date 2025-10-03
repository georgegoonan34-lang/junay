"""
Junay 4K YouTube Downloader
A modern, professional YouTube video downloader with 4K support
Built with CustomTkinter for a flashy, modern UI
"""

import customtkinter as ctk
import threading
import os
from tkinter import filedialog, messagebox
from pathlib import Path
import yt_dlp
import sys

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")  # Force dark mode for beautiful iOS-like design
ctk.set_default_color_theme("blue")  # Will override with custom purple colors


class JunayDownloader(ctk.CTk):
    """Main application class for the YouTube downloader"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Junay 4K Downloader")
        self.geometry("800x600")
        self.resizable(False, False)

        # State variables
        self.download_path = str(Path.home() / "Downloads")  # Default to user's Downloads folder
        self.is_downloading = False

        # Build the UI
        self.setup_ui()

        # Force update for macOS compatibility
        self.update_idletasks()

    def setup_ui(self):
        """Create and arrange all UI elements with beautiful iOS-style dark mode design"""

        # iOS-style color palette - deep dark with purple accents
        BG_DARK = "#1a1a1a"  # Deep dark background
        CARD_BG = "#2a2a2a"  # Card/section background
        PURPLE_PRIMARY = "#8B5CF6"  # Beautiful purple accent
        PURPLE_HOVER = "#7C3AED"  # Darker purple for hover
        TEXT_PRIMARY = "#FFFFFF"  # White text
        TEXT_SECONDARY = "#A0A0A0"  # Gray text

        # Main container with deep dark background
        self.configure(fg_color=BG_DARK)
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_DARK)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Header Section - Clean and minimal
        title_label = ctk.CTkLabel(
            main_frame,
            text="JUNAY 4K",
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color=PURPLE_PRIMARY
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Download YouTube videos in stunning quality",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 35))

        # URL Input Section - Smooth rounded card
        url_frame = ctk.CTkFrame(main_frame, corner_radius=16, fg_color=CARD_BG)
        url_frame.pack(fill="x", pady=(0, 16))

        url_label = ctk.CTkLabel(
            url_frame,
            text="YouTube URL",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        url_label.pack(anchor="w", padx=24, pady=(20, 8))

        # URL entry with smooth edges
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="https://youtube.com/watch?v=...",
            height=50,
            font=ctk.CTkFont(size=13),
            border_width=0,
            corner_radius=12,
            fg_color="#333333",
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_SECONDARY
        )
        self.url_entry.pack(fill="x", padx=24, pady=(0, 20))

        # Quality Selection Section - iOS-style card
        quality_frame = ctk.CTkFrame(main_frame, corner_radius=16, fg_color=CARD_BG)
        quality_frame.pack(fill="x", pady=(0, 16))

        quality_label = ctk.CTkLabel(
            quality_frame,
            text="Video Quality",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        quality_label.pack(anchor="w", padx=24, pady=(20, 8))

        # Quality dropdown with purple accent
        self.quality_var = ctk.StringVar(value="2160p (4K)")
        self.quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            values=["2160p (4K)", "1440p (2K)", "1080p (Full HD)", "720p (HD)", "Best Available"],
            variable=self.quality_var,
            height=50,
            corner_radius=12,
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=12),
            fg_color="#333333",
            button_color=PURPLE_PRIMARY,
            button_hover_color=PURPLE_HOVER,
            text_color=TEXT_PRIMARY
        )
        self.quality_menu.pack(fill="x", padx=24, pady=(0, 20))

        # Download Location Section - Smooth card
        location_frame = ctk.CTkFrame(main_frame, corner_radius=16, fg_color=CARD_BG)
        location_frame.pack(fill="x", pady=(0, 16))

        location_label = ctk.CTkLabel(
            location_frame,
            text="Save Location",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_PRIMARY
        )
        location_label.pack(anchor="w", padx=24, pady=(20, 8))

        # Location display and browse button - iOS-style
        location_container = ctk.CTkFrame(location_frame, fg_color="transparent")
        location_container.pack(fill="x", padx=24, pady=(0, 20))

        self.location_display = ctk.CTkEntry(
            location_container,
            height=50,
            font=ctk.CTkFont(size=12),
            corner_radius=12,
            border_width=0,
            fg_color="#333333",
            text_color=TEXT_PRIMARY,
            state="readonly"
        )
        self.location_display.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.location_display.configure(state="normal")
        self.location_display.insert(0, self.download_path)
        self.location_display.configure(state="readonly")

        browse_btn = ctk.CTkButton(
            location_container,
            text="Browse",
            width=110,
            height=50,
            corner_radius=12,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=PURPLE_PRIMARY,
            hover_color=PURPLE_HOVER,
            text_color=TEXT_PRIMARY,
            command=self.browse_location
        )
        browse_btn.pack(side="right")

        # Progress Section - Minimal design
        self.progress_frame = ctk.CTkFrame(main_frame, corner_radius=16, fg_color=CARD_BG)
        self.progress_frame.pack(fill="x", pady=(0, 20))

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to download",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_SECONDARY
        )
        self.progress_label.pack(pady=(20, 10))

        # Progress bar with purple accent
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=8,
            corner_radius=4,
            fg_color="#333333",
            progress_color=PURPLE_PRIMARY
        )
        self.progress_bar.pack(fill="x", padx=24, pady=(0, 20))
        self.progress_bar.set(0)

        # Download Button - Bold and beautiful purple
        self.download_btn = ctk.CTkButton(
            main_frame,
            text="Download Video",
            height=56,
            corner_radius=14,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=PURPLE_PRIMARY,
            hover_color=PURPLE_HOVER,
            text_color=TEXT_PRIMARY,
            command=self.start_download
        )
        self.download_btn.pack(fill="x", pady=(0, 20))

        # Footer - Minimal credits
        credits_label = ctk.CTkLabel(
            main_frame,
            text="Built by George for Junay  •  Powered by yt-dlp",
            font=ctk.CTkFont(size=10),
            text_color="#505050"
        )
        credits_label.pack(pady=(0, 0))

    def browse_location(self):
        """Open folder browser to select download location"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:  # Only update if user selected a folder
            self.download_path = folder
            self.location_display.configure(state="normal")
            self.location_display.delete(0, "end")
            self.location_display.insert(0, folder)
            self.location_display.configure(state="readonly")

    def get_format_selector(self):
        """Convert quality selection to yt-dlp format string"""
        quality = self.quality_var.get()

        # Map quality options to yt-dlp format selectors
        # This ensures we get the best video+audio combination for selected quality
        quality_map = {
            "2160p (4K)": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
            "1440p (2K)": "bestvideo[height<=1440]+bestaudio/best[height<=1440]",
            "1080p (Full HD)": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "720p (HD)": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "Best Available": "bestvideo+bestaudio/best"
        }

        return quality_map.get(quality, "bestvideo+bestaudio/best")

    def progress_hook(self, d):
        """Callback function to update progress bar during download"""
        if d['status'] == 'downloading':
            # Extract progress percentage from yt-dlp
            if 'downloaded_bytes' in d and 'total_bytes' in d:
                percent = d['downloaded_bytes'] / d['total_bytes']
                self.progress_bar.set(percent)

                # Update status text with download info
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                if speed:
                    speed_mb = speed / 1_000_000  # Convert to MB/s
                    self.progress_label.configure(
                        text=f"Downloading... {percent*100:.1f}% | {speed_mb:.2f} MB/s | ETA: {eta}s"
                    )
                else:
                    self.progress_label.configure(text=f"Downloading... {percent*100:.1f}%")

        elif d['status'] == 'finished':
            self.progress_bar.set(1.0)
            self.progress_label.configure(text="Processing... (merging video & audio)")

    def download_video(self):
        """Main download function (runs in separate thread to avoid UI freezing)"""
        url = self.url_entry.get().strip()

        # Validate URL
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            self.reset_ui()
            return

        # Configure yt-dlp options
        ydl_opts = {
            'format': self.get_format_selector(),  # Quality selector
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),  # Output file naming
            'progress_hooks': [self.progress_hook],  # Progress callback
            'merge_output_format': 'mp4',  # Ensure output is mp4
            'postprocessor_args': ['-c:v', 'copy', '-c:a', 'aac'],  # Fast merge with AAC audio
        }

        try:
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = info.get('title', 'video')

            # Success notification
            self.progress_label.configure(text="✅ Download Complete!", text_color="green")
            messagebox.showinfo(
                "Success",
                f"'{video_title}' downloaded successfully!\n\nSaved to: {self.download_path}"
            )

        except Exception as e:
            # Error handling
            self.progress_label.configure(text="❌ Download Failed", text_color="red")
            messagebox.showerror("Download Error", f"Failed to download video:\n\n{str(e)}")

        finally:
            # Reset UI back to ready state
            self.reset_ui()

    def start_download(self):
        """Initiate download process in background thread"""
        if self.is_downloading:
            return  # Prevent multiple simultaneous downloads

        # Update UI to downloading state
        self.is_downloading = True
        self.download_btn.configure(state="disabled", text="DOWNLOADING...")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Starting download...", text_color="gray70")

        # Run download in background thread to keep UI responsive
        download_thread = threading.Thread(target=self.download_video, daemon=True)
        download_thread.start()

    def reset_ui(self):
        """Reset UI elements back to initial state after download"""
        self.is_downloading = False
        self.download_btn.configure(state="normal", text="⬇️  DOWNLOAD VIDEO")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Ready to download", text_color="gray70")


# Application entry point
if __name__ == "__main__":
    app = JunayDownloader()
    app.mainloop()
