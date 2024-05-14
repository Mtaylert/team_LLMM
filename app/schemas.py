from pydantic import BaseModel

class LLMInput(BaseModel):
    input_question: str
    chunking_type: str


