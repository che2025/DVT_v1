#!/usr/bin/env python3
"""
DVT Test Report Generator - Refactored FastAPI Application
Main application with separated front-end and back-end logic
"""

import os
import sys
from datetime import datetime
from typing import List, Dict
from pathlib import Path

# FastAPI imports
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

# Core modules
from report_generator_agent.ai_config import configure_ai
from report_generator_agent.report_generator import DVTReportGenerator

# Initialize FastAPI app
app = FastAPI(title="DVT Test Report Generator", version="1.0.0")

# Configure static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="frontend")

# Configure AI and initialize report generator
ai_client = configure_ai()
report_generator = DVTReportGenerator(client=ai_client)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page with upload form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_report(
    request: Request,
    title: str = Form(...),
    report_number: str = Form(...),
    revision: str = Form(...),
    project_name: str = Form(...),
    document_owner: str = Form(...),
    protocol_number: str = Form(""),
    jira_tickets: str = Form(""),
    test_data_type: str = Form(...),
    units_sterilized: str = Form(...),
    units_modified: str = Form(...),
    modification_description: str = Form(""),
    calibration_verified: str = Form(...),
    test_execution_chronology: str = Form("[]"),  # JSON string of chronology data
    protocol_file: UploadFile = File(...),
    data_files: List[UploadFile] = File(default=[]),
    analysis_images: List[UploadFile] = File(default=[])  # Analysis images for test result analysis
):
    """Generate DVT report from uploaded files"""
    try:
        # Ensure report number has RPT- prefix
        if not report_number.startswith('RPT-'):
            report_number = 'RPT-' + report_number
        
        # Prepare report configuration
        report_config = {
            "title": title,
            "report_number": report_number,
            "revision": revision,
            "project_name": project_name,
            "document_owner": document_owner,
            "protocol_number": protocol_number,
            "jira_tickets": [ticket.strip() for ticket in jira_tickets.split(",") if ticket.strip()],
            "test_data_type": test_data_type
        }
        
        # Prepare device configuration
        import json
        try:
            chronology_data = json.loads(test_execution_chronology) if test_execution_chronology else []
            print(f"🔍 [DEBUG] Received test_execution_chronology: {test_execution_chronology}")
            print(f"🔍 [DEBUG] Parsed chronology_data: {chronology_data}")
        except json.JSONDecodeError as e:
            print(f"❌ [ERROR] Failed to parse chronology JSON: {e}")
            chronology_data = []
            
        device_config = {
            "units_sterilized": units_sterilized.lower() == "true",
            "units_modified": units_modified.lower() == "true",
            "modification_description": modification_description.strip() if modification_description else "",
            "calibration_verified": calibration_verified.lower() == "true",
            "test_execution_chronology": chronology_data
        }
        
        # Process analysis images
        analysis_image_paths = []
        if analysis_images:
            print(f"🖼️ [DEBUG] Processing {len(analysis_images)} analysis images")
            for i, image_file in enumerate(analysis_images):
                if image_file.filename and image_file.size > 0:
                    # Save image temporarily
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.filename)[1]) as tmp_file:
                        content = await image_file.read()
                        tmp_file.write(content)
                        analysis_image_paths.append(tmp_file.name)
                        print(f"🖼️ [DEBUG] Saved image {i+1}: {image_file.filename} ({len(content)} bytes)")
        
        print(f"🖼️ [DEBUG] Total analysis images processed: {len(analysis_image_paths)}")
        
        # Process uploaded files
        processed_data = await report_generator.process_files(protocol_file, data_files)
        
        # Generate all report sections using AI tasks
        sections = await report_generator.generate_report_sections(report_config, processed_data, device_config, analysis_image_paths)
        
        # Create Word document
        report_path = await report_generator.create_word_document(report_config, sections)
        
        # Store report info for success page
        report_info = {
            "filename": os.path.basename(report_path),
            "title": title,
            "report_number": report_number,
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "file_path": report_path
        }
        
        # Return success page with download link
        return templates.TemplateResponse("success.html", {
            "request": request, 
            "report_info": report_info
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@app.get("/download/{filename}")
async def download_report(filename: str):
    """Download generated report"""
    file_path = os.path.join('Output', filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    else:
        raise HTTPException(status_code=404, detail="Report file not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ai_configured": ai_client is not None,
        "frontend_configured": os.path.exists("frontend"),
        "static_configured": os.path.exists("static")
    }

if __name__ == "__main__":
    # Check for HTTPS flag
    use_https = '--https' in sys.argv
    
    print("🚀 Starting DVT Test Report Generator (Refactored)")
    print("=" * 55)
    print("📋 Architecture:")
    print("   • Separated front-end and back-end")
    print("   • Modular business logic")
    print("   • Template-based UI")
    print("   • Static asset management")
    print("")
    print("📁 File Structure:")
    print("   • main.py - FastAPI application")
    print("   • frontend/ - HTML pages")
    print("   • static/ - CSS/JS assets")
    print("   • core/ - Business logic modules")
    print("")
    
    if use_https:
        if os.path.exists('server.crt') and os.path.exists('server.key'):
            print(f"🔒 HTTPS interface: https://localhost:8000")
            print(f"📚 API docs: https://localhost:8000/docs")
            print("✅ Secure downloads enabled - No Chrome warnings!")
        else:
            print("❌ SSL certificates not found. Please run:")
            print("   python generate_cert.py")
    else:
        print(f"🌐 HTTP interface: http://localhost:8000")
        print(f"📚 API docs: http://localhost:8000/docs")
        print("💡 To avoid Chrome download warnings:")
        print("   1. Run: python generate_cert.py")
        print("   2. Run: python main.py --https")
    
    print("")
    if not ai_client:
        print("⚠️  Note: Set GEMINI_API_KEY environment variable for AI features")
    else:
        print("✅ AI features enabled with Gemini integration")
    print("=" * 55)
    
    # Start server with or without SSL
    if use_https:
        uvicorn.run(app, host="0.0.0.0", port=8000, 
                   ssl_keyfile="server.key", ssl_certfile="server.crt")
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
