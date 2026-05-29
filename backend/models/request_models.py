from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    startup_name: str
    startup_idea: str
