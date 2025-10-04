"""
Junay Downloader Launcher
This script starts the Flask server and opens the browser automatically
Used for packaging into a Windows .exe
"""

import sys
import os
import threading
import time
import webbrowser
from waitress import serve
from app import app

def open_browser():
    """Wait for server to start, then open browser"""
    time.sleep(2)  # Wait for server to initialize
    webbrowser.open('http://127.0.0.1:5001')

def main():
    """Main entry point for the launcher"""
    print("=" * 60)
    print("  JUNAY 4K DOWNLOADER")
    print("  Starting server...")
    print("=" * 60)

    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    print("\n✓ Server started!")
    print("✓ Opening browser...")
    print("\nThe app is now running at: http://127.0.0.1:5001")
    print("\nPress CTRL+C to stop the server\n")

    # Start the production server (Waitress)
    # This is better than Flask's dev server for production use
    try:
        serve(app, host='127.0.0.1', port=5001, threads=4)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)

if __name__ == '__main__':
    main()
