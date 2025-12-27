import os
from google import genai
from google.genai import types

class AISummarizer:
    """
    Class responsible for generating AI summaries using Google GenAI.
    """
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def summarize(self, profile_data: dict) -> str:
        """
        Generates a summary based on the profiling data.
        """
        if not self.client:
            return "Gemini API Key not found. Please set GEMINI_API_KEY environment variable."

        prompt = f"""
        You are a data analyst. Analyze the following dataset profile and provide a concise summary.
        Highlight key insights, missing values, and potential data quality issues.
        
        Profile Data:
        {profile_data}
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"
