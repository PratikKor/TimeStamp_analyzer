Timestamp Analyzer for File Systems
|--------------------------------------------------------------------------------------------------------------------------|
A powerful, multi-threaded, command-line Timestamp Analyzer built with Python. This tool scans files in specified 
directories, retrieves timestamp metadata (creation, modification, and access times), and provides extensive filtering, 
sorting, and exporting options. With a text-based user interface, it allows easy navigation and supports absolute or 
relative paths to any directory on the system.

Features
Multi-threaded: Utilizes threading for faster processing, especially with large datasets.
Recursive Scanning: Option to scan directories recursively.
Symbolic Link Traversal: Allows users to include symlinked files if desired.

Comprehensive Filtering:
Filter by file size, date range, and extension.
Sort results by creation, modification, or access time.
Advanced Date and Time Display: Converts timestamps into a human-readable format.

Error Handling: Gracefully skips restricted files and logs errors.

Export Options:
Supports CSV, JSON, and Excel (XLSX) formats for easy data sharing.
Beautiful Output: Uses Rich library for a user-friendly text-based interface with tables and progress indicators.

Requirements
|--------------------------------------------------------------------------------------------------------------------------|
Python 3.6+
Additional Python libraries:
rich: For a visually appealing CLI experience
pandas: For exporting to Excel (optional if you don't need Excel output)

Install dependencies with:
|--------------------------------------------------------------------------------------------------------------------------|
pip install rich pandas

Installation
Clone the repository and navigate to the project directory:
|--------------------------------------------------------------------------------------------------------------------------|
git clone https://github.com/yourusername/timestamp-analyzer.git
cd timestamp-analyzer

Run the program:
|--------------------------------------------------------------------------------------------------------------------------|
python advanced_timestamp_analyzer.py

Usage
Upon running the program, you will be prompted to configure various settings.
|--------------------------------------------------------------------------------------------------------------------------|

Main Options
Directory Path: Specify the directory to analyze. Both relative and absolute paths are supported.
Number of Threads: Choose the number of threads for parallel processing.
Recursive Scanning: Choose whether to include subdirectories.
Follow Symbolic Links: Decide whether to follow symlinks.
Filter by Extension: Filter files by a specific extension (e.g., .txt, .jpg).
Minimum/Maximum File Size: Set size limits (in bytes) for files to include in the scan.
Sort Order: Choose sorting by created, modified, or accessed timestamp.
Export Format: Export results in CSV, JSON, or Excel.

|--------------------------------------------------------------------------------------------------------------------------|
Enter the absolute or relative path to the directory to scan for timestamps: /home/user/documents
Enter the number of threads to use: 4
Scan recursively? (y/n): y
Follow symbolic links? (y/n): n
Filter by file extension (e.g., .txt, .jpg): .txt
Minimum file size in bytes: 100
Maximum file size in bytes: 1000000
Sort files by (created, modified, accessed): created
Export format (csv, json, excel): csv
|--------------------------------------------------------------------------------------------------------------------------|

Output
The tool outputs a formatted table of results, displaying:
|--------------------------------------------------------------------------------------------------------------------------|
File Path
Size (in bytes)
Creation Date
Modification Date
Access Date
Results are also exported to a file in the specified format (csv, json, or excel).
|--------------------------------------------------------------------------------------------------------------------------|
