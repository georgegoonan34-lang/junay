"""
Junay 4K YouTube Downloader - macOS Test Version
Uses standard tkinter for Mac compatibility
Same functionality as the Windows version
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import yt_dlp


class JunayDownloaderMac:
    """macOS-compatible version for testing"""

    def __init__(self, root):
        self.root = root
        self.root.title("Junay 4K Downloader (Mac Test)")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        # Configure dark-ish theme colors
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.accent_color = "#4a9eff"
        self.root.configure(bg=self.bg_color)

        # State variables
        self.download_path = str(Path.home() / "Downloads")
        self.is_downloading = False

        # Build UI
        self.setup_ui()

    def setup_ui(self):
        """Create all UI elements"""

        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = tk.Label(
            main_frame,
            text="⚡ JUNAY 4K DOWNLOADER ⚡",
            font=("Helvetica", 28, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title.pack(pady=(0, 5))

        subtitle = tk.Label(
            main_frame,
            text="Download YouTube videos in stunning 4K quality",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg="#cccccc"
        )
        subtitle.pack(pady=(0, 25))

        # URL Section
        url_frame = tk.LabelFrame(
            main_frame,
            text="📺 YouTube URL",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            padx=15,
            pady=15
        )
        url_frame.pack(fill="x", pady=(0, 15))

        self.url_entry = tk.Entry(
            url_frame,
            font=("Helvetica", 13),
            width=50
        )
        self.url_entry.pack(fill="x")
        self.url_entry.insert(0, "Paste YouTube video URL here...")
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)

        # Quality Section
        quality_frame = tk.LabelFrame(
            main_frame,
            text="🎬 Video Quality",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            padx=15,
            pady=15
        )
        quality_frame.pack(fill="x", pady=(0, 15))

        self.quality_var = tk.StringVar(value="2160p (4K)")
        quality_dropdown = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=["2160p (4K)", "1440p (2K)", "1080p (Full HD)", "720p (HD)", "Best Available"],
            state="readonly",
            font=("Helvetica", 12),
            width=30
        )
        quality_dropdown.pack(fill="x")

        # Location Section
        location_frame = tk.LabelFrame(
            main_frame,
            text="📁 Save Location",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            padx=15,
            pady=15
        )
        location_frame.pack(fill="x", pady=(0, 15))

        location_container = tk.Frame(location_frame, bg=self.bg_color)
        location_container.pack(fill="x")

        self.location_entry = tk.Entry(
            location_container,
            font=("Helvetica", 11),
            state="readonly"
        )
        self.location_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.location_entry.configure(state="normal")
        self.location_entry.insert(0, self.download_path)
        self.location_entry.configure(state="readonly")

        browse_btn = tk.Button(
            location_container,
            text="Browse",
            font=("Helvetica", 12),
            command=self.browse_location,
            bg=self.accent_color,
            fg="white",
            cursor="hand2"
        )
        browse_btn.pack(side="right")

        # Progress Section
        progress_frame = tk.LabelFrame(
            main_frame,
            text="Progress",
            font=("Helvetica", 14, "bold"),
            bg=self.bg_color,
            fg=self.fg_color,
            padx=15,
            pady=15
        )
        progress_frame.pack(fill="x", pady=(0, 15))

        self.progress_label = tk.Label(
            progress_frame,
            text="Ready to download",
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg="#cccccc"
        )
        self.progress_label.pack(pady=(0, 5))

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(fill="x")

        # Download Button
        self.download_btn = tk.Button(
            main_frame,
            text="⬇️  DOWNLOAD VIDEO",
            font=("Helvetica", 18, "bold"),
            bg=self.accent_color,
            fg="white",
            command=self.start_download,
            cursor="hand2",
            height=2
        )
        self.download_btn.pack(fill="x", pady=(0, 10))

        # Credits
        credits = tk.Label(
            main_frame,
            text="Built by George for Junay 💙 | Powered by yt-dlp",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        credits.pack()

    def clear_placeholder(self, event):
        """Clear placeholder text on focus"""
        if self.url_entry.get() == "Paste YouTube video URL here...":
            self.url_entry.delete(0, tk.END)

    def browse_location(self):
        """Browse for download location"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.location_entry.configure(state="normal")
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, folder)
            self.location_entry.configure(state="readonly")

    def get_format_selector(self):
        """Convert quality selection to yt-dlp format string"""
        quality = self.quality_var.get()

        # Map quality options to yt-dlp format selectors
        quality_map = {
            "2160p (4K)": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
            "1440p (2K)": "bestvideo[height<=1440]+bestaudio/best[height<=1440]",
            "1080p (Full HD)": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "720p (HD)": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "Best Available": "bestvideo+bestaudio/best"
        }

        return quality_map.get(quality, "bestvideo+bestaudio/best")

    def progress_hook(self, d):
        """Update progress bar during download"""
        if d['status'] == 'downloading':
            # Extract progress percentage
            if 'downloaded_bytes' in d and 'total_bytes' in d:
                percent = d['downloaded_bytes'] / d['total_bytes']
                self.progress_bar['value'] = percent * 100

                # Update status text
                speed = d.get('speed', 0)
                eta = d.get('eta', 0)
                if speed:
                    speed_mb = speed / 1_000_000
                    self.progress_label.configure(
                        text=f"Downloading... {percent*100:.1f}% | {speed_mb:.2f} MB/s | ETA: {eta}s"
                    )
                else:
                    self.progress_label.configure(text=f"Downloading... {percent*100:.1f}%")

                # Force UI update
                self.root.update_idletasks()

        elif d['status'] == 'finished':
            self.progress_bar['value'] = 100
            self.progress_label.configure(text="Processing... (merging video & audio)")
            self.root.update_idletasks()

    def download_video(self):
        """Main download function (runs in separate thread)"""
        url = self.url_entry.get().strip()

        # Validate URL
        if not url or url == "Paste YouTube video URL here...":
            messagebox.showerror("Error", "Please enter a YouTube URL")
            self.reset_ui()
            return

        # Configure yt-dlp options
        ydl_opts = {
            'format': self.get_format_selector(),
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'merge_output_format': 'mp4',
            'postprocessor_args': ['-c:v', 'copy', '-c:a', 'aac'],
        }

        try:
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = info.get('title', 'video')

            # Success notification
            self.progress_label.configure(text="✅ Download Complete!", fg="green")
            messagebox.showinfo(
                "Success",
                f"'{video_title}' downloaded successfully!\n\nSaved to: {self.download_path}"
            )

        except Exception as e:
            # Error handling
            self.progress_label.configure(text="❌ Download Failed", fg="red")
            messagebox.showerror("Download Error", f"Failed to download video:\n\n{str(e)}")

        finally:
            # Reset UI
            self.reset_ui()

    def start_download(self):
        """Initiate download in background thread"""
        if self.is_downloading:
            return

        # Update UI to downloading state
        self.is_downloading = True
        self.download_btn.configure(state="disabled", text="DOWNLOADING...")
        self.progress_bar['value'] = 0
        self.progress_label.configure(text="Starting download...", fg="#cccccc")

        # Run download in background thread
        download_thread = threading.Thread(target=self.download_video, daemon=True)
        download_thread.start()

    def reset_ui(self):
        """Reset UI after download"""
        self.is_downloading = False
        self.download_btn.configure(state="normal", text="⬇️  DOWNLOAD VIDEO")
        self.progress_bar['value'] = 0
        self.progress_label.configure(text="Ready to download", fg="#cccccc")


# Application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = JunayDownloaderMac(root)
    root.mainloop()
