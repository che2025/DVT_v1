"""
AI Configuration module for DVT Test Report Generator
"""

import os
from google import genai
from google.genai.types import (
    GenerateContentConfig,
    ThinkingConfig,
    GenerateContentResponse,
)

def configure_ai():
    """Configure and return AI client using Vertex AI"""
    # Check if Vertex AI environment variables are set
    project = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_LOCATION')
    use_vertexai = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')
    
    if project and location and use_vertexai == 'true':
        # Configure for Vertex AI - uses application-default credentials
        client = genai.Client()
        return client
    else:
        return None
