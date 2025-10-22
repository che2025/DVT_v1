1	Summary	2

2	Problem Statement	2

3	Use Case	2

4	AI Tasks	3

4.1	Create Scope and Purpose	3

4.2	Create Reference Section	4

4.3	Create Acronyms & Definitions section	5

4.4	Create Test Procedure Summary	6

4.5	Create Device Under Test Configuration Section	7

4.6	Create the Equipment Used Section	8

4.7	Create Test Result Summary Section	9

4.8	Create the Test results Details section	12

4.9	Create Protocol Deviations Section	14

4.10	Create Defective Unit Investigations section	15

4.11	Create Test Method Loss Investigations section	16

4.12	Create the Conclusion section	17

4.13	Create Report Document and Attachments in Sharepoint with specific filename format	18





# Summary

An AI agent that takes as inputs Excel files, Test files (.cvs), Jira Ticket number and uses a knowledge base of protocols, common acronyms and definitions, to create a test report and its attachment following a specific MS Word Template.

# Problem Statement

DVT reports can take from 1 to 5 days to complete.

Small projects have typically 5-10 reports when bigger projects can have 20-40 test reports to complete.

Content organization in DVT reports is not consistent between teams and even projects.

# 3 Use Case High Level Details

## 3.1 Files types that can be used with this use case:

All these files types would be accessible through a Sharepoint location

- PDF

- MS OFFICE Suite like, Excel or Word

- Text Files

- JMP Files. Also this file format can be used as well but for a specific purpose:

- Zipped files (these would not be processed, but the agent would change the file name to a specific nomenclature (see section 4.13 for this use case)

## 3.2 Source of data / Systems

- Jira (could be multiple projects in Jira)

- Sharepoint (inputs from the user)

- Sharepoint (knowledge base for common info to use across the AI tasks)



## High Level Process

1. User Accesses the DVT Report Generator Agent through a web UI

2. The user is presented with a form where the agent asks for:

- Document Title, number and revision for the report to create

- Document Number of the protocol used to generate the data

- Which report template to use for this report

- Jira Ticket numbers for each defective unit investigation performed

- The sharepoint location where the input files for the report are located

- The sharepoint location where the report and its attachments should be created

3. The AI agent processes the input files, the Jira Tickets and uses the protocol knowledge base to execute the tasks required to create the test report and its attachments.

4. The AI agent creates the report document and its relevant attachments in the sharepoint location provided by the user.

5. Once the report is created the AI agent checks for common acronyms and definitions from the knowledge base and updates the acronyms and definitions section.

6. The user reviews the documentation created and informs the AI on corrections needed for certain sections (such as: make the defective unit summary more concise, or use bullet points for the conclusion).

7. The AI agent corrects the documents and update the report according to the user’s request.





# 4 AI Tasks

This section describes the tasks that are needed to be performed by the AI.  The tasks goes through each section of the test report and details what are the inputs of the tasks, what are the outputs, the instructions the AI needs to follow and an example.

## 4.1 Create Scope and Purpose

AI agent creates the scope and purpose section of the report using the information from the protocol that was used to execute the test.

### 4.1.1 INSTRUCTIONS:

- After the requester provided the protocol reference that was used to execute the test, the agent looks up the protocol knowledge base to extract the information from the appropriate protocol.

- The agent adapts the scope and purpose of the protocol for a report.

- For the purpose, the agent adds a reference to the protocol document number and revision number used for this report.

- For the scope, the agent adds a reference to the project name as part of the scope for the report.

- The agent writes the scope and purpose text in the report using specific MS Word Paragraph styles.

### 4.1.2 Knowledge Base:

Protocols (from user upload or location in Oracle CPLM or Sharepoint)

### 4.1.3 INPUTS:

- Protocol Document or Number executed

- Project name for the report

### 4.1.4 OUTPUTS:

- Updated Scope and Purpose section of the report

### 4.1.5 EXAMPLE:

- PURPOSE / SCOPE From Protocol: The purpose of this protocol is to define the steps to execute the EMC test. The scope of the protocol applies to the G7 platform. 

- Adapted PURPOSE / SCOPE for the Report: The purpose of this report is to document the results of the EMC test executed under protocol [PTL Number] [PTL REV]. The scope of this report applies to the G7 platform for project [Project Name]. 

## 4.2 Create Reference Section

The AI agent created the reference section of the report which consists of a list of documents that are referenced in the report.

### 4.2.1 INSTRUCTIONS:

- The agent extracts from the report any document number that is referenced. The document number must follow a specific format in accordance with the Doc Number Format knowledge base.

- The agent retrieves the following information for each document number in the document meta data: Document Title, Document Latest Revision

- The agent creates in the reference section a reference table with the following columns: Doc Number, Doc Title, Doc Rev.

- For each document number found in the report, the agent creates a line item in the reference table with the appropriate information.

- If for certain document numbers the agent cannot find a Document Title or Document Latest Revision, the agent will place TBD as placeholder for that information in the reference table.

### 4.2.2 Knowledge base:

- Document Number format

- List of documents meta data (doc number, doc name, doc latest revision)

### 4.2.3 INPUTS:

Test Report

### 4.2.4 OUTPUTS:

Table in the reference section of the report.

### 4.2.5 EXAMPLE:

This is an example of the reference table assuming the agent found Doc Title and Doc Rev for the first 3 documents.

| Document No. | Document Title                                                          | Rev |   |   |
|--------------|-------------------------------------------------------------------------|-----|---|---|
| PTL-903900   | G7 GSS Wearable and Transmitter Battery Life Accelerated Aging Protocol | 002 |   |   |
| PLN-1001255  | G7 Osprey 15.5-day Master Design Verification Plan                      | 002 |   |   |
| RS-00002     | G7 IIT Glucose Sensing System Requirement Specification                 | 012 |   |   |
| HRS-999099   | TBD                                                                     | TBD |   |   |



## 4.3 Create Acronyms & Definitions section

The AI agent created the Acronyms & Definitions section of the report which consists of a list of terms from the acronyms and definitions database that can be found in the report.

### 4.3.1 INSTRUCTIONS:

- The agent extracts from the report any acronyms that is referenced. The acronyms are any word that is in ALL CAPS in the document.

- The agent retrieves the following information for each acronym in the Acronym Knowledge Base: Acronym Definition

- The agent creates in the Acronyms section a table with the following columns: Acronym, Definition.

- For each acronym found in the report, the agent creates a line item in the Acronym table with the appropriate information.

- If for certain Acronym the agent cannot find an Acronym Definition, the agent will place TBD as placeholder for that information in the Acronym table.

### 4.3.2 Knowledge base:

Acronym Knowledge Base

### 4.3.3 INPUTS:

Test Report

### 4.3.4 OUTPUTS:

Table in the Acronym section of the report.

### 4.3.5 EXAMPLE:

| Acronym | Definitions               |   |   |   |
|---------|---------------------------|---|---|---|
| BLE     | Bluetooth Low Energy      |   |   |   |
| GSS     | Glucose Sensing Subsystem |   |   |   |
| ZULU    | TBD                       |   |   |   |
|         |                           |   |   |   |


## 4.4 Create Test Procedure Summary

The AI agent creates a test procedure summary which serves as an executive summary of the protocol.  The goal is to enable the reader to visualize what parameters the protocol verifies; what type of equipment are involved and the duration of the test.

### 4.4.1 INSTRUCTIONS:

- The agent extracts from the protocol, the test procedure summary section and copies it to the report.

- If the protocol does not have a summary, the agent summarizes the test procedure section of the protocol and adds the summary in the Test Procedure section of the report.

- The test procedure summary shall be 1 paragraph of approximately 200 words that gives the reader:

1. Conditioning done on the test article prior to test execution

2. The parameters evaluated during the test execution

3. The type of equipment or instrumentation involved

4. How the device is monitored during the test

5. The duration of the test if mentioned in the protocol

### 4.4.2 Knowledge Base:

Protocols

### 4.4.3 INPUTS:

Protocol Number

### 4.4.4 OUTPUTS:

Test Procedure Summary section in the report

### 4.4.5 EXAMPLE:

| INPUT                  | OUTPUT |   |   |   |
|------------------------|--------|---|---|---|
| [reference a protocol] |        |   |   |   |
|                        |        |   |   |   |



## 4.5 Create Device Under Test Configuration Section

The AI agent retrieves from the data sheets the information related to the test article configuration and reproduces them into the report.

### 4.5.1 INSTRUCTIONS:

- The agent reads the Test Article Log Data Sheets as input for this section.

- The agent asks if the test units were:

    - Sterilized

    - Any modifications were made not related to manufacturing (ex. RC installation)

- If there are 10 or less test articles listed in the Test Article Log, the agent creates a table with the following information for each test article:

    - Test Article Part Number

    - Test Article Serial Number

    - Test Article Lot number

    The agent also adds a paragraph above the table that describes if the units were sterilized and if the units have any modifications made outside of the normal manufacturing.

- If there are more than 10 units, the agent creates a summary using bullet points that includes:

    - Number of DUT used for the test, which is the total number of DUT in the test article log

    - All the unique DUT Part Number used for the test

    - All the unique ER Number or Lot Number used for the test

    - If the units were sterilized

    - Any modifications made to the units that are not part of production.

   The agent copies the Test Article Log as an attachment to the report and names the attachment with the following format:

    - [Report Document Number] rev[report revision number] Attachment A - Test Article Log, where

    - [Report Document Number] is the report number provided by the requester

    - [report revision number] is the report revision number provided by the requester.

### 4.5.2 Knowledge Base

- RDBP Jira Database

### 4.5.3 INPUTS:

- Test Article Log Data Sheet

### 4.5.4 OUTPUTS:

- Updated Device Under Test Configuration section in the report

## 4.6 Create the Equipment Used Section

The AI agent retrieves from the data sheets the information related to the equipment used for the test and reproduces them into the report.

### 4.6.1 INSTRUCTIONS:

- The agent reads the Equipment Log, Software Log and Material Log Data Sheets as input for this section.

- The agent requests from the user if all equipment were verified as calibrated at the time of use. Depending on the response from the user the agent creates a short paragraph that states if the equipment were verified as calibrated or not at time of use.

- If the Equipment Log has 5 or less items, the agent creates a table for Equipment Used which copies the content of the Equipment Log Data Sheet.

- If the Software Log has 5 or less items, the agent creates a table for Software Used which copies the content of the Software Log Data Sheet.

- If the Material Log has 5 or less items, the agent creates a table for Material Used which copies the content of the Material Log Data Sheet.

- If there is more than 5 items in any log:

    - The agent copies the Log in the report folder as an attachment to the report and names the attachment with the following format:

        - [Report Document Number] rev[report revision number] Attachment B - Equipment Used Logs, where:

            - [Report Document Number] is the report number provided by the requester

            - [report revision number] is the report revision number provided by the requester.

### 4.6.2 Knowledge Base:

- None

### 4.6.3 INPUTS:

- Equipment Log Data Sheet

- Software Log Data Sheet

- Material Log Data Sheet

### 4.6.4 OUTPUTS:

- Equipment Used Section completed in the Report

### 4.6.5 EXAMPLES:

## 4.7 Create Test Result Summary Section

The AI agent creates a summary table that gives a quick view of the test results and relevant information relation

### 4.7.1 INSTRUCTIONS:

- The agent extracts from the protocol all the individual acceptance criteria, the type of data analysis (i.e. attribute or variable) and their confidence and reliability targets.

- The agent groups all acceptance criteria that requires an attribute data analysis in the same table with the following columns:

    - Req ID

    - Acceptance Criteria

    - Confidence / Reliability

    - Initial Sample Size

    - Test Method Losses

    - Actual Sample Size

    - Defective Units

    - Actual Confidence / Reliability

    Where:

    - The Req ID is taken from the protocol acceptance criteria section and represents the unique ID related to the acceptance criteria.

    - The acceptance criteria is taken from the protocol acceptance criteria section.

    - The Confidence / Reliability is taken from the protocol risk assessment section and represents the confidence / reliability needed to pass the test.

    - The Initial sample size is taken from the Test Article Log Data Sheet related to each acceptance criteria and is the total number of test article from the data sheet.

    - The test method losses is taken from the Test Article Log Data Sheet and is the total number of test article flagged as Test Method Loss (replaced and not replaced)

    - The actual sample size is the Initial Sample Size minus the Test Method Losses that are not replaced.

    - The Defective Units is taken from the Test Article Log Data Sheet and are the total number of units that are flagged as FAIL in the log.

    - The Actual Confidence / Reliability is the calculated confidence / reliability represented by the actual sample size and number of defective units taken from the Test Article Log Data Sheet.

- The agent groups all acceptance criteria that requires a variable data analysis in the same table with the following columns:

    - Req ID

    - Acceptance Criteria

    - Initial Sample Size

    - Test Method Losses

    - Actual Sample Size

    - Defective Units

    - Tolerance Interval

    - Confidence / Reliability

    Where:

    - The Req ID is taken from the protocol acceptance criteria section and represents the unique ID related to the acceptance criteria.

    - The acceptance criteria is taken from the protocol acceptance criteria section.

    - The Confidence / Reliability is taken from the protocol risk assessment section and represents the confidence / reliability needed to pass the test.

    - The Initial sample size is taken from the Test Article Log Data Sheet related to each acceptance criteria and is the total number of test article from the data sheet.

    - The test method losses is taken from the Test Article Log Data Sheet and is the total number of test article flagged as Test Method Loss (replaced and not replaced)

    - The actual sample size is the Initial Sample Size minus the Test Method Losses that are not replaced.

    - The Defective Units is taken from the Test Article Log Data Sheet and are the total number of units that are flagged as FAIL in the log.

    - The tolerance interval is the calculated statistical tolerance interval from the data in the Test Article Log Data Sheet.

    - The Actual Confidence / Reliability is the calculated confidence / reliability represented by the actual sample size and number of defective units taken from the Test Article Log Data Sheet.

### 4.7.2 Knowledge Base:

- Protocols

### 4.7.3 INPUTS:

- Test Article Log Datasheet for each acceptance criteria of the protocol

### 4.7.4 OUTPUTS:

- Summary Tables in the test summary section.

### 4.7.5 EXAMPLES:

This is an example of a table for acceptance criteria with Attribute data analysis:

| REQ ID                     | Acceptance Criteria                                                   | Confidence / Reliability | Initial Sample Size | Test Method Losses | Actual Sample Size | Defective Units | Actual Confidence / Reliability |
|---------------------------|---------------------------------------------------------------------|---------------------------|----------------------|---------------------|---------------------|------------------|---------------------------------|
| 110596, 110672, 202369   | Successful communication of display 24 hours after end of session with 90%/90% conf/rel | 90% / 90%                | 120                  | 1                   | 119                 | 3                | 99.77% / 90%                   |


This is an example of a table for acceptance criteria with variable data analysis:

| REQ ID                     | Acceptance Criteria                                                   | Initial Sample Size | Test Method Losses | Actual Sample Size | Defective Units | Tolerance Interval (Lower Limit) | Actual Confidence / Reliability |
|---------------------------|---------------------------------------------------------------------|----------------------|---------------------|---------------------|------------------|-----------------------------------|---------------------------------|
| 110596, 202364, 202369   | 95%/90% Lower Limit Tolerance interval of dynamic voltage > 2.0 V at End of Session | 120                  | 1                   | 119                 | 0                | 2.39 V                            | 95% / 90%                       |


## 4.8 Create the Test results Details section

The AI agent gathers from the user the details of the test execution and creates a section that details, the date and location when the conditioning of the test articles occurred and when and where the test was executed, data related to the test that are relevant to the type of analysis conducted for the test.

### INSTRUCTIONS:

The agent request from the user:

The conditioning, execution of test and other important test steps that needs to be reported in the report.

The start and end date of each step

The location the test step was executed

The agent creates a table with the following columns:

Test Step, which is a step for each test step given by the user

Start Date, date at which the test step was started

End Date, date at which the test step was ended

Location, location where the test step was executed

For each acceptance criteria with variable data analysis, the agent will add in the test details section a graphical analysis of the results which includes:

Histogram Distribution and Normality distribution Fit which shows

A line for Lower Specification Limit (LSL) and Upper Specification Limit (USL)

A line for the Lower Tolerance Interval (LTI) and Upper Tolerance Interval (UTL)

A table named Summary Statistics which includes:

Minimum, 25% quartile, Median, 75% quartile, Maximum

Sample Average

Number of Sample

A table named Tolerance Interval with:

Proportion used for the Tolerance Interval Calculation

Lower Tolerance Interval

Upper Tolerance Interval

Confidence used for the Tolerance Interval Calculation

Actual Confidence Level of the calculation

The agent will ask the user for additional elements to add in the test details section. If there are additional elements to add, the agent will request a short description of the elements to add to inspire itself in providing an explanation with the elements to add.

### Knowledge Base:

None

### INPUTS:

User provided with request from the agent

### OUTPUTS:

Updated Test Details section

### EXAMPLES:

The following test steps were executed:

The low limit tolerance interval was calculated for both battery vendor and shown in Figure 1

Figure 1. Analysis of Lower Limit Tolerance Interval for acceptance criteria #2





## Create Protocol Deviations Section

The AI agent parse through the Deviations Datasheet and creates a high level summary of each deviations in this section.

### INSTRUCTIONS:

If there are no deviations found the agent shall write No deviations occurred in the execution of this test in the Deviation section of the report.

The agent creates an introduction of the section that includes the total number of deviations, a statement of if any of the deviations affects the results of the test and the number of deviations that requires an update to the test procedures.

The agent creates a subsection for each deviation from the Deviation Datasheet which includes the following:

Summary of the deviation

Statement about the impact of the deviation on the test results and if the results are still valid.

Statement about actions needed to resolve the deviation. If no action needed, the agent will state no action needed to resolve the deviation.

### Knowledge Base:

None

### INPUTS:

Deviations Data Sheets

JIRA Deviations Records Database

### OUTPUTS:

Deviation section created in the report.

### EXAMPLES:

There are two deviations to this protocol that does not affect the results of this test.

8.1 DEVIATION #1: Simulated manufacturing temperatures

Units did not go through the manufacturing process to get exposed to the process temperatures of the conductive epoxy. To account for the potential impact of this step on the battery life, the devices were placed into an oven at 80C / 60 min (uncontrolled RH). The temperature and exposure time simulated represents the FASTr production line recipe RCP-1000184, which specifies a temperature of 78 C for 50 minutes.  This simulated step represented the temperatures seen in manufacturing and will not impact the test results. The protocol will not be updated to incorporate this deviation as going through the manufacturing process should be the preferred way to condition the units.

8.2 DEVIATION #2: Battery discharge done at end of session

To account for the missing battery depletion, the average transmitter sleep current from PTL-903600 Appendix B was used to determine the missing capacity to deplete. The missing capacity to deplete was added as test session time at the end of the test. This step adds variability to the results as the Arbin tester provides a constant capacity depletion for all batteries, while each PCBA will have a different current draw to deplete the batteries.  However, the added variability was mitigated by adding 5 days to the protocol execution. The protocol will not be updated to incorporate this deviation as depleting batteries prior to the manufacturing process should be preferred, however, this deviation is deemed equivalent to the intent of the original protocol.

## Create Defective Unit Investigations section

The AI agent extracts information from the Defective Unit Investigation JIRA ticket.  The agent uses the information in the JIRA tickets to provide a summary of all the investigations related to defective units in this report section.

### INSTRUCTIONS:

The agent requests the Jira Ticket Number for each defective unit investigations from the user and creates a subsection for each investigation in the following format:

Subsection title format: Defective Unit Investigation [number] [Investigation Ticket Reference]

where [number] is the investigation number starting from 1, and [Investigation Ticket Reference] is the provided investigation JIRA ticket reference provided in the protocol notes.

Subsection Content: Use the protocol notes to write a Defective Units Investigation summary which includes:

Which specification was not met by the defective unit(s)

The number of defective units related to this specification

The serial number of the defective units.

Summary of the root cause investigation of the failed unit(s) or a statement to refer to the investigation for further information.

List of actions taken to close the investigation

If no defective unit exists, the agent adds the statement: “No defective unit in the execution of this test.” in the Defective Unit Investigations section of the report.

If there are more than 1 defective unit investigation, the agent creates an introduction fir this section that includes the total number of defective units, which specifications were not met and the number of defective units for each specification that was not met.

### Knowledge Base

JIRA Project SHAD

### INPUTS

Jira Ticket Number

### OUTPUTS:

Updated test report Defective Units Investigations section

### EXAMPLES:

9.1 Defective Unit Investigation #1 - SHAD-2

Three Test articles (570281018183, 582216277440, 433673915827) failed to communicate with the display device at 22.66 days to retrieve the database from the transmitter, as noted in Jira Ticket SHAD-2. Manufacturing logs confirm the issue is not related to the PCBA. The test method review found that the database download method is less intensive than the private data download method used by display devices. The units could not be retested due to the destructive nature of the investigation and are considered failures. The protocol should be updated to reflect that communication with the display device should retrieve private data, as this better represents the display device's data request method.

## 4.11 Create Test Method Loss Investigations section

The AI agent extracts information from the Test Method Loss Investigation data sheet.  The agent uses the information in the data sheets to provide a summary of all the investigations related to defective units in this report section.

### 4.11.1 INSTRUCTIONS:

  - If no test method loss occurred,  the agent adds the statement: “No test method loss occurred in the execution of this test” in the Test Method Loss Investigations section of the report.

  - If there are more than 1 test method investigation, the agent creates an introduction using the information from all the test method losses investigations which includes:

    - the total number of test method losses,

    - a statement if replacement were done and

    - if the minimum sample size is still met

  - For each test method loss investigation the agent creates a subsection in the Test Method Loss Investigations section in the following manner:

    - Subsection title format: Test Method Loss Investigation [number]

      - where [number] is the investigation number starting from 1

    - Subsection Content:

      - Description of the event(s) that determined the test article(s) are test method loss(es).

      - The number of units flagged as test method loss for this investigation and the serial numbers of each test articles flagged as test method losses

      - The number of units replaced and their serial numbers.

      - Statement if the minimum sample size was still met for this test method loss investigation

### 4.11.2 Knowledge Base

None

### 4.11.3 INPUTS

Test Method Loss Investigation Data Sheets

### 4.11.4 OUTPUTS

Updated test report Test method Loss Investigations section

### 4.11.5 EXAMPLES:

There was a total of 3 test methods losses of which 2 of them were replaced.  The minimum sample size was met despite these 3 test method losses.

10.1 Test Method Loss Investigation #1

Two Units (454517824545, 393917822929) were punctured during deployment by the operator and were replaced with units SN 949417829494, 757517827575. The minimum sample size was still met after replacements.

10.2 Test Method Loss Investigation #2

Test unit 743513455243 was depleted for 24 hours past the maximum depleted time due to an error in calculating the depletion time. Units were not replaced as there was sufficient samples to meet the minimum sample size.

## Create the Conclusion section

The AI agent takes information from the scope and test results sections and provides a conclusion which summarizes the test results for each acceptance criteria evaluated in the report.

### INSTRUCTIONS:

The agent creates a conclusion that includes the following information in the first paragraph:

A statement that the acceptance criteria were either met or not.

A reference to the requirements unique identifiers evaluated in the report

A reference to the protocol used and its revision.

The agent then creates 1 paragraph for each acceptance criteria evaluated that includes the following information:

Total units passing the specification over the total of units tested (excluding test method losses) in the following format ([# units meeting specification / # units tested excluding test method losses)

If data from the test is analyzed as attribute data, include the confidence achieved for the reliability requested by the acceptance criteria.

If data from the test is analyzed as variable data, include the tolerance interval per the required confidence and reliability from the acceptance criteria.

The parameter measured for the acceptance criteria and the required confidence and reliability needed.

### Knowledge Base:

None

### INPUTS:

Test Report Results section

Test Report Scope section

### OUTPUTS:

Conclusion section completed

### EXAMPLES:

The battery life for the G7 GSS Transmitters (MT-26023-72), with Maxell and Panasonic batteries, met the requirement for GSS-110596, GSS-202364, HRS-149897, and GSS-110672 for both acceptance criteria defined in PT-903900 rev 002.

Specifically, a 95%/90% lower tolerance interval of 2.39 V for Transmitter with Maxell batteries and 2.38 V for Transmitter with Panasonic batteries both met the 2.00 V acceptance criteria at the end of the Sensor Session.  Also, 119 out of 120 devices of transmitters with Maxell batteries (90% / 96.76% conf/rel) and 120 of 120 units 90% / 98.08% conf/rel) with Panasonic batteries were able to successfully communicate with a display device 24 hours after the end of the session and met the 90%/90% conf/rel acceptance criteria.

## Create Report Document and Attachments in Sharepoint with specific filename format

The AI agent having access to the sharepoint location provided by the user, creates a folder and gives it a name related to the RPT being created and saves the Report and its attachments in that location.

If the AI is instructed to change the report content, the AI has the ability to edit or replace the reports and attachments in that location.

The AI will follow a strict rule on the naming convention for the folder and file names created.

### INSTRUCTIONS:

Using the Report Number, the AI agent creates a folder in the Sharepoint location provided and names it with the following convention:

Folder Name: [RPT number]

In the folder created, the AI agent will save the report and name it with the following convention:

[RPT Number] rev[Revision Number] [Title of the Report, truncated at 85 characters]

In the folder created, the AI agent will save the report attachments and name it with the following convention:

[RPT Number] rev[Revision Number] Attachment [Attachment Number] - [Title of the Attachment, truncated at 60 characters]

The AI shall have read and write access to the reports and attachments.

### Knowledge Base to use:

None

### INPUTS:

Test Report Number

Test Report Title

Sharepoint location to save the reports and attachments

### OUTPUTS:

Report Folder

Test Report saved into the report folder

Test Report attachments saved into the report folder

### EXAMPLES:

N/A

