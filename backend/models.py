from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import re


# --- File models ---

class FileInfo(BaseModel):
    id: Optional[int] = None
    original_path: str = Field(..., description="Original absolute path of the file")
    current_path: str = Field(..., description="Current absolute path of the file")
    original_filename: str = Field(..., description="Original filename")
    current_filename: str = Field(..., description="Current filename")
    file_hash: Optional[str] = Field(None, description="SHA-256 hash of the file")
    file_type: Optional[str] = Field(None, description="File type/extension")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @validator("current_path", "original_path")
    def must_be_filesystem_safe(cls, v):
        """Validate path doesn't contain traversal sequences."""
        if ".." in v.split(os.sep):
            raise ValueError("Path traversal detected")
        return os.path.normpath(v)


class FileCreate(FileInfo):
    """For creating/importing a file record."""


# --- Analysis models ---

class AnalysisBase(BaseModel):
    category: Optional[str] = Field(None, description="Recommended category")
    subcategory: Optional[str] = Field(None, description="Recommended subcategory")
    suggested_filename: Optional[str] = Field(None, description="Recommended new filename")
    suggested_destination: Optional[str] = Field(None, description="Recommended destination folder")
    summary: Optional[str] = Field(None, description="AI-generated summary")
    importance: Optional[str] = Field(
        None, description="Importance: low|medium|high"
    )
    confidence: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Confidence score 0.0-1.0"
    )
    tags: Optional[List[str]] = Field(
        None, description="List of tags/topics"
    )
    reason: Optional[str] = Field(None, description="Reasoning for the analysis")


class AnalysisCreate(AnalysisBase):
    """For creating an analysis record."""
    file_id: Optional[int] = Field(None, description="Reference to the file being analyzed")


class AnalysisInDB(AnalysisBase):
    id: int
    file_id: int
    created_at: str

    class Config:
        from_attributes = True


# --- Operation models ---

class OperationBase(BaseModel):
    operation_type: str = Field(
        ..., description="Type: move|rename|organize|duplicate|summary"
    )
    old_path: str = Field(..., description="Original path before operation")
    new_path: str = Field(..., description="New path after operation")


class OperationCreate(OperationBase):
    """For creating an operation record."""
    file_id: int = Field(..., description="Reference to the file")


class OperationInDB(OperationBase):
    id: int
    file_id: int
    timestamp: str
    undone: bool = False

    class Config:
        from_attributes = True


# --- Settings models ---

class SettingUpdate(BaseModel):
    key: str = Field(..., description="Setting key")
    value: str = Field(..., description="Setting value")


class SettingsResponse(BaseModel):
    ai_provider: str = "LM Studio"
    base_url: str = "http://localhost:1234/v1"
    model: str = "gemma-2b"
    api_key: Optional[str] = None
    minimum_confidence: float = 0.9
    auto_mode: bool = False
    auto_mode_threshold: float = 0.9
    duplicate_detection: bool = True
    generate_summary: bool = True


# --- Rule models ---

class ConditionBase(BaseModel):
    field: str = Field(..., description="Condition field to check")
    operator: str = Field(
        ..., description="Operator: =|>|<|contains|regex"
    )
    value: Any = Field(..., description="Condition value")


class ActionBase(BaseModel):
    type: str = Field(..., description="Action type: move|rename|category")
    target: Optional[str] = Field(None, description="Action target/path")


class RuleBase(BaseModel):
    name: str = Field(..., description="Rule name")
    conditions: List[ConditionBase] = Field(
        default_factory=list, description="List of conditions"
    )
    actions: List[ActionBase] = Field(
        default_factory=list, description="List of actions"
    )
    enabled: bool = Field(True, description="Whether rule is enabled")


class RuleCreate(RuleBase):
    """For creating a rule."""


class RuleUpdate(BaseModel):
    """For updating a rule."""
    name: Optional[str] = None
    conditions: Optional[List[ConditionBase]] = None
    actions: Optional[List[ActionBase]] = None
    enabled: Optional[bool] = None


class RuleInDB(RuleBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True


# --- Response models ---

class ApiResponse(BaseModel):
    success: bool = True
    message: str = ""
    data: Any = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: Optional[Dict[str, Any]] = None


# File operation result

class FileOperationResult(BaseModel):
    success: bool
    message: str
    file_id: Optional[int] = None
    undone: bool = False


# Duplicate detection result

class DuplicateInfo(BaseModel):
    is_duplicate: bool
    confidence: float
    similar_files: List[str] = Field(default_factory=list)
    description: str = ""


# API error helpers

def error_404(message: str) -> dict:
    return {"success": False, "message": message, "details": None}


def error_422(message: str, details: Optional[Dict] = None) -> dict:
    return {
        "success": False,
        "message": message,
        "details": details or {"field": "validation"},
    }


def error_500(message: str, details: Optional[Dict] = None) -> dict:
    return {
        "success": False,
        "message": message,
        "details": details or {"operation": "unknown"},
    }