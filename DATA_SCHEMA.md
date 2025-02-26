# Manifest Generator Data Schema

The Manifest Generator creates JSON files with a specific structure containing participant and study metadata. This document outlines the schema and expected values for each field.

## JSON Schema

```json
{
  "date": "YYYY-MM-DD",
  "current_time": "HH:MM",
  "participant_id": "string",
  "participant_initials": "string",
  "assigned_subject_knowledge": "string",
  "methods_of_analysis": "integer (1-4)",
  "recruitment_form_completed": "boolean",
  "participant_gender": "string",
  "subject_knowledge_topics": "array of 2 integers (1-5)",
  "behavioral_profiles": "array of 2 integers (1-5)",
  "screen_resolution": "string (e.g., 1920x1080)",
  "screen_distance": "string (e.g., distance in cm)",
  "sampling_rate": "string (e.g., rate in Hz)",
  "additional_notes": "string",
  "audio_recording": "string (one/two/none)",
  "generated_at": "ISO format datetime string",
  "generator_version": "string (semantic versioning)"
}
```

## Field Descriptions

| Field Name | Type | Description | Example Value |
|------------|------|-------------|---------------|
| date | String | Collection date in YYYY-MM-DD format | "2023-06-15" |
| current_time | String | Collection time in HH:MM format | "14:30" |
| participant_id | String | Unique identifier for the participant | "P123456" |
| participant_initials | String | Participant's initials | "JD" |
| assigned_subject_knowledge | String | Subject knowledge area assigned to participant | "Machine Learning" |
| methods_of_analysis | Integer | Number of analysis methods to be used (1-4) | 2 |
| recruitment_form_completed | Boolean | Whether the recruitment form was completed | true |
| participant_gender | String | Participant's gender | "Female" |
| subject_knowledge_topics | Array | Two distinct topic indices (1-5) | [2, 4] |
| behavioral_profiles | Array | Two distinct behavioral profile indices (1-5) | [1, 3] |
| screen_resolution | String | Resolution of display used for eye tracking | "1920x1080" |
| screen_distance | String | Distance from participant to screen | "65 cm" |
| sampling_rate | String | Eye tracker sampling rate | "250 Hz" |
| additional_notes | String | Any additional observations or notes | "Participant wore glasses" |
| audio_recording | String | Audio recording configuration | "two" |
| generated_at | String | ISO format timestamp of when file was generated | "2023-06-15T14:32:45.123456" |
| generator_version | String | Version of the manifest generator used | "1.1.0" |

## Data Validation Rules

1. **Date and Time**: 
   - Date must follow YYYY-MM-DD format
   - Time must follow HH:MM format (24-hour)

2. **Numeric Fields**:
   - methods_of_analysis: Integer between 1 and 4
   - subject_knowledge_topics: Array containing two unique integers between 1 and 5
   - behavioral_profiles: Array containing two unique integers between 1 and 5

3. **Audio Recording**:
   - Must be one of: "one", "two", or "none"

## Example JSON Output

```json
{
  "date": "2023-06-15",
  "current_time": "14:30",
  "participant_id": "P123456",
  "participant_initials": "JD",
  "assigned_subject_knowledge": "Machine Learning",
  "methods_of_analysis": 2,
  "recruitment_form_completed": true,
  "participant_gender": "Female",
  "subject_knowledge_topics": [2, 4],
  "behavioral_profiles": [1, 3],
  "screen_resolution": "1920x1080",
  "screen_distance": "65 cm",
  "sampling_rate": "250 Hz",
  "additional_notes": "Participant wore glasses",
  "audio_recording": "two",
  "generated_at": "2023-06-15T14:32:45.123456",
  "generator_version": "1.1.0"
}
```

## Notes for Developers

- The schema may evolve in future versions
- Any changes to the schema should be reflected in the version number
- All string fields have no explicit length limits
- Fields containing numbers as strings (e.g., "250 Hz") allow for units to be included 