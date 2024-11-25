# TikTok Video Automation Project

This project automates the process of downloading a video from YouTube, adding subtitles, splitting the video into parts, and uploading it to TikTok. The scripts handle all these tasks in sequence, making it easier to publish content on TikTok.

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Project Workflow](#project-workflow)
4. [Running the Project](#running-the-project)
5. [File Descriptions](#file-descriptions)
6. [Important Notes](#important-notes)

## Requirements
- Python 3.10
- Selenium
- yt-dlp
- ffmpeg
- EdgeDriver

## Installation
1. Install the required Python packages:
   ```bash
   pip install selenium yt-dlp ffmpeg-python
   ```
2. Install [EdgeDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and ensure it is placed in the specified path (`C:\EdgeDriver`). Make sure the version matches your installed Microsoft Edge browser.

## Project Workflow
The automation process is divided into several key steps:
1. **Download Video from YouTube**: Use `yt-dlp` to download a video in the best available quality.
2. **Add Subtitles**: Add subtitles to the downloaded video using `ffmpeg`.
3. **Split the Video into Parts**: Split the video into smaller parts, suitable for uploading to TikTok.
4. **Upload Video to TikTok**: Automate the process of uploading the video using Selenium with saved cookies for login.

## Running the Project
### Step 1: Save TikTok Cookies
Before running the automation script, you need to manually log in to TikTok and save the cookies to ensure the script can upload videos automatically.

1. Run the `save_manual_cookies.py` script:
   ```bash
   python save_manual_cookies.py
   ```
2. This will open a browser window. Log in to TikTok manually.
3. After logging in, press Enter in the terminal to save the cookies. This will create a file called `tiktok_cookies.pkl` which will be used later for authentication.

### Step 2: Run the Main Script
After saving the cookies, run the `main.py` script to automate the entire workflow.

```bash
python main.py
```
This script will:
- Download the video from YouTube.
- Add subtitles to the video.
- Split the video into smaller parts.
- Upload the video parts to TikTok.

## File Descriptions
- **main.py**: The main automation script that orchestrates downloading, processing, and uploading the video.
- **save_manual_cookies.py**: Script used to save TikTok cookies after a manual login.
- **upload_tiktok.py**: Script that handles the video upload process to TikTok using Selenium.
- **delete_all_cookies.py**: Optional script to delete all cookies from the Edge browser if needed.

## Important Notes
- **Cookies**: You only need to save cookies (`save_manual_cookies.py`) once, unless they expire or you need to log in again.
- **Browser Compatibility**: This project uses EdgeDriver. Ensure that the EdgeDriver version matches your Edge browser version.
- **Login Issues**: If you encounter login issues, such as "too many attempts", try clearing the cookies using `delete_all_cookies.py` and save new cookies.
- **Sequential Execution**: Make sure each step (downloading, subtitle addition, splitting) is completed before uploading. The `main.py` script handles this automatically, but if you modify it, ensure the order is preserved.

## Troubleshooting
- **Browser Closes Immediately**: This might happen if the script finishes before the upload completes. Make sure you have sufficient `time.sleep()` intervals or use `WebDriverWait` to wait for specific elements.
- **Upload Failures**: If the upload fails, verify the TikTok webpage layout hasn't changed, and that the XPath selectors in `upload_tiktok.py` are correct.
- **Failed to Resolve Address**: Errors like `Failed to resolve address for stun.l.google.com` are generally network-related and can often be ignored.

