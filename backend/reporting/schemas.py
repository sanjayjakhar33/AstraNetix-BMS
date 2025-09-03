from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

# Report Template Schemas
class ReportTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    report_type: str  # usage, billing, network, compliance
    config: Dict[str, Any]  # fields, filters, formatting
    schedule: Optional[Dict[str, Any]] = None

class ReportTemplateResponse(BaseModel):
    id: str
    isp_id: str
    name: str
    description: Optional[str]
    report_type: str
    config: Dict[str, Any]
    schedule: Optional[Dict[str, Any]]
    is_active: bool
    created_at: datetime

# Report Generation Schemas
class ReportGenerationRequest(BaseModel):
    template_id: str
    file_format: str  # pdf, csv, xlsx
    parameters: Optional[Dict[str, Any]] = {}

class ReportGenerationResponse(BaseModel):
    id: str
    template_id: str
    generated_by: Optional[str]
    file_path: Optional[str]
    file_format: str
    status: str
    parameters: Dict[str, Any]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

# Custom Report Builder Schemas
class ReportField(BaseModel):
    name: str
    label: str
    type: str  # string, number, date, boolean
    source_table: str
    calculation: Optional[str] = None  # sum, avg, count, etc.

class ReportFilter(BaseModel):
    field: str
    operator: str  # equals, contains, greater_than, etc.
    value: Any

class CustomReportRequest(BaseModel):
    name: str
    description: Optional[str] = None
    fields: List[ReportField]
    filters: List[ReportFilter]
    grouping: Optional[List[str]] = []
    sorting: Optional[List[Dict[str, str]]] = []
    date_range: Optional[Dict[str, str]] = None

# Compliance Report Schemas
class ComplianceReportType(BaseModel):
    type: str  # gdpr, pci, iso, sox
    requirements: List[str]
    data_sources: List[str]
    retention_period: int  # days

class ComplianceReportResponse(BaseModel):
    report_type: str
    compliance_score: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    findings: List[Dict[str, Any]]
    recommendations: List[str]
    generated_at: datetime

# BI Integration Schemas
class BIEndpointConfig(BaseModel):
    endpoint_name: str
    description: str
    data_source: str
    refresh_interval: int  # minutes
    authentication: Dict[str, Any]
    parameters: Dict[str, Any]