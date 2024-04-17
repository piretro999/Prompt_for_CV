# CV Data Extractor

## Overview
The CV Data Extractor comprises two key components: the `cvparser.py` script and its accompanying documentation. An alternative to cvparser.py you can find the prompt that has to be put directly on http://chat.openai.com interface. This tool is specifically crafted to extract detailed information from a Curriculum Vitae (CV) formatted and enclosed within `<<<` and `>>>` markers, organizing it into both XML and JSON formats for versatile applications.

## Features
- **Data Extraction:** Efficiently extracts essential details such as personal information, contacts, and professional background from the CV.
- **Data Organization:** Systematically groups and organizes data to facilitate accessibility and integration.
- **Multi-format Output:** Outputs data in both XML and JSON formats to cater to various application needs.

## Input Format
If you use the openai interface, just insert the CV text between the `<<<` and `>>>` symbols in the input field. The CV should include structured sections like Personal Details, Contact Information, and Professional Background.
If you use the python script remember to insert your API key and to modify the name of the target CV file in txt format.

## Output Description
- **XML Format:** Hierarchically structured with nested elements for entries like skills and experiences.
- **JSON Format:** Structured as key-value pairs, ideal for integration with web applications and databases.

## Usage Instructions
1. Place the CV text within the `<<<` and `>>>` markers.
2. OR Execute the `cvparser.py` script.
3. Review the outputs in both XML and JSON formats.

## Important Notes
- No data should be omitted during extraction. If information is missing, indicate 'NOT PROVIDED' for those fields, except name and surname which should be inferred from the email if possible.
- Use the `<doubt>` node in the XML to report ambiguities or missing information.

## Sample Outputs
- Refer to the `examples` folder for XML and JSON format samples, showing expected output.
