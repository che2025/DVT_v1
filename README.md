# DVT Test Report Generator

AI-powered system that automates DVT test report generation from protocol documents and test data.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Features

- **Single-file application** - All functionality in `app.py`
- **AI-powered analysis** - Uses Google Gemini for document processing
- **All 13 AI tasks implemented** (Sections 4.1-4.13 from requirements)
- **Web-based interface** - Easy file upload and report generation
- **Word document output** - Professional formatted reports

## AI Tasks Implemented

1. ✅ **Create Scope and Purpose** (4.1)
2. ✅ **Create Reference Section** (4.2) 
3. ✅ **Create Acronyms & Definitions** (4.3)
4. ✅ **Create Test Procedure Summary** (4.4)
5. ✅ **Create Device Under Test Configuration** (4.5)
6. ✅ **Create Equipment Used Section** (4.6)
7. ✅ **Create Test Result Summary** (4.7)
8. ✅ **Create Test Results Details** (4.8)
9. ✅ **Create Protocol Deviations** (4.9)
10. ✅ **Create Defective Unit Investigations** (4.10)
11. ✅ **Create Test Method Loss Investigations** (4.11)
12. ✅ **Create Conclusion** (4.12)
13. ✅ **Create Report Document with Formatting** (4.13)

## File Types Supported

- **Protocol Documents**: .docx files
- **Test Data**: .xlsx/.xls files
- **Output**: .docx Word documents

## Optional: AI Configuration

For full AI features, set your Google Gemini API key:

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Edit `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

The application works without AI configuration but uses fallback templates.

## Usage

1. Open http://localhost:8000
2. Fill in report details (title, number, revision, project name)
3. Upload protocol document (.docx)
4. Upload test data files (.xlsx)
5. Optionally add JIRA ticket numbers
6. Click "Generate DVT Report"
7. Download the generated Word document

## Output

Reports are saved to the `Output/` folder and automatically downloaded.

## Architecture

- **Backend**: FastAPI with embedded HTML
- **Document Processing**: python-docx, openpyxl
- **AI**: Google Gemini API
- **Frontend**: Bootstrap 5 + vanilla JavaScript
- **Deployment**: Single Python process with Uvicorn

## Troubleshooting

- **Import errors**: Run `pip install -r requirements.txt`
- **Port conflicts**: Change port in `app.py` (line with `uvicorn.run`)
- **AI not working**: Configure GEMINI_API_KEY in `.env`
