![Status: In Progress](https://img.shields.io/badge/status-in%20progress-yellow)

# AI-Powered Data Exploration Web App

🚧 **Project Status: Actively Under Development**

This project is currently being built and refactored incrementally. Features, architecture, and documentation may evolve as development progresses.

---

## Overview

This is an **AI-powered data exploration and visualization web application** that helps users quickly understand structured datasets.

Users can upload datasets (CSV, TSV, Excel, and SQL sources) through a web interface and instantly receive:

* Dataset previews (`head(n)`)
* Structural information (`info()`)
* Descriptive statistics (`describe()`)
* Automated visualizations
* AI-generated summaries explaining data quality, types, and issues

The goal is to reduce the time it takes to move from *raw data* to *understanding*.

---

## Key Features

* 📂 Upload CSV, TSV, and Excel files
* 🔍 Automatic data profiling (missing values, data types, stats)
* 📊 Dynamic visualizations based on column types
* 🤖 AI-powered dataset summarization (grounded in real statistics)
* 🧱 Clean OOP-based backend architecture
* 🌐 Web-based interface (not API-only)
* 🐳 Local-first deployment (Docker-ready)

---

## Tech Stack

**Backend**

* Python
* FastAPI
* Pandas, NumPy
* Uvicorn

**Frontend**

* HTML, CSS
* Minimal JavaScript

**Tooling**

* uv (dependency management)
* Git & GitHub

---

## Installation (Local Development)

```bash
# Clone the repository
git clone https://github.com/your-username/ai-powered-data-explorer.git
cd ai-powered-data-explorer

# Install dependencies
uv sync

# Run the app
uv run main.py
```

Then open:

```
http://127.0.0.1:8000
```

For Documwentation, visit:

```
http://127.0.0.1:8000/docs
```
---

## Why This Project Exists

Exploratory Data Analysis (EDA) is often repetitive and time-consuming. This project automates the most common EDA steps while keeping results explainable and grounded in real statistics.

It is designed as a **learning-focused but production-minded** system, emphasizing:

* clean architecture
* reproducibility
* explainability

---

## Contributing

Contributions are welcome — especially while the project is evolving.

### How to contribute

1. Fork the repository
2. Create a new branch

   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes with clear commits
4. Open a Pull Request describing **what** and **why**

### Guidelines

* Follow existing code structure
* Write clear commit messages
* Keep changes focused and incremental

---

## Roadmap (High-Level)

* [ ] User authentication & saved datasets
* [ ] Advanced visualizations
* [ ] Dataset comparison
* [ ] Improved AI insights
* [ ] Cloud deployment

---

## License

This project is open source and available under the MIT License.

---

**Author:** Beknan Chemeda
