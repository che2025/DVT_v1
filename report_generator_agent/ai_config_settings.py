"""
Configuration setti        "test_method_loss": 10000,       # Large for detailed reports
        "test_result_summary": 20000,   # Very large for comprehensive summaries
        "protocol_deviations": 10000,   # Large for multiple deviations
        "defective_unit_investigations": 10000  # Large for multiple investigations
    } for DVT AI Agents
Centralized settings for models, temperatures, and other parameters
"""

from typing import Dict, Any


class AgentConfig:
    """Configuration for AI agents and their behavior"""
    
    # Model settings
    DEFAULT_MODEL = "gemini-2.5-flash"
    
    # Temperature settings by task
    TASK_TEMPERATURES = {
        "scope_and_purpose": 0.5,      # Lower for consistency
        "reference_section": 0.3,      # Very low for accuracy
        "test_procedure": 0.6,         # Medium for natural writing  
        "acronyms_definitions": 0.2,   # Very low for extraction
        "device_config": 0.4,          # Low-medium for data processing
        "connection_test": 0.1,        # Minimal for test
        "protocol_analysis": 0.3,      # Low for factual extraction
        "test_method_loss": 0.4,       # Low-medium for investigation reports
        "test_result_summary": 0.3,    # Low for data extraction accuracy
        "protocol_deviations": 0.4,    # Low-medium for structured formatting
        "defective_unit_investigations": 0.4,  # Low-medium for investigation reports
        "conclusion": 0.5              # Medium for analysis and synthesis
    }
    
    # Content limits
    CONTENT_LIMITS = {
        "protocol_content": 3000,      # Characters for scope/purpose
        "report_content": 4000,        # Characters for reference scanning
        "procedure_content": 4000,     # Characters for procedure summary
        "complete_report": 6000,       # Characters for acronyms scanning
        "protocol_analysis": 2000,     # Characters for quick analysis
        "deviations_content": 5000     # Characters for deviation data processing
    }
    
    # Target specifications
    TARGET_SPECS = {
        "procedure_word_count": 200,   # Target words for procedure summary
        "procedure_elements": 5,       # Required elements in summary
        "max_retry_attempts": 3        # Max retries for failed operations
    }
    
    # Knowledge base settings
    KNOWLEDGE_BASE = {
        "enable_document_metadata": True,
        "enable_acronym_lookup": True,
        "enable_definitions_lookup": True,
        "fallback_to_tbd": True
    }
    
    @classmethod
    def get_temperature(cls, task_name: str) -> float:
        """Get temperature setting for a specific task"""
        return cls.TASK_TEMPERATURES.get(task_name, 0.7)
    
    @classmethod
    def get_content_limit(cls, content_type: str) -> int:
        """Get content limit for a specific content type"""
        return cls.CONTENT_LIMITS.get(content_type, 3000)
    
    @classmethod
    def get_target_spec(cls, spec_name: str) -> Any:
        """Get target specification for a parameter"""
        return cls.TARGET_SPECS.get(spec_name)


class PromptConfig:
    """Configuration for prompt templates and formatting"""
    
    # Common instruction patterns
    COMMON_INSTRUCTIONS = {
        "professional_style": "Use professional technical writing style",
        "ms_word_format": "Format for MS Word document",
        "no_extra_text": "Do not include extra explanations or headers",
        "exact_format": "Use EXACTLY the format shown",
        "sort_alphabetically": "Sort items alphabetically"
    }
    
    # Output format requirements
    OUTPUT_FORMATS = {
        "markdown_table": "Return as properly formatted markdown table",
        "paragraph_only": "Return ONLY the paragraph content",
        "structured_sections": "Return with specific section formatting"
    }
    
    # Exclusion patterns
    EXCLUSIONS = {
        "common_words": ["THE", "AND", "OR", "BUT", "FOR", "TO", "OF", "IN", "ON", "AT"],
        "ignore_patterns": ["TBD", "N/A", "---"]
    }


class ErrorConfig:
    """Configuration for error handling and fallbacks"""
    
    # Error messages
    ERROR_MESSAGES = {
        "ai_not_configured": "⚠️ AI client not configured",
        "generation_failed": "AI generation failed",
        "content_empty": "No content provided for analysis",
        "parsing_failed": "Failed to parse AI response"
    }
    
    # Fallback content
    FALLBACK_CONTENT = {
        "scope_purpose": "Scope and purpose will be generated from protocol content",
        "references": "Reference section will be populated from document analysis",
        "procedure": "Test procedure summary will be extracted from protocol",
        "acronyms": "Acronyms and definitions will be generated from report scan",
        "deviations": "No deviations.",
        "defective_unit_investigations": "No defective unit investigations available."
    }
    
    # Retry settings
    RETRY_CONFIG = {
        "max_attempts": 3,
        "backoff_factor": 2,
        "timeout_seconds": 30
    }
