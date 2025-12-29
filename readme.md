# AI-Powered Data Exploration Web App

A self-hosted, full-stack web application designed for interactive data exploration. Upload datasets, generate stats/visualizations automatically, and get AI-powered insights using Google Gemini or OpenAI.

## Features
- **Easy Upload**: Drag-and-drop CSV, Excel, or TSV files.
- **Automated Profiling**: Instantly view `head()`, missing values, descriptive statistics, and correlation matrices.
- **Visualizations**: Auto-generated histograms, boxplots, and heatmaps using Seaborn/Matplotlib.
- **AI Integration**: Enter your API key (Gemini supported by default) to get a natural language summary and insights about your data.
- **Responsive UI**: Clean, modern interface built with HTML5, CSS3, and minimal Vanilla JS.

## Project Structure
```
/
├── app/                # Backend Source Code
│   ├── main.py         # FastAPI Entry Point
│   ├── services/       # Business Logic (Dataset, Profiler, AI)
│   ├── routers/        # API Endpoints
│   └── schemas/        # Pydantic Models
├── static/             # Frontend Assets (CSS, JS)
├── templates/          # HTML Templates (Jinja2)
├── Dockerfile          # Container Config
└── requirements.txt    # Python Dependencies
```

## Getting Started

### Prerequisites
- Python 3.9+
- A Google Gemini API Key (for AI features) [Get one here](https://aistudio.google.com/app/apikey)

### Local Installation
1. **Clone the repository** (if using git) or download the source.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
4. **Access the App**:
   Open browser to `http://127.0.0.1:8000`

### Docker Deployment
1. **Build the Image**:
   ```bash
   docker build -t ai-data-explorer .
   ```
2. **Run the Container**:
   ```bash
   docker run -p 8000:8000 ai-data-explorer
   ```
   
## Usage Guide
1. **Home Page**: Upload your dataset file.
2. **Dashboard**: 
   - Review the "Dataset Info" and "Missing Values".
   - Explore the "Descriptive Statistics" table.
   - Analyze the generated Visualizations.
3. **AI Insights**:
   - Locate the "✨ AI Insights" card at the top.
   - Enter your Gemini API Key.
   - Click "Generate" to receive a comprehensive analysis.

## Tech Stack
- **Backend**: FastAPI, Pandas, Matplotlib, Seaborn
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **AI**: Google Generative AI (Gemini) SDK
