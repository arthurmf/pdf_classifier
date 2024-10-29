# **PDF Quality Classifier**

This is a Python-based GUI application for classifying PDFs as "Good" or "Bad." The application allows users to browse through a collection of PDFs, classify them, and store the results efficiently. The app is packaged into a standalone Windows executable, making it easy for non-technical users to use without needing Python installed.

---

## **Features**

- **Dynamic PDF Folder Selection**: Users can select any folder containing PDFs to classify.
- **User-Friendly Interface**: Simple GUI with "Good," "Bad," "Back," and "Next" buttons for easy navigation and classification.
- **Colored Status Indicators**: The current status of each PDF (Good/Bad) is shown with color-coded labels.
- **SQLite Database for Persistent Storage**: All classification results are saved in a SQLite database to ensure data consistency and easy retrieval.
- **CSV Export**: Option to export classification results to a CSV file.

---

## **Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Packaging as an EXE](#packaging-as-an-exe)
- [Dependencies](#dependencies)
- [How to Retrieve Results](#how-to-retrieve-results)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## **Installation**

### Prerequisites:

- **Python 3.x** (if running from source)
- **Required libraries**: See [Dependencies](#dependencies).
- For **Windows executable users**: No installation is required—just run the provided `.exe` file.

### Clone the Repository:

```bash
git clone https://github.com/your-repo/pdf-quality-classifier.git
cd pdf-quality-classifier
```

### Install Dependencies:

```bash
pip install -r requirements.txt
```

---

## **Usage**

### 1. Run the Application

If using Python:

```bash
python pdf_classifier.py
```

If using the **Windows executable**:
- Double-click the `pdf_classifier.exe` file.

### 2. Select a PDF Folder

- When the app starts, you’ll be prompted to **select a folder containing PDFs**.

### 3. Classify PDFs

- Use the **Good** (Green) or **Bad** (Red) buttons to classify PDFs.
- Use the **Back** and **Next** buttons to navigate between PDFs.
- The **current status** of each PDF is displayed with colored labels:
  - **Green**: Good
  - **Red**: Bad
  - **Black**: Not Classified

### 4. Export Results

- Click the **Export to CSV** button to save the results as a `classification_results.csv` file.

---

## **Packaging as an EXE**

To create a standalone Windows executable:

1. Install **PyInstaller**:

   ```bash
   pip install pyinstaller
   ```

2. Build the executable:

   ```bash
   pyinstaller --onefile --windowed pdf_classifier.py
   ```

3. The executable will be available in the `dist/` folder as `pdf_classifier.exe`.

---

## **Dependencies**

The following dependencies are required:

- **tkinter**: For the GUI  
- **PyMuPDF (fitz)**: For PDF rendering  
- **sqlite3**: For classification storage  

Install them using:

```bash
pip install PyMuPDF
```

---

## **How to Retrieve Results**

1. **SQLite Database**:  
   - The results are saved in `classification_results.db`.  
   - The user can **send you this file** after classification.

2. **CSV Export**:  
   - Users can export results to `classification_results.csv` using the **Export to CSV** button.

---

## **Troubleshooting**

1. **PDFs not loading properly**:
   - Ensure the PDFs are valid and not corrupted.

2. **Missing dependencies**:
   - Run `pip install -r requirements.txt` to ensure all dependencies are installed.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contributing**

Contributions are welcome! Please create a pull request or submit issues if you encounter any bugs or have feature requests.

---

## **Acknowledgments**

- **PyMuPDF** for PDF rendering.  
- **SQLite** for lightweight database management.  
- **tkinter** for the simple GUI interface.