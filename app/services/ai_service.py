from google import genai
from google.genai import types
import os
import json

class AIService:
    """
    Service to generate AI summaries using Google's new GenAI SDK (v2+).
    Uses 'gemini-2.5-flash' as requested.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        # Initialize client with API key if provided, else it might look for env var
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            # Fallback to env var if available, though logic usually passes it in
            self.client = genai.Client()

    def generate_insight(self, context_data: dict, prompt_type: str = "overview") -> str:
        """
        Generates insights based on the provided context and prompt type.
        prompt_type can be: 'overview', 'stats', 'missing', 'visualization'
        """
        try:
            prompt = self._construct_prompt(context_data, prompt_type)
            
            # Using the requested model
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating AI insight: {str(e)}"

    def _construct_prompt(self, data: dict, prompt_type: str) -> str:
        """Constructs a specific prompt based on the type of analysis requested."""
        
        base_instruction = """
        You are an expert Data Analyst AI. Your goal is to explain data clearly to a user.
        Analyze the provided data JSON and respond in Markdown.
        Structure your response with these sections:
        - **What does this data mean?**: Brief explanation of the metrics or chart.
        - **Key Observations**: What stands out? (Trends, outliers, high/low values).
        - **Actionable Advice**: What should the user do next? (Data cleaning, further analysis, business implication).
        
        Keep it concise, professional, yet easy to understand.
        """

        if prompt_type == "overview":
            columns = data.get('columns', [])
            missing = data.get('missing_values', {})
            description = str(data.get('description', {}))[:1500] 
            content = f"""
            Task: Provide a high-level summary of the entire dataset.
            
            Dataset Context:
            - Columns: {columns}
            - Missing Values Summary: {missing}
            - Statistical Snapshot: {description}
            """
            
        elif prompt_type == "stats":
            content = f"""
            Task: Analyze the descriptive statistics table.
            
            Statistics Data:
            {json.dumps(data, indent=2)}
            
            Focus on distribution, central tendencies (mean/median), and spread.
            """

        elif prompt_type == "missing":
            content = f"""
            Task: Analyze the missing values profile.
            
            Missing Values Data:
            {json.dumps(data, indent=2)}
            
            Evaluate the severity of missing data and suggest imputation or handling strategies.
            """

        elif prompt_type == "visualization":
            # For viz, we might get column stats + chart type info
            col_name = data.get('column', 'Unknown')
            chart_type = data.get('type', 'Chart')
            stats = data.get('stats', {})
            
            content = f"""
            Task: Analyze a {chart_type} for the column '{col_name}'.
            
            Underlying Statistics for this column:
            {json.dumps(stats, indent=2)}
            
            Explain what a {chart_type} of this data shows regarding distribution or relationship.
            """
            
        else:
            content = f"Task: Analyze the following data: {str(data)[:2000]}"

        return f"{base_instruction}\n\n{content}"
