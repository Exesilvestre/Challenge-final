from pydantic import BaseModel
from typing import List

class MessageCreate(BaseModel):
    content: str
    role: str  # "user" or "assistant"

class ConversationCreate(BaseModel):
    name: str

class MessagePrompt(BaseModel):
    prompt: str

class ConversationUpdate(BaseModel):
    new_name: str

class MessageResponse(BaseModel):
    id: int
    content: str
    role: str

    class Config:
        orm_mode = True

class ConversationResponse(BaseModel):
    id: int
    name: str
    messages: List[MessageResponse]

    class Config:
        orm_mode = True