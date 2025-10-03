"""
Build script to package Junay Downloader as a standalone Windows .exe
This script uses PyInstaller to create a single executable file
"""

import PyInstaller.__main__
import sys
import os

def build_exe():
    """Build the application as a Windows executable"""

    # PyInstaller arguments
    # --name: Name of the output executable
    # --onefile: Bundle everything into a single .exe file
    # --windowed: Don't show console window (GUI app only)
    # --icon: Application icon (optional, would need an .ico file)
    # --add-data: Include additional files if needed
    # --clean: Clean PyInstaller cache before building

    args = [
        'junay_downloader.py',           # Main script to build
        '--name=JunayDownloader',         # Output name
        '--onefile',                      # Single file executable
        '--windowed',                     # No console window
        '--clean',                        # Clean build
        '--noconfirm',                    # Overwrite output without asking
    ]

    print("🔨 Building Junay Downloader executable...")
    print("This may take a few minutes...\n")

    # Run PyInstaller
    PyInstaller.__main__.run(args)

    print("\n✅ Build complete!")
    print(f"📦 Executable location: {os.path.join('dist', 'JunayDownloader.exe')}")
    print("\nYou can now send the JunayDownloader.exe file to your friend!")

if __name__ == "__main__":
    build_exe()
