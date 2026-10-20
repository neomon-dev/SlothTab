"""AI Prompt templates for SlothTab."""

# Use raw strings (r"""...""") to avoid escape sequence warnings with backslash-quotes
FILE_CLASSIFICATION_PROMPT = r"""You are SlothTab, a local-first file organization assistant.

Analyze the supplied file information and content.

Recommend:
- category: One of College, Work, Personal, Development, Media, Archive, or Other
- subcategory: More specific classification (e.g., Assignments, Notes, Projects, Programming, Cloud Computing)
- suggested_filename: A concise, descriptive filename (filesystem-safe, preserve extension)
- suggested_destination: Where the file should go (relative to the workspace root)
- summary: A brief summary of the file contents (max 2-3 sentences)
- importance: low | medium | high (estimated importance/urgency)
- tags: 3-5 relevant tags/topics
- confidence: A confidence score between 0.0 and 1.0
- reason: Brief explanation for the recommendations

File information:
- Filename: {filename}
- Extension: {extension}
- File size: {file_size} bytes
- MIME type: {mime_type}
- Extracted text: {extracted_text}

Constraints:
- Never invent facts
- If uncertain, lower confidence
- Filename must be filesystem-safe (no / \ : * ? " < > |)
- Destination must be relative and safe
- Return ONLY valid JSON, no surrounding text
- Category should be one: College, Work, Personal, Development, Media, Archive, Other

JSON format:
{
  "category": "College",
  "subcategory": "Notes",
  "suggested_filename": "cloud-computing-notes.txt",
  "suggested_destination": "College/Notes",
  "summary": "Notes about cloud computing concepts.",
  "importance": "medium",
  "confidence": 0.94,
  "tags": ["cloud-computing", "notes"],
  "reason": "The file contains notes about cloud computing topics.",
}"""

FILENAME_ONLY_PROMPT = r"""You are SlothTab. Generate a concise, descriptive filename for this file.

Filename rules:
- filesystem-safe (no / \ : * ? " < > |)
- concise yet descriptive
- preserve the extension
- avoid unnecessary punctuation
- avoid excessive length

Current filename: {current_filename}
File info: {file_info}
Extracted text: {extracted_text}

Return ONLY valid JSON:
{
  "suggested_filename": "descriptive-filename.txt"
}"""

DESTINATION_PROMPT = r"""You are SlothTab. Recommend a destination folder for this file.

Available categories:
College:
  Assignments, Notes, Projects, Exams, Programming, Cloud Computing
Work:
  Documents, Reports, Projects
Personal:
  Documents, Photos, Receipts
Development:
  Code, Documentation, Screenshots
Media:
  Images, Videos, Audio
Archive:
  Miscellaneous
Other:

Current filename: {current_filename}
Category: {category}
Subcategory: {subcategory}
Extracted text: {extracted_text}

Return ONLY valid JSON:
{
  "suggested_destination": "College/Notes"
}"""

SUMMARIZATION_PROMPT = r"""You are SlothTab. Generate a concise summary of this document.

Rules:
- Maximum 3 bullet points
- 2-3 sentences total
- Capture the main purpose or key information
- Do not invent details not present in the text

File content: {extracted_text}

Return ONLY valid JSON:
{
  "summary": "This document explains... Key points: • ... • ..."
}"""

IMPORTANCE_PROMPT = r"""You are SlothTab. Estimate the importance/urgency of this file.

Importance levels:
- low: Personal emails, newsletters, reference material
- medium: Project docs, instructions, non-urgent work
- high: Assignment with deadline, time-sensitive materials

File info:
- Filename: {filename}
- Extracted text: {extracted_text}
- Any dates/deadlines detected: {dates}

Return ONLY valid JSON:
{
  "importance": "medium",
  "confidence": 0.88,
  "reason": "No urgent deadlines detected, but project-relevant content present.",
  "evidence": "Specific text evidence if deadline found, otherwise N/A"
}"""

IMAGE_ANALYSIS_PROMPT = r"""You are SlothTab. Analyze this image file.

If the model supports vision, describe what you see. If not, use filename and metadata.

File: {filename}
File size: {file_size} bytes
MIME type: {mime_type}
Extracted metadata: {metadata}

Describe:
- What the image shows
- If it's a screenshot, what application/subject
- If it's a photo, what subject
- Any text visible in the image

Return ONLY valid JSON:
{
  "description": "A screenshot of a cloud console showing VM creation steps.",
  "detected_text": "gcloud compute instances create...",
  "image_type": "screenshot",
  "confidence": 0.91
}"""

DUPLICATE_REASONING_PROMPT = r"""You are SlothTab. Determine if this file is a duplicate or similar to other files.

Current file:
- Filename: {current_filename}
- Size: {file_size} bytes
- Hash: {file_hash}
- Extracted text: {extracted_text}

Compare with these potential duplicates:
- Existing file 1: {file1_info}
- Existing file 2: {file2_info}

Return ONLY valid JSON:
{
  "is_duplicate": false,
  "similarity_type": "exact|possible|different",
  "confidence": 0.95,
  "reason": "Files have identical hashes and sizes.",
  "notes": "Optional notes about differences"
}"""