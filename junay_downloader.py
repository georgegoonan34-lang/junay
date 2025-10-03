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
ctk.set_appearance_mode("System")  # Use system appearance for better macOS compatibility
ctk.set_default_color_theme("blue")  # Blue theme (can be changed to "green" or "dark-blue")


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
        """Create and arrange all UI elements"""

        # Main container with padding
        # Explicit colors for macOS compatibility
        main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray95", "gray10"))
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header/Title Section
        title_label = ctk.CTkLabel(
            main_frame,
            text="⚡ JUNAY 4K DOWNLOADER ⚡",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("#1f6aa5", "#4a9eff")  # Gradient-like blue
        )
        title_label.pack(pady=(0, 10))

        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Download YouTube videos in stunning 4K quality",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        subtitle_label.pack(pady=(0, 30))

        # URL Input Section
        url_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        url_frame.pack(fill="x", pady=(0, 20))

        url_label = ctk.CTkLabel(
            url_frame,
            text="📺 YouTube URL:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        url_label.pack(anchor="w", padx=20, pady=(15, 5))

        # URL entry with placeholder
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="Paste YouTube video URL here...",
            height=45,
            font=ctk.CTkFont(size=14),
            border_width=2
        )
        self.url_entry.pack(fill="x", padx=20, pady=(0, 15))

        # Quality Selection Section
        quality_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        quality_frame.pack(fill="x", pady=(0, 20))

        quality_label = ctk.CTkLabel(
            quality_frame,
            text="🎬 Video Quality:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        quality_label.pack(anchor="w", padx=20, pady=(15, 5))

        # Quality dropdown
        self.quality_var = ctk.StringVar(value="2160p (4K)")  # Default to 4K
        self.quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            values=["2160p (4K)", "1440p (2K)", "1080p (Full HD)", "720p (HD)", "Best Available"],
            variable=self.quality_var,
            height=40,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=12)
        )
        self.quality_menu.pack(fill="x", padx=20, pady=(0, 15))

        # Download Location Section
        location_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        location_frame.pack(fill="x", pady=(0, 20))

        location_label = ctk.CTkLabel(
            location_frame,
            text="📁 Save Location:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        location_label.pack(anchor="w", padx=20, pady=(15, 5))

        # Location display and browse button container
        # Removed fg_color="transparent" for macOS compatibility
        location_container = ctk.CTkFrame(location_frame, fg_color=location_frame.cget("fg_color"))
        location_container.pack(fill="x", padx=20, pady=(0, 15))

        self.location_display = ctk.CTkEntry(
            location_container,
            height=40,
            font=ctk.CTkFont(size=12),
            state="readonly"
        )
        self.location_display.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.location_display.configure(state="normal")
        self.location_display.insert(0, self.download_path)
        self.location_display.configure(state="readonly")

        browse_btn = ctk.CTkButton(
            location_container,
            text="Browse",
            width=100,
            height=40,
            font=ctk.CTkFont(size=14),
            command=self.browse_location
        )
        browse_btn.pack(side="right")

        # Progress Section
        self.progress_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        self.progress_frame.pack(fill="x", pady=(0, 20))

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to download",
            font=ctk.CTkFont(size=14),
            text_color="gray70"
        )
        self.progress_label.pack(pady=(15, 5))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 15))
        self.progress_bar.set(0)  # Start at 0%

        # Download Button
        self.download_btn = ctk.CTkButton(
            main_frame,
            text="⬇️  DOWNLOAD VIDEO",
            height=60,
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=("#1f6aa5", "#4a9eff"),
            hover_color=("#16537e", "#357abd"),
            command=self.start_download
        )
        self.download_btn.pack(fill="x", pady=(0, 15))

        # Footer/Credits
        credits_label = ctk.CTkLabel(
            main_frame,
            text="Built by George for Junay 💙 | Powered by yt-dlp",
            font=ctk.CTkFont(size=11),
            text_color="gray50"
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
