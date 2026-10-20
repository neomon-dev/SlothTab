# 🦥 SlothTab

> **Let your local AI do the boring stuff.**

## Why Exist

SlothTab is a **local-first AI productivity agent** for people who keep saying:

> "I'll organize this later."

The application analyzes your files using open-weight AI models running locally and automatically organizes, renames, and summarizes them — without ever sending your data to the cloud.

## Features

### Core Capabilities

- **Intelligent File Analysis**: Uses local open-weight models to classify files, generate descriptive filenames, and recommend destinations
- **Smart Categorization**: Automatic classification into College, Work, Personal, Development, Media, Archive categories
- **Structured AI Output**: All AI recommendations validated through Pydantic models before any file operations
- **Confidence Scores**: Every recommendation includes a confidence score (0.0-1.0) for user review
- **Importance Detection**: Automatic estimation of file importance (low/medium/high) with evidence
- **Duplicate Detection**: SHA-256 hash-based detection of exact and possible duplicates
- **File Summarization**: Concise summaries of supported documents (PDF, DOCX, TXT, MD)
- **Image Understanding**: Local vision analysis of screenshots and photos (metadata + optional vision models)

### File Operations

- **Safe Move/Rename**: All file operations go through application safety checks, never through AI commands
- **User Approval Workflow**: AI suggests, user approves before any changes
- **Auto Mode**: High-confidence actions (>90%) can be automated with safeguards
- **Undo Support**: Every operation is recorded and reversible through the Activity page
- **Rules Engine**: User-defined automation rules that work alongside AI classification

### User Interface

- **Dashboard**: Overview of processed files, sloth score, and recent activity
- **Inbox**: Folder selection, drag-and-drop, batch analysis
- **Activity Timeline**: Beautiful visual history with filters (All, Organized, Renamed, Summarized, Needs Review)
- **Rules Management**: Create, edit, and delete automation rules
- **Settings**: AI provider configuration (LM Studio, Ollama, Custom OpenAI-compatible)
- **Demo Mode**: Sample messy folder with real pipeline processing

### Supported File Types (Minimum)

| Extension | Type |
|-----------|------|
| .pdf | PDF documents |
| .docx | Microsoft Word documents |
| .txt | Plain text |
| .md | Markdown |
| .png | Images |
| .jpg, .jpeg | Images |
| .webp | Images |

### Privacy & Security

- **🔒 LOCAL-FIRST**: All files stay on your machine. No cloud AI required.
- **No Cloud APIs**: Works with LM Studio, Ollama, or any OpenAI-compatible local model
- **No Telemetry**: No analytics, no phone home, no data collection
- **Path Security**: All destinations validated to stay within configured workspace
- **No Automatic Deletion**: Files are never deleted without explicit approval
- **No Overwrites**: Destination conflicts are prevented and reported
- **Input Validation**: File contents treated as untrusted input

### Model Support

SlothTab supports any OpenAI-compatible local model:

- **LM Studio**: Default `http://localhost:1234/v1`
- **Ollama**: Default `http://localhost:11434/v1`
- **Generic OpenAI-compatible**: Any endpoint supporting `/chat/completions`

Supported model families include: Gemma, Qwen, DeepSeek, Llama, Mistral, and other compatible open-weight models.

### Sloth Score

A fun productivity metric calculating approximate effort saved:

```
files organized + files renamed + summaries generated + duplicates identified
----------------------------------------------------------- ≈ Sloth Score (%)
                              100%
```

Labelled as an approximate/productivity metric, not scientifically accurate.

## Architecture

```text
                  USER LAPTOP
                       │
                       ▼
                ┌─────────────┐
                │  SlothTab   │
                └──────┬──────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        Local Files         Local AI Server
                                 │
                       ┌─────────┴─────────┐
                       │                   │
                   LM Studio            Ollama
                       │                   │
                       └─────────┬─────────┘
                                 ▼
                          Open-weight LLM
```

## Installation

### 1. Prerequisites

- Python 3.12+
- Node.js 18+ (for frontend, optional - static HTML can be served directly)
- LM Studio or Ollama for local AI models

### 2. Backend Installation

```bash
# Clone the repository
git clone https://github.com/<your-github-user>/SlothTab.git
cd SlothTab

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend
python -m slothtab.backend.app
```

The backend runs on `http://127.0.0.1:8000`.

### 3. Frontend Installation

```bash
# Install frontend dependencies
cd frontend
npm install

# Start the frontend dev server
npm run dev
```

The frontend runs on `http://localhost:5173`.

### Docker deployment

Docker provides the production-style setup: it builds the React frontend, serves it
from FastAPI, and persists the SQLite database in a named volume.

```bash
docker compose up --build
```

Open `http://localhost:8000`. To let the container organize a host folder, set
`SLOTHTAB_WORKSPACE` before starting Compose:

```powershell
$env:SLOTHTAB_WORKSPACE = "C:\Users\you\Downloads"
docker compose up --build
```

The mounted folder is available to the container at `/workspace`. Set the SlothTab
workspace base to `/workspace` in the app settings. Local AI providers such as
LM Studio or Ollama must be reachable from the container; use a host address
appropriate for your Docker runtime rather than `localhost`.

### 4. LM Studio Setup

1. Download and install [LM Studio](https://lmstudio.ai/)
2. Open LM Studio and browse models
3. Download an appropriate open-weight model (e.g., gemma-2b, llama-3b)
4. Click "Start Server" to enable the local HTTP API
5. Default endpoint: `http://localhost:1234/v1`

### 5. Ollama Setup

1. Download and install [Ollama](https://ollama.com/)
2. Pull a model: `ollama pull llama3:8b`
3. Start the server (it auto-starts as a service)
4. Default endpoint: `http://localhost:11434/v1`

### 6. First Run

1. Open SlothTab in your browser
2. Go to Settings → AI Provider
3. Select your provider (LM Studio / Ollama / Custom)
4. Enter the base URL (auto-filled based on selection)
5. Click "Test Connection"
6. If connected, you're ready to organize files!

## Usage

### Basic File Organization

1. Open SlothTab
2. Go to the **Inbox** page
3. Click "Choose Folder" or enter a folder path
4. SlothTab will analyze all supported files
5. Review the AI suggestions:
   - Confidence scores show how sure the AI is
   - Each suggestion includes a reason
6. Click "Apply Suggestions" to organize automatically
   - Or review individually and click Apply on each
7. Check the **Activity** page to see what was done
8. Use "Undo" if you need to reverse any operation

### Auto Mode

1. Enable Auto Mode in Settings
2. Set minimum confidence threshold (default: 90%)
3. Configure safeguards: "Never delete files", "Never overwrite files", "Keep activity log"
4. High-confidence actions will be applied automatically
5. Low-confidence suggestions still require user approval

### Creating Rules

1. Go to the **Rules** page
2. Click "Add Rule"
3. Set conditions (e.g., "Category = College AND Confidence > 90%")
4. Set actions (e.g., "Move to: College/")
5. Rules work alongside AI classification for automated organization

## Development

### Project Structure

```
slothtab/
├── backend/          # FastAPI application
│   ├── app.py        # Main FastAPI app
│   ├── db.py         # SQLite database
│   ├── models.py     # Pydantic models
│   ├── ai_provider.py  # AI provider abstraction
│   ├── file_processing.py  # PDF, DOCX, TXT, MD, image processing
│   ├── prompts.py    # AI prompt templates
│   └── routes.py     # FastAPI endpoints
├── frontend/         # React + TypeScript + Vite
│   ├── package.json  # Dependencies
│   ├── vite.config.ts  # Vite config
│   ├── tailwind.config.ts  # Tailwind config
│   ├── src/          # Source files
│   │   ├── main.tsx      # Entry point
│   │   ├── App.tsx       # Main component with navigation
│   │   ├── pages/        # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Inbox.tsx
│   │   │   ├── Activity.tsx
│   │   │   ├── Rules.tsx
│   │   │   ├── Settings.tsx
│   │   │   └── DemoMode.tsx
│   │   ├── components/   # UI components
│   │   │   ├── ui/       # Reusable UI components
│   │   │   └── lib/      # Utilities
│   │   └── index.html    # HTML template
│   └── public/           # Static assets
├── data/               # SQLite database storage
├── requirements.txt      # Python dependencies
└── README.md           # This documentation
```

### Adding New File Types

1. Add a new processor function in `slothtab/backend/file_processing.py`
2. Add the extension mapping in `get_supported_extensions()`
3. Add the extension to `get_processor_for_file()`
4. The AI analysis will work automatically with the extracted text

### Adding New AI Providers

1. Create a new class inheriting from `AIProvider`
2. Implement `chat_complete()`, `get_available_models()`, and `test_connection()`
3. Add a case in `create_provider()` factory function
4. No changes needed to the rest of the application

## Open Innovation Section

### Why Open AI Matters

**Privacy**
Documents remain on the user's machine. No sensitive data leaves the local system.

**Model Freedom**
The user can choose which open-weight model powers SlothTab. Switch from Gemma to Qwen to Llama without changing application code.

**No Per-Request Cloud Cost**
After obtaining the model, repeated usage doesn't require paying a cloud API for every file. Local inference is free after the initial download.

**Offline Capability**
SlothTab can continue working without internet access. Once the model is loaded, file organization works completely offline.

**Customization**
Users can change:
- Models (Gemma, Qwen, DeepSeek, Llama, Mistral, etc.)
- Prompts (modify the analysis prompts to match their preferences)
- Categories (add or modify default categories)
- Confidence thresholds (adjust the risk tolerance)
- Automation rules (create personal automation workflows)

**Transparency**
The entire AI → recommendation → validation → file-operation pipeline can be inspected by the user. Every AI response is validated through Pydantic models before any file operations execute. The confidence system shows exactly how sure the AI is about each recommendation.

## Demo Script

```text
Start withDownloads/

IMG_8273.png
IMG_8274.png
assignment_final_FINAL2.pdf
cloudnotes.txt
receipt_2938.jpg
document123.pdf
screenshot.png

Open SlothTab.
Select the folder.
Click: "Let the sloth handle it 🦥"

Show AI processing.

Then display:

        🦥 DONE

7 files handled

4 organized
2 renamed
1 duplicate detected

0 files uploaded
0 files deleted

Estimated time saved:
~15 minutes

Show the organized folder.
```

## License

MIT License - feel free to use and modify for your own projects.