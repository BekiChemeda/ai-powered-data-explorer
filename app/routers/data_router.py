from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.services.dataset import Dataset
from app.services.profiler import Profiler
from app.services.visualizer import Visualizer
from app.services.ai_summarizer import AISummarizer
from app.services.file_manager import FileManager
from app.schemas.schemas import ProfileResponse, SummaryResponse, VisualizationResponse, InfoResponse
import os

router = APIRouter()
file_manager = FileManager()
ai_summarizer = AISummarizer()

def get_dataset(file_id: str) -> Dataset:
    file_path = os.path.join(file_manager.UPLOAD_DIR, file_id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    dataset = Dataset(file_path)
    try:
        dataset.load()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return dataset

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = file_manager.save_file(file)
        file_id = os.path.basename(file_path)
        return {"message": "File uploaded successfully", "file_id": file_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile/{file_id}", response_model=ProfileResponse)
def get_profile(file_id: str):
    dataset = get_dataset(file_id)
    profiler = Profiler(dataset)
    return profiler.get_profile()


@router.get("/info/{file_id}", response_model=InfoResponse)
def get_info(file_id: str, head_rows: int = 5):
    try:
        dataset: Dataset = get_dataset(file_id)
        return dataset.summary(head_rows=head_rows)

    except KeyError:
        raise HTTPException(status_code=404, detail="Dataset not found")

    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/visualize/{file_id}", response_model=VisualizationResponse)
def visualize(file_id: str, chart_type: str, column: str = None):
    dataset = get_dataset(file_id)
    visualizer = Visualizer(dataset)
    
    try:
        if chart_type == "histogram":
            if not column:
                raise HTTPException(status_code=400, detail="Column name required for histogram")
            image = visualizer.generate_histogram(column)
        elif chart_type == "bar":
            if not column:
                raise HTTPException(status_code=400, detail="Column name required for bar chart")
            image = visualizer.generate_bar_chart(column)
        elif chart_type == "correlation":
            image = visualizer.generate_correlation_heatmap()
        else:
            raise HTTPException(status_code=400, detail="Invalid chart type")
        
        return {"image_base64": image}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/summarize/{file_id}", response_model=SummaryResponse)
def summarize(file_id: str):
    dataset = get_dataset(file_id)
    profiler = Profiler(dataset)
    profile_data = profiler.get_profile()
    
    summary = ai_summarizer.summarize(profile_data)
    return {"summary": summary}
