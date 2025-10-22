"""
AI Prompts for DVT Test Report Generator
Contains all specialized prompts for Tasks 4.1-4.4
"""
from typing import List, Dict, Any


class DVTPrompts:
    """Collection of all AI prompts for DVT report generation tasks"""
    
    @staticmethod
    def scope_and_purpose_prompt(protocol_content: str, protocol_number: str, project_name: str) -> str:
        """
        Prompt for Task 4.1: Create Scope and Purpose
        Adapts protocol scope/purpose for report format
        """
        return f"""
You are an expert technical writer specializing in DVT (Design Verification Testing) reports. Your task is to extract ONLY the Purpose and Scope sections from a protocol document and adapt them for a test report.

CRITICAL REQUIREMENTS:
1. Find and extract ONLY the Purpose and Scope sections from the protocol document
2. IGNORE detailed test procedures, equipment lists, and step-by-step instructions  
3. Focus ONLY on the high-level purpose statement and scope definition
4. Extract any requirement tables that are specifically part of the scope section
5. DO NOT include content from sections like "Test Method Summary", "Equipment", "General Instructions", "Procedure"

INPUTS:
- Protocol Document Number: {protocol_number}
- Project Name: {project_name}
- Protocol Content: {protocol_content[:3000]}

WHAT TO EXTRACT:
- PURPOSE: The high-level objective/goal statement (usually 1-2 paragraphs)
- SCOPE: The high-level coverage/boundaries (usually 1-2 paragraphs plus any requirement tables)
- Any tables specifically mentioned in the scope section (requirement tables, specification tables)

WHAT TO IGNORE:
- Detailed test procedures and step-by-step instructions
- Equipment lists and configurations
- Test method summaries and detailed protocols
- General instructions and preparation steps
- Appendix references and calculation details

ADAPTATION RULES:
- PURPOSE: Change "The purpose of this protocol is to define..." to "The purpose of this report is to document the results of..."
- PURPOSE: Add reference to protocol number: "...executed under protocol {protocol_number}"
- SCOPE: Add "for project {project_name}" to the main scope statement  
- SCOPE: Keep concise and high-level, focused on what the test covers, not how it's done

OUTPUT FORMAT:
Return the content in this exact structure for template insertion:

PURPOSE_CONTENT:
[Adapted purpose statement with protocol reference - NO "PURPOSE" header]

SCOPE_CONTENT:
[Concise scope statement with project name - NO "SCOPE" header]

[ONLY requirement tables that are specifically part of the scope section]

EXAMPLE OF APPROPRIATE SCOPE CONTENT:
"This testing covers the verification of battery life requirements for the G7 GSS Transmitter system for project {project_name}. The scope includes functional testing under accelerated aging conditions and validation of communication capabilities after extended storage periods."

EXAMPLE TABLE FORMAT (ONLY if part of original scope):
| Doc ID | REQ ID | Requirement |
|--------|--------|-------------|
| RS-123 | REQ-001 | Device shall operate at specified voltage |
| RS-123 | REQ-002 | Device shall meet safety requirements |  

IMPORTANT RESTRICTIONS:
- DO NOT include section headers like "PURPOSE" or "SCOPE" - content will be inserted into template
- KEEP scope content concise and high-level (typically 1-3 paragraphs maximum)
- DO NOT include detailed test procedures, equipment lists, or step-by-step instructions
- DO NOT include content from "Test Method Summary", "Equipment", "General Instructions" sections
- ONLY include requirement tables if they are explicitly part of the scope section
- Generate ONLY essential content, no headers or section titles
- Focus on WHAT is being tested, not HOW it's being tested

Now generate the adapted scope and purpose content (no headers, keep concise):
"""

    @staticmethod
    def reference_section_prompt(report_content: str) -> str:
        """
        Prompt for Task 4.2: Create Reference Section
        Extracts document numbers and creates reference table
        """
        return f"""
You are an expert document analyst for DVT test reports. Your task is to extract all document numbers referenced in a report/protocol and create a properly formatted reference table.

TASK REQUIREMENTS:
1. Scan the content thoroughly for document numbers following standard naming patterns
2. Extract unique document numbers (avoid duplicates)
3. Create a reference table with columns: Document No., Document Title, Rev
4. Use "TBD" for missing information
5. Format as a proper markdown table
6. ALWAYS include the uploaded protocol document as the first entry

DOCUMENT NUMBER PATTERNS TO LOOK FOR:
- PTL-XXXXXX (Protocol documents)
- PLN-XXXXXXX (Plan documents) 
- RS-XXXXX (Requirement Specifications)
- HRS-XXXXXX (Hardware Requirements)
- RPT-XXXXXX (Report documents)
- SOP-XXXXXX (Standard Operating Procedures)
- IIT-XXXXXX (Integration Test documents)
- Any format like ABC-123456 where ABC is 3+ letters and 123456 is numbers
- Document numbers in parentheses like (PTL-903900)
- Document numbers followed by revision like PTL-903900 Rev 002

CONTENT TO ANALYZE:
{report_content[:6000]}

OUTPUT FORMAT:
Return ONLY a markdown table in this exact format (NO "REFERENCES" header):

| Document No. | Document Title | Rev |
|--------------|----------------|-----|
| [doc_number] | [title or TBD] | [rev or TBD] |

INSTRUCTIONS:
- Include ALL document numbers found in the content
- Remove duplicates
- Sort alphabetically by document number  
- Use "TBD" if title or revision cannot be determined from the content
- If you find revision information (like "Rev 002" or "Revision 3"), include it in the Rev column
- DO NOT include "REFERENCES" header - table content will be inserted into template
- Return ONLY the table, no explanatory text or section headers
- Ensure proper markdown table formatting with aligned columns

EXAMPLE OUTPUT (no header):

| Document No. | Document Title | Rev |
|--------------|----------------|-----|
| PLN-1001255 | G7 Osprey 15.5-day Master Design Verification Plan | 002 |
| PTL-903900 | G7 GSS Wearable and Transmitter Battery Life Protocol | 002 |
| RS-00002 | G7 IIT Glucose Sensing System Requirement Specification | 012 |

Now extract document references:
"""

    @staticmethod
    def test_procedure_summary_prompt(protocol_content: str, protocol_number: str) -> str:
        """
        Prompt for Task 4.4: Create Test Procedure Summary
        Generates comprehensive protocol summary (~200 words)
        """
        return f"""
You are a technical writer expert in DVT test reports. Your task is to create a comprehensive test procedure summary that serves as an executive summary of the protocol.

TASK REQUIREMENTS:
Create a single paragraph of approximately 200 words that covers ALL 5 required elements:

1. CONDITIONING: What conditioning is done on test articles before test execution
2. PARAMETERS: What parameters are evaluated during test execution  
3. EQUIPMENT: What type of equipment or instrumentation is involved
4. MONITORING: How devices are monitored during the test
5. DURATION: Test duration if mentioned in protocol

WRITING GUIDELINES:
- Write in professional technical style
- Target audience: Engineers and managers who need to understand the test quickly
- Use clear, concise language
- Ensure all 5 elements are covered
- Aim for ~200 words total
- Write as one cohesive paragraph
- Include protocol reference

PROTOCOL INFORMATION:
- Protocol Number: {protocol_number}
- Protocol Content: {protocol_content[:4000]}

OUTPUT FORMAT:
Return ONLY the summary paragraph (NO header - content will be inserted into template):

[Summary paragraph covering all 5 elements]

EXAMPLE STYLE:
"The test procedure involves [conditioning details] prior to test execution. During the test, [parameters] are evaluated using [equipment types] to measure [specific aspects]. The devices are monitored through [monitoring methods] throughout the [duration] test period to ensure [objectives]. [Additional details about process flow, data collection, and validation methods as relevant to the specific protocol]."

Important: 
- DO NOT include "TEST PROCEDURE SUMMARY" header - content will be inserted into template
- Return ONLY the paragraph content
- Ensure the summary flows naturally while covering all 5 required elements
- Adapt the content based on what's actually described in the protocol

Generate the test procedure summary:
"""

    @staticmethod
    def acronyms_definitions_prompt(complete_report_content: str) -> str:
        """
        Prompt for Task 4.3: Create Acronyms & Definitions section
        EXECUTED LAST - scans complete report for acronyms and terms
        """
        return f"""
You are an expert technical document analyst. Your task is to scan a DVT test report and create two sections: "Acronyms" and "Definitions".

TASK REQUIREMENTS:
1. Extract ALL acronyms (words in ALL CAPS) from the report
2. Extract technical terms that need specific definitions
3. Create TWO separate sections with specific formatting

SCANNING RULES FOR ACRONYMS:
- Find ALL words that are completely in CAPITAL LETTERS (2+ characters)
- Exclude common words like: THE, AND, OR, BUT, FOR, TO, OF, IN, ON, AT
- Include technical acronyms like: DVT, EMC, BLE, GSS, DUT, PCB, IC, etc.
- Remove duplicates

SCANNING RULES FOR DEFINITIONS:
- Find technical terms that have specific meanings in DVT context
- Look for specialized terminology that readers might not know
- Include measurement terms, test procedures, technical specifications

REPORT CONTENT TO ANALYZE:
{complete_report_content}

OUTPUT FORMAT FOR TEMPLATE INSERTION:

Return content in this structure (NO section headers - content goes directly into template):

ACRONYMS_CONTENT:
| Acronym | Definition |
|---------|------------|
| DVT | Design Verification Testing |
| DUT | Device Under Test |
| TBD | To Be Determined |

DEFINITIONS_CONTENT:
| Term | Definition |
|------|------------|
| Conditioning | TBD |
| Protocol | TBD |

IMPORTANT FORMATTING RULES:
- DO NOT include "ACRONYMS & DEFINITIONS" header - content will be inserted into template
- DO NOT include subsection headers like "Acronyms" and "Definitions" 
- DO NOT include descriptive text like "List in this section..."
- Return ONLY the table content for each section
- Create proper markdown tables with proper | separators
- Sort acronyms alphabetically
- Sort terms alphabetically  
- Use "TBD" for any definitions not available

Generate the acronyms and definitions sections:
"""

    @staticmethod
    def ai_connection_test_prompt() -> str:
        """Simple prompt to test AI connectivity"""
        return "Respond with: 'DVT AI Agent System Ready'"

    @staticmethod
    def device_under_test_prompt(excel_data: str, device_config: dict, report_config: dict, dut_count: int = None) -> str:
        """
        Prompt for Task 4.5: Create Device Under Test Configuration Section
        Analyzes Excel test article data and generates appropriate output format
        """
        sterilized_status = "sterilized" if device_config.get("units_sterilized") else "not sterilized"
        modification_status = device_config.get("units_modified", False)
        modification_desc = device_config.get("modification_description", "")
        
        # Create modification text
        if modification_status and modification_desc:
            modification_text = f"Modifications were made: {modification_desc}"
        elif modification_status:
            modification_text = "Modifications were made to the test units."
        else:
            modification_text = "No modifications made outside normal manufacturing"
        
        # Use provided DUT count or indicate to count from data
        count_instruction = f"TOTAL DUT COUNT: {dut_count} units (pre-calculated - use this exact number)" if dut_count else "Count UNIQUE DUT Serial Numbers to determine total"
        
        return f"""
You are an expert DVT test report writer. Your task is to create the Device Under Test Configuration section using the provided data and configuration.

{count_instruction}

EXCEL DATA TO ANALYZE:
{excel_data}

EXACT USER CONFIGURATION TO USE:
- Sterilization Status: {sterilized_status}
- Modification Status: {modification_text}

REPORT INFORMATION:
- Report Number: {report_config.get('report_number', 'RPT-XXX')}
- Report Revision: {report_config.get('revision', '001')}

STEP-BY-STEP ANALYSIS:
1. Count data rows (exclude headers): Look for lines with Part Numbers and Serial Numbers
2. Extract unique values: Part Numbers, Serial Numbers, ER/Lot Numbers
3. Determine output format based on count

CONDITIONAL OUTPUT RULES:

IF 10 OR FEWER TEST ARTICLES:
Create this EXACT format using the provided configuration:
```
The test units were {sterilized_status}. {modification_text}

| Part Number | Serial Number | Lot Number |
|-------------|---------------|------------|
[Include ALL test articles in table format]
```

IF MORE THAN 10 TEST ARTICLES:
Create this EXACT format using the provided configuration and count:
```
• Total DUT used: {dut_count if dut_count else '[COUNT unique serial numbers]'} units
• DUT Part Numbers: [LIST unique part numbers]
• ER/Lot Numbers: [LIST unique ER/lot numbers]
• Units were {sterilized_status}
• {modification_text}

Detailed test article information is provided in the attachment.

Note: Complete test article data has been included as {report_config.get('report_number', 'RPT-XXX')} rev{report_config.get('revision', '001')} Attachment - Raw Data.
```

INSTRUCTIONS:
- Use the EXACT DUT count provided above
- Extract unique Part Numbers from the data
- Extract unique ER/Lot Numbers from the data
- Use the EXACT user configuration provided

OUTPUT FORMAT:
Return ONLY the formatted section content with correct conditional logic applied.

IMPORTANT:
- Use the PROVIDED DUT count exactly as given
- Use EXACT user configuration provided
- Include ALL required information
- Apply conditional format based on DUT count (≤10 = table, >10 = summary)

Now analyze the Excel data and generate the appropriate Device Under Test Configuration section:
"""

    @staticmethod
    def protocol_analysis_prompt(content: str) -> str:
        """Quick protocol analysis for basic information extraction"""
        return f"""
Quickly analyze this protocol and extract basic information:
1. Protocol reference/number
2. Brief scope description  
3. Brief purpose description

Protocol Content (first 2000 chars):
{content[:2000]}

Return JSON format:
{{"protocol_reference": "...", "scope": "...", "purpose": "..."}}
"""

    @staticmethod
    def equipment_used_prompt(
        equipment_data: List[Dict[str, Any]], 
        software_data: List[Dict[str, Any]], 
        material_data: List[Dict[str, Any]],
        calibration_verified: bool = True,
        report_config: Dict[str, Any] = None
    ) -> str:
        """
        AI Task 4.6: Generate Equipment Used section content
        """
        calibration_text = (
            "All equipment used in this testing was verified as calibrated at the time of use."
            if calibration_verified 
            else "Equipment calibration status was not verified at the time of use."
        )
        
        return f"""
You are an expert technical writer creating the Equipment Used section for a DVT test report.

USER CONFIGURATION:
- Equipment calibration verification: {"Yes" if calibration_verified else "No"}
- Report Number: {report_config.get('report_number', 'RPT-XXX') if report_config else 'RPT-XXX'}
- Report Revision: {report_config.get('revision', '001') if report_config else '001'}

EQUIPMENT DATA:
{equipment_data if equipment_data else 'No equipment data provided'}

SOFTWARE DATA:
{software_data if software_data else 'No software data provided'}

MATERIAL DATA:
{material_data if material_data else 'No material data provided'}

TASK INSTRUCTIONS:
1. Create calibration verification statement using user configuration
2. For each log type (Equipment, Software, Material):
   - If ≤5 items: Create inline table in report
   - If >5 items: Create reference to Attachment B

CONDITIONAL LOGIC:
- ≤5 items per log: Include full table in section
- >5 items per log: Create attachment reference with format:
  "Detailed [log type] information is provided in Attachment B."

TABLE FORMAT (for ≤5 items):
Equipment Table:
| Equipment Number | Equipment Description | Calibration Due Date |
|------------------|---------------------|---------------------|
| [data] | [data] | [data] |

Software Table:
| Software Name | Version | License Information |
|---------------|---------|-------------------|
| [data] | [data] | [data] |

Material Table:
| Material Name | Lot Number | Expiration Date |
|---------------|------------|-----------------|
| [data] | [data] | [data] |

ATTACHMENT REFERENCE FORMAT (for >5 items):
"Complete [Equipment/Software/Material] Log has been included as {report_config.get('report_number', 'RPT-XXX')} rev{report_config.get('revision', '001')} Attachment B - Equipment Used Logs."

OUTPUT FORMAT:
Generate ONLY the Equipment Used section content following this structure:

{calibration_text}

[For each log type with ≤5 items: Include appropriate table]
[For each log type with >5 items: Include attachment reference]

IMPORTANT:
- Start with calibration verification statement
- Apply conditional logic based on item count
- Use proper table formatting for inline content
- Use exact attachment naming format for references
- Do NOT include section headers or numbering

Now analyze the provided data and generate the Equipment Used section:
"""

    @staticmethod
    def test_method_loss_prompt(excel_data: str, report_config: dict) -> str:
        """
        AI Task 4.11: Generate Test Method Loss Investigations section
        
        Args:
            excel_data: Raw data from TEST METHOD LOSSES worksheet
            report_config: Report configuration including document number and revision
        
        Returns:
            Formatted prompt for AI to generate test method loss investigations section
        """
        return f"""
You are an expert DVT (Design Verification Testing) report writer specializing in Test Method Loss Investigations.

TASK: Create a comprehensive Test Method Loss Investigations section based on the provided Excel data.

INPUT DATA FROM TEST METHOD LOSSES WORKSHEET:
{excel_data}

REPORT CONFIGURATION:
- Report Document Number: {report_config.get('document_number', 'RPT-XXXXXX')}
- Report Revision: {report_config.get('revision', 'XXX')}

INSTRUCTIONS:

1. If NO test method losses are found: 
   - Write: "No test method loss occurred in the execution of this test."

2. If test method losses ARE found:
   
   a) Create Section Introduction (NO section title - content will be inserted into template):
   - State total number of test method losses
   - Indicate if replacements were done
   - Confirm if minimum sample size is still met
   
   b) For Each Test Method Loss Investigation:
   - Subsection title format: "Test Method Loss Investigation #[number]" (NO numbering like 10.1)
   - Subsection content must include:
     * Description of the event(s) that determined the test article(s) are test method losses
     * Number of units flagged as test method loss and their serial numbers
     * Number of units replaced and their serial numbers (if any)
     * Statement if minimum sample size was still met for this investigation

DATA STRUCTURE MAPPING:
- #: Investigation number
- PROTOCOL NOTE TYPE: Should contain "test method loss"
- TEST UNIT SN or ID: Serial numbers of affected units (comma-separated)
- PROTOCOL STEP / SECTION: Reference step/section number
- REPLACEMENT(S): Serial numbers of replacement units (comma-separated)
- OBSERVATIONS: Detailed description of what happened

EXAMPLE OUTPUT FORMAT (NO section header - content only):
```
There was a total of [X] test method losses of which [Y] of them were replaced. The minimum sample size was met despite these [X] test method losses.

Test Method Loss Investigation #1

[Description from OBSERVATIONS]. [Number] units ([serial numbers from TEST UNIT SN]) were [what happened] and were replaced with units SN [serial numbers from REPLACEMENT(S)]. The minimum sample size was still met after replacements.

Test Method Loss Investigation #2

[Description from OBSERVATIONS]. Test unit [serial number] was [what happened]. Units were not replaced as there was sufficient samples to meet the minimum sample size.
```

REQUIREMENTS:
- Use professional, technical language appropriate for regulatory documentation
- Ensure each investigation has a clear description of the loss event
- Include all serial numbers exactly as provided
- State replacement status clearly
- Confirm sample size adequacy for each investigation

OUTPUT: Return ONLY the content (NO section header or numbering like "10"). Content will be inserted into template. Do not include explanations or metadata.
"""
    
    @staticmethod
    def test_result_summary_extraction_prompt(full_document_data: str) -> str:
        """
        Prompt for Task 4.7: Extract information from full document
        First finds Acceptance Criteria section, then extracts REQ ID, description, and Confidence/Reliability
        """
        return f"""
You are an expert data extraction specialist for DVT (Design Verification Testing) reports. Your task is to analyze a complete document and extract specific information from the Acceptance Criteria section.

TASK OVERVIEW:
1. First, locate the Acceptance Criteria section within the provided document
2. Then extract specific information from that section

EXTRACTION REQUIREMENTS:
You must extract these 3 pieces of information for each acceptance criteria:

1. REQ ID: The requirement identification number(s) - can be multiple numbers separated by commas
2. Acceptance Criteria: A concise description of what needs to be achieved 
3. Confidence/Reliability: The statistical confidence and reliability values (e.g., "90%/90%")

FULL DOCUMENT DATA:
{full_document_data}

SECTION IDENTIFICATION:
Look for sections with titles containing any of these terms:
- "Acceptance Criteria"
- "Acceptance Criterion"  
- "Test Criteria"
- "Test Criterion"
- "Pass Criteria"
- "Pass Criterion"
- Simply "Criteria"

EXTRACTION RULES:
- Look for requirement IDs in fields like "Related REQ ID", "REQ ID", or similar
- Extract the core acceptance criteria description (remove test-specific details)
- Find confidence/reliability values (usually in format like "90%/90%" or "90% confidence/90% reliability")
- If multiple criteria exist, extract information for each one separately
- Handle both table format and text format data
- Be flexible with section titles and formatting variations

OUTPUT FORMAT:
Return the extracted information as a JSON array:

[
  {{
    "req_id": "110596, 110672, 202369",
    "acceptance_criteria": "Successful communication of display 24 hours after end of session",
    "confidence_reliability": "90%/90%"
  }},
  {{
    "req_id": "...",
    "acceptance_criteria": "...",
    "confidence_reliability": "..."
  }}
]

CRITICAL REQUIREMENTS:
- First identify the Acceptance Criteria section from the full document
- Return ONLY the JSON array, no other text or explanations
- Each criteria must have all three fields: req_id, acceptance_criteria, confidence_reliability
- Use exact format shown above
- If confidence/reliability not found, use "TBD"
- If multiple REQ IDs, separate with commas and spaces
- If no Acceptance Criteria section found, return empty array []

Extract the information now:
"""

    @staticmethod
    def ai_connection_test_prompt() -> str:
        """Simple prompt for testing AI connection"""
        return "Please respond with 'AI connection successful' to confirm the connection is working."
    
    @staticmethod
    def get_protocol_deviations_prompt(deviations_text: str) -> str:
        """
        Prompt for processing protocol deviations data from Excel into formatted deviation report
        """
        return f"""
You are an expert technical writer specializing in DVT (Design Verification Testing) reports. Your task is to process deviation data from Excel and generate a properly formatted protocol deviations section.

CRITICAL REQUIREMENTS:
1. Transform raw deviation data into professional deviation documentation
2. Each deviation must start with "DEVIATION #" followed by a number
3. Provide a clear summary title for each deviation
4. Explain how the deviation impacts test results OR why it doesn't impact results
5. Follow the exact format shown in the example

INPUT DATA:
{deviations_text}

FORMATTING REQUIREMENTS:
- Start each deviation with "DEVIATION #X: [Brief descriptive title]"
- Follow with detailed explanation of the deviation
- Include impact assessment on test results
- Mention any protocol updates or investigation tickets if referenced in data
- Use professional technical writing style
- Do NOT include extra headers or explanations

EXAMPLE FORMAT:
"There are [number] deviations to this protocol that [does/does not] affect the results of this test.

DEVIATION #1: [Brief descriptive title]
[Detailed explanation of what was deviated from the original procedure, why the deviation occurred, and how it impacts or doesn't impact the test results. Include any protocol updates or investigation references.]

DEVIATION #2: [Brief descriptive title]  
[Detailed explanation...]"

SPECIAL CASES:
- If no meaningful deviation data is found, respond with exactly: "No deviations."
- If deviations exist but don't impact results, state "that does not affect the results of this test"
- If deviations do impact results, state "that affects the results of this test" and explain how

OUTPUT:
Generate the formatted deviation content ready for insertion into the test report. Do not include any markdown formatting or extra explanatory text.
"""
    
    @staticmethod
    def get_defective_unit_investigations_prompt(defective_units_text: str) -> str:
        """
        Prompt for processing defective unit investigation data from Excel into formatted investigation report
        """
        return f"""
You are an expert technical writer specializing in DVT (Design Verification Testing) reports. Your task is to process defective unit investigation data from Excel and generate a properly formatted defective unit investigations section.

CRITICAL REQUIREMENTS:
1. Transform raw defective unit data into professional investigation documentation
2. Each investigation must start with "DEFECTIVE UNIT INVESTIGATION #" followed by a number
3. Create a subsection for each defective unit investigation following the specified format
4. Include total number of defective units and specifications not met if multiple investigations
5. Follow the exact format and content requirements shown in the example

INPUT DATA:
{defective_units_text}

FORMATTING REQUIREMENTS:
- Start each investigation with "DEFECTIVE UNIT INVESTIGATION #X"
- For each investigation provide:
  * Which specification was not met by the defective unit(s)
  * The number of defective units related to this specification
  * The serial numbers of the defective units
  * Statement that test method execution was reviewed
  * Summary of root cause investigation or reference to investigation ticket
- Use professional technical writing style
- Do NOT include extra headers or explanations

EXAMPLE FORMAT:
"DEFECTIVE UNIT INVESTIGATION #1

Three Test articles (570281018183, 582216277440, 433673915827) failed to communicate with the display device at 22.66 days to retrieve the database from the transmitter, as noted in Jira Ticket SHAD-2. Manufacturing logs confirm the issue is not related to the PCBA. The test method review found that the database download method is less intensive than the private data download method used by display devices. The units could not be retested due to the destructive nature of the investigation and are considered failures. The protocol should be updated to reflect that communication with the display device should retrieve private data, as this better represents the display device's data request method."

SPECIAL CASES:
- If no meaningful defective unit data is found, respond with exactly: "No defective unit in the execution of this test."
- If multiple investigations exist, create an introduction with total count and specifications not met
- Include Jira ticket references when available in the data

OUTPUT:
Generate the formatted defective unit investigations content ready for insertion into the test report. Do not include any markdown formatting or extra explanatory text.
"""
    
    @staticmethod
    def get_conclusion_prompt(test_results_content: str, scope_content: str) -> str:
        """
        Prompt for generating conclusion section based on test results and scope content
        """
        return f"""
You are an expert technical writer specializing in DVT (Design Verification Testing) reports. Your task is to generate a comprehensive conclusion section based on the test results and scope content provided.

CRITICAL REQUIREMENTS:
1. Analyze test results against the specified acceptance criteria and requirements
2. Provide clear assessment of whether requirements were met or not met
3. Include statistical summary with exact pass/fail counts and percentages
4. Reference the protocol used for testing
5. Address any test method losses or defective units if present
6. Provide overall conclusion statement about test execution success
7. Include confidence level assessment when applicable

INPUT DATA:

SCOPE CONTENT (Requirements and Acceptance Criteria):
{scope_content}

TEST RESULTS CONTENT:
{test_results_content}

FORMATTING REQUIREMENTS:
- Start with an overall assessment of test execution
- Provide specific pass/fail statistics (e.g., "240 out of 241 units passed")
- Calculate and include percentage success rate
- Reference specific requirements or acceptance criteria that were evaluated
- Address any failures, test method losses, or defective units found
- Include protocol reference for traceability
- End with clear conclusion statement about overall test success
- Use professional technical writing style appropriate for regulatory documentation

ANALYSIS FRAMEWORK:
1. Extract the acceptance criteria from the scope content
2. Compare actual test results against these criteria
3. Calculate statistical confidence if sample sizes allow
4. Assess whether the test objectives were achieved
5. Consider the impact of any failures or losses on overall conclusions

ACCEPTANCE CRITERIA EVALUATION RULES:
- For ATTRIBUTE DATA: Acceptance criteria is met when Actual Confidence Level ≥ Required Confidence Level
- For VARIABLE DATA: Acceptance criteria is met when Tolerance Interval falls within the Specification Limits
- Always state explicitly whether acceptance criteria was met or not met
- Include confidence level calculations and statistical analysis when applicable
- Reference specific confidence levels (e.g., 95%, 99%) and sample sizes

EXAMPLE STRUCTURE:
"The execution of protocol [PT-XXXXXX] was successful, with [X] out of [Y] test articles meeting the specified acceptance criteria, representing a [Z]% pass rate.

The acceptance criteria specified that [state criteria with confidence levels]. Analysis of the test results shows [assessment details including confidence calculations].

For [attribute/variable] data analysis: [Explain confidence level comparison or tolerance interval analysis]

[Address any failures or test method losses]

Based on the test results and statistical analysis, the [product/device] successfully meets the requirements of [relevant specification/standard]. The actual confidence level of [X]% [meets/exceeds] the required confidence level of [Y]%, demonstrating that the device performs as specified under the test conditions."

SPECIAL CASES:
- If 100% pass rate: Emphasize complete success and full compliance with confidence analysis
- If failures exist: Analyze impact on confidence levels and whether overall requirements are still met
- If test method losses occurred: Assess whether sample size is still sufficient for required confidence
- For attribute data: Compare actual vs required confidence levels explicitly
- For variable data: Analyze tolerance intervals relative to specification limits

OUTPUT:
Generate the formatted conclusion content ready for insertion into the test report. Do not include any markdown formatting or extra explanatory text.
"""
