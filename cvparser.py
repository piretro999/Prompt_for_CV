# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 22:00:36 2024

@author: Paolo Forte
"""

import requests
from lxml import etree
import json

def read_cv(filepath):
    """Read the entire CV content from a file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def extract_information_with_chatgpt(cv_text, api_key):
    """Use ChatGPT to semantically extract structured information from the CV text."""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    prompt = f"Please read the text included into the <<< and >>> symbols containing the CV. Extract the following information: 1. Name 2. Surname 3. Profile Title 4. Date of Birth 5. Profile description 6. Country of Residence 7. Profile description 8. Residence Address 9. Phone contact 1 10. Phone contact 2 11. Email contact 12. Linkedin profile 13. Training and Education 14. Year of training 15. Skills 16. Soft skills 17, Certifications 18. Known languages 19. Level of known languages 20. Key achievements and Awards 21. Job experiences including:    - Start date    - End date    - Company    - Role    - Description 22. Extra or volunteer experiences including:    - Start date    - End date    - Company    - Role    - Description Remove any bullet points or special characters preceding each value. Group the extracted information as follows: - PersonName - Surname - profileTitle - Date of Birth - Profile description - Country of Residence - City of Residence - Residence Address - Phone contact 1 - Phone contact 2 - Email contact - Linkedin profile - Known languages(multiple values) - Level of known languages(multiple values) - Training and Education (multiple values) - Training Year (multiple values) - Skills and areas of expertise(multiple values) - Soft skills (multiple values) - Certifications (multiple values) - Key Achievements and Awards (multiple values) - Job Experiences (multiple values with start date, end date, company, role, and description) After extracting the information, organize it into an array with the following structure: name surname profileTitle dateOfBirth profileDescription countryOfResidence cityOfRedsidence residenceAddress phoneContact emailContact linkedInProfile trainingAndEducation_1 trainingAndEducation_...n trainingYear_1 trainingYear_..n knownLanguage_1 levelOfKnownLanguage_1 knownLanguage_...n levelOfKnownLanguage_...n skillAndExpertise_1 skillAndExpertise_...n softSkills_1 softSkills_...n certifications_1 certifications_..n keyAchievementsAndAwards_1 keyAchievementsAndAwards_...n experienceStartDate_1 experienceEndDate_1 experienceCompany_1 experienceRole_1 experienceDescription_1 experienceStartDate_...n experienceEndDate_...n experienceCompany_...n experienceRole_...n experienceDescription_...n Use '...n' as a placeholder indicating multiple occurrences in the array. Finally, output the extracted information in json format according to the structure provided  IT IS VERY IMPORTANT THAT YOU DO NOT OMIT ANY SINGLE DATA THAT IS PRESENT, IN PARTICULAR EVERY language, experience, skill, training and all the relating sub-data MUST be present into the json file It is also important that you do not presume or invent any data. any doubt can be reported into the a node called doubt, and if a date or a data is not provided, just insert NOT PROVIDED <<<{cv_text}>>>"
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0,
        'max_tokens': 4000,
        'top_p': 0.00001,
        'frequency_penalty':0,
        'presence_penalty':0
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    response_data = response.json()
    if 'choices' in response_data and response_data['choices']:
        extracted_text = response_data['choices'][0].get('message', {}).get('content', '')
        return parse_extracted_text(extracted_text)
    else:
        print("Failed to get a valid response:", response_data)
        return {}

def parse_extracted_text(text):
    """Parse the extracted text into a structured dictionary."""
    # Remove specified characters from the text
    text = text.replace('"', '').replace('\\"', '').replace('[', '').replace('],', '').replace('""', '').replace(',""', '')
    data = {}
    lines = text.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip().split(',') if ',' in value else [value.strip()]
    return data

def save_to_json(data):
    """Save extracted data to a JSON file matching the XML structure."""
    with open('output.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    api_key = 'INPUT YOUR API KEY HERE'
    filepath = 'path_to_your_cv_file.txt'
    max_attempts = 5
    attempts = 0
    all_data = {}

    while attempts < max_attempts:
        cv_content = read_cv(filepath)
        new_data = extract_information_with_chatgpt(cv_content, api_key)
        for key, value in new_data.items():
            if key in all_data:
                if isinstance(all_data[key], list):
                    all_data[key] = list(set(all_data[key] + value))
                else:
                    all_data[key] = [all_data[key]] + value
            else:
                all_data[key] = value  # Initially set the value as a list
        if all(all_data.get(key) for key in new_data.keys()):
            break
        attempts += 1

    print("Extracted Information:", all_data)
    save_to_json(all_data)
