# Digital Analytics

> ⚠️ **Note:** This project is currently in early development. Features and APIs are subject to change.

A digital analytics platform built with Python, leveraging FastAPI for the backend and powerful data libraries like Pandas, NumPy, and Matplotlib for analysis and visualization.

## 🚀 Features

- **FastAPI Backend**: High-performance API for handling requests.
- **Data Processing**: Utilizes Pandas and NumPy for efficient data manipulation.
- **Visualization**: Integrates Matplotlib for generating insights.
- **Modular Structure**: Organized into routers, schemas, and services for scalability.

## 🛠️ Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) (Recommended for dependency management)

## 📦 Installation & Running

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Digital-Analytics
   ```

2. **Install dependencies**
   Using `uv`:
   ```bash
   uv sync
   ```
   Or using standard `pip`:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: If `requirements.txt` is missing, use `pyproject.toml`)*

3. **Run the application**
   You can start the development server using `uv`:
   ```bash
   uv run uvicorn main:app --reload
   ```
   Or directly with Python if dependencies are installed in your environment:
   ```bash
   python main.py
   ```

   The API will be available at `http://127.0.0.1:8000`.
   Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## 🤝 How to Contribute

We welcome contributions! Since the project is still in development, there are many opportunities to help shape its direction.

### Steps to Contribute

1. **Fork the repository** to your GitHub account.
2. **Clone your fork** locally.
3. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Make your changes** and commit them with clear messages.
5. **Push to your fork**:
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request** (PR) to the main repository.

### Guidelines

- Please ensure your code follows the existing style.
- If adding new dependencies, update `pyproject.toml`.
- Describe your changes clearly in the Pull Request description.

