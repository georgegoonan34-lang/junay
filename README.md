# ⚡ Junay 4K Downloader

A modern, professional YouTube video downloader with 4K support. Built with Python and CustomTkinter for a sleek, dark-mode UI.

## 🌟 Features

- **4K Video Support** - Download videos in stunning 2160p quality
- **Multiple Quality Options** - Choose from 4K, 2K, 1080p, 720p, or Best Available
- **Modern UI** - Flashy dark-mode interface with smooth animations
- **Progress Tracking** - Real-time download progress with speed and ETA
- **Easy to Use** - Simple, intuitive interface anyone can use
- **Standalone Executable** - No installation required, just run the .exe

## 📸 UI Preview

The app features:
- Clean, modern dark-mode design
- Large, easy-to-read buttons and inputs
- Real-time progress tracking
- Custom location selection
- Quality presets for different needs

---

## 🚀 For Junay (End User)

### How to Use:

1. **Double-click** `JunayDownloader.exe` to launch the app
2. **Paste** a YouTube video URL into the text field
3. **Select** your desired video quality (default is 4K)
4. **Choose** where to save the video (or use default Downloads folder)
5. **Click** the big "DOWNLOAD VIDEO" button
6. **Wait** for the download to complete - you'll see progress in real-time!

### Tips:
- Make sure you have a stable internet connection for 4K downloads
- 4K files are large (can be several GB), ensure you have enough disk space
- The first download might take a moment to initialize
- Downloaded videos are saved as `.mp4` files

### Requirements:
- Windows 7 or later
- Internet connection
- No additional software needed!

---

## 🛠️ For George (Developer)

### Setup Development Environment:

1. **Clone/Navigate to project:**
   ```bash
   cd Junay
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements_build.txt
   ```

### Running the App (Development):

```bash
python junay_downloader.py
```

### Building the Executable:

**Option 1: Use the build script (easiest)**
```bash
python build_exe.py
```

**Option 2: Direct PyInstaller command**
```bash
pyinstaller --name=JunayDownloader --onefile --windowed --clean junay_downloader.py
```

The executable will be created in the `dist/` folder as `JunayDownloader.exe`

### Shipping to Junay:

1. Build the executable (see above)
2. Navigate to `dist/` folder
3. Send `JunayDownloader.exe` to Junay via:
   - Google Drive / Dropbox
   - Email (if file size allows)
   - USB drive
   - File transfer service (WeTransfer, etc.)

**That's it!** Junay just needs to run the .exe file. No Python installation required.

---

## 📁 Project Structure

```
Junay/
├── junay_downloader.py      # Main application code
├── build_exe.py              # Script to build .exe
├── requirements.txt          # Runtime dependencies
├── requirements_build.txt    # Build dependencies (includes PyInstaller)
├── .gitignore               # Git ignore file
└── README.md                # This file
```

---

## 🔧 Technical Details

**Built with:**
- **Python 3.8+**
- **CustomTkinter** - Modern UI framework
- **yt-dlp** - YouTube downloading engine
- **PyInstaller** - Packaging to .exe

**How it works:**
1. Uses yt-dlp to fetch video from YouTube
2. Downloads best video and audio streams separately
3. Merges them into a single MP4 file
4. All processing happens locally on the user's machine

---

## ⚖️ Legal & Ethical Use

**IMPORTANT:** This tool is intended for downloading videos you have the right to download:
- Your own uploaded content
- Public domain videos
- Videos with Creative Commons licenses
- Content where you have permission from the creator

Please respect copyright laws and YouTube's Terms of Service.

---

## 📝 Portfolio & LinkedIn

**For Portfolio/LinkedIn Description:**

> Built a professional desktop application for downloading YouTube videos in 4K quality.
>
> - Developed modern UI with Python and CustomTkinter
> - Integrated yt-dlp for reliable video downloading
> - Packaged as standalone Windows executable using PyInstaller
> - Features real-time progress tracking, quality selection, and custom save locations
> - Delivered as production-ready software for end users

**Skills demonstrated:**
- Python Development
- GUI Design (CustomTkinter)
- Threading & Async Operations
- Software Packaging & Distribution
- User Experience Design
- API Integration (yt-dlp)

---

## 🐛 Troubleshooting

**Issue:** App won't start
- Make sure you have Windows 7 or later
- Try running as administrator
- Check antivirus isn't blocking it

**Issue:** Downloads fail
- Verify the YouTube URL is valid and accessible
- Check your internet connection
- Some videos may be restricted by region or age

**Issue:** Slow downloads
- 4K files are large, this is normal
- Check your internet speed
- Try a lower quality option

**Issue:** "Not enough space" error
- 4K videos can be several GB
- Free up disk space or choose a different save location

---

## 💙 Credits

Built by **George** for **Junay**

Powered by:
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video downloading
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework

---

## 📬 Feedback & Support

Questions or issues? Reach out to George!

Made with 💙 and ☕
