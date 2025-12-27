from fpdf import FPDF

# Roadmap content
roadmap_text = """
AI-Powered Data Exploration Web App – 5-Day Roadmap

Overview
Duration: 5 Days
Daily Commitment: 5 Hours / Day
Target Audience: Junior Backend / ML Engineer
Goal: Build a working, interview-ready AI-powered data exploration web application with backend-first architecture.

Day 1 – Foundation & Data Ingestion (5 Hours)
1. Project Setup & Environment (45 min)
- Create project folder structure
- Initialize virtual environment
- Install dependencies: FastAPI, Uvicorn, Pandas, NumPy, Pydantic, python-multipart
Outcome: Clean project skeleton ready for development

2. Backend Structure & App Initialization (45 min)
- Create main.py
- Configure FastAPI app
- Set up routers folder
Outcome: App runs locally with /docs

3. File Upload Endpoint (1 hr 30 min)
- Implement /upload endpoint
- Support CSV, TSV, Excel
- Basic file-type validation
Outcome: Users can upload files successfully

4. Pandas Data Loading Logic (1 hr)
- Load uploaded files into DataFrame
- Handle separators and encoding
Outcome: DataFrame creation works reliably

5. Quick Sanity Tests (1 hr)
- Upload sample datasets
- Fix crashes and edge cases
Day 1 Deliverable: File upload → DataFrame conversion

Day 2 – Validation, Profiling & Column Inference (5 Hours)
1. Input Validation with Pydantic (1 hr)
- Validate head(n) and user parameters
- Enforce limits
Outcome: Safe, predictable inputs

2. Data Profiling Service (1 hr 30 min)
- Implement missing value counts
- Compute basic statistics
- Store profiling results
Outcome: Dataset summary available programmatically

3. Column Type Inference (1 hr)
- Numeric vs categorical vs datetime
- Map types to analysis strategies
Outcome: System understands schema automatically

4. Profiling Endpoint (1 hr 30 min)
- Create /profile endpoint
- Return JSON profiling output
Day 2 Deliverable: Automatic dataset profiling

Day 3 – Visualization Engine & Frontend (5 Hours)
1. Visualization Utilities (1 hr 30 min)
- Histograms for numeric data
- Bar charts for categorical data
Outcome: Server-side plots generated

2. Plot Serving Endpoint (1 hr)
- Return images or base64
- Connect plots to frontend
Outcome: Visuals visible in browser

3. Frontend HTML Upload Page (1 hr)
- Upload form
- Basic layout
Outcome: Users interact through browser

4. Frontend Integration (1 hr 30 min)
- JavaScript fetch calls
- Render tables and plots
Day 3 Deliverable: Working web interface

Day 4 – AI Summarization & Explainability (5 Hours)
1. Prompt Design & Grounding (1 hr)
- Define AI input format
- Inject statistics only
Outcome: Safe AI prompts

2. AI Integration (1 hr 30 min)
- Call LLM API
- Handle errors and timeouts
Outcome: AI summaries generated

3. Explainable AI Logic (1 hr)
- Ensure AI outputs reference computed facts
Outcome: Trustworthy AI behavior

4. AI Summary Endpoint (1 hr 30 min)
- /summarize endpoint
- Frontend display
Day 4 Deliverable: AI-powered data explanation

Day 5 – Architecture Polish & Deployment (5 Hours)
1. Code Refactoring & Separation (1 hr 30 min)
- Move logic to services
- Clean imports
Outcome: Production-style architecture

2. Error Handling & Edge Cases (1 hr)
- Invalid files
- Empty datasets
Outcome: Robust system

3. Dockerization (1 hr)
- Write Dockerfile
- Local container run
Outcome: One-command deployment

4. README & Documentation (1 hr 30 min)
- Setup instructions
- Architecture explanation
Day 5 Deliverable: Interview-ready project

Final Result
By the end of Day 5, you will have:
- A backend-first web application
- AI-assisted, explainable data insights
- Local deployability
- Strong Kagool-aligned portfolio project
"""

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

for line in roadmap_text.split("\n"):
    pdf.multi_cell(0, 7, line)

pdf_path = "/mnt/data/AI_Data_Exploration_Roadmap.pdf"
pdf.output(pdf_path)
pdf_path
