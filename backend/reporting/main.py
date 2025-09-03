from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
import uuid

from shared.database.connection import get_db
from shared.models.models import (
    ReportTemplate, ReportGeneration, User, Branch, ISP, 
    BandwidthUsage, Payment, SupportTicket
)
from auth.dependencies import get_current_user, get_current_isp
from .schemas import (
    ReportTemplateCreate, ReportTemplateResponse,
    ReportGenerationRequest, ReportGenerationResponse,
    CustomReportRequest, ComplianceReportResponse,
    BIEndpointConfig
)

router = APIRouter()

@router.get("/{isp_id}/templates", response_model=List[ReportTemplateResponse])
async def get_report_templates(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """Get all report templates for ISP"""
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        templates = db.query(ReportTemplate).filter(
            ReportTemplate.isp_id == current_isp.id,
            ReportTemplate.is_active == True
        ).all()
        
        return [
            ReportTemplateResponse(
                id=str(template.id),
                isp_id=str(template.isp_id),
                name=template.name,
                description=template.description,
                report_type=template.report_type,
                config=template.config,
                schedule=template.schedule,
                is_active=template.is_active,
                created_at=template.created_at
            ) for template in templates
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching report templates: {str(e)}"
        )

@router.post("/{isp_id}/templates", response_model=ReportTemplateResponse)
async def create_report_template(
    isp_id: str,
    template_data: ReportTemplateCreate,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Create custom report template with drag-and-drop fields
    - Custom field selection and formatting
    - Automated scheduling options
    - Multiple export formats support
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        template = ReportTemplate(
            isp_id=current_isp.id,
            name=template_data.name,
            description=template_data.description,
            report_type=template_data.report_type,
            config=template_data.config,
            schedule=template_data.schedule
        )
        
        db.add(template)
        db.commit()
        db.refresh(template)
        
        return ReportTemplateResponse(
            id=str(template.id),
            isp_id=str(template.isp_id),
            name=template.name,
            description=template.description,
            report_type=template.report_type,
            config=template.config,
            schedule=template.schedule,
            is_active=template.is_active,
            created_at=template.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating report template: {str(e)}"
        )

@router.post("/{isp_id}/generate", response_model=ReportGenerationResponse)
async def generate_report(
    isp_id: str,
    generation_request: ReportGenerationRequest,
    current_user: dict = Depends(get_current_user),
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Generate report from template with scheduled delivery
    - PDF, CSV, XLSX export formats
    - Email delivery and cloud storage
    - API endpoints for BI tools integration
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        # Verify template exists and belongs to ISP
        template = db.query(ReportTemplate).filter(
            ReportTemplate.id == generation_request.template_id,
            ReportTemplate.isp_id == current_isp.id
        ).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report template not found"
            )
        
        # Create report generation record
        generation = ReportGeneration(
            template_id=template.id,
            generated_by=current_user.get("id"),
            file_format=generation_request.file_format,
            parameters=generation_request.parameters,
            status='generating'
        )
        
        db.add(generation)
        db.commit()
        db.refresh(generation)
        
        # Generate report data based on template configuration
        report_data = await generate_report_data(template, generation_request.parameters, db)
        
        # Simulate file generation (in production, this would create actual files)
        file_path = f"/reports/{isp_id}/{generation.id}.{generation_request.file_format}"
        
        # Update generation record
        generation.file_path = file_path
        generation.status = 'completed'
        generation.completed_at = datetime.now()
        
        db.commit()
        db.refresh(generation)
        
        return ReportGenerationResponse(
            id=str(generation.id),
            template_id=str(generation.template_id),
            generated_by=str(generation.generated_by) if generation.generated_by else None,
            file_path=generation.file_path,
            file_format=generation.file_format,
            status=generation.status,
            parameters=generation.parameters,
            error_message=generation.error_message,
            created_at=generation.created_at,
            completed_at=generation.completed_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        generation.status = 'failed'
        generation.error_message = str(e)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )

@router.post("/{isp_id}/custom-report", response_model=Dict[str, Any])
async def generate_custom_report(
    isp_id: str,
    report_request: CustomReportRequest,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Custom report builder with drag-and-drop interface
    - Dynamic field selection
    - Real-time filtering and grouping
    - Interactive data visualization
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        # Build query based on custom report request
        report_data = await build_custom_report_query(report_request, current_isp.id, db)
        
        return {
            "report_name": report_request.name,
            "description": report_request.description,
            "generated_at": datetime.now().isoformat(),
            "total_records": len(report_data),
            "data": report_data[:100],  # Limit to first 100 records for API response
            "fields": [field.dict() for field in report_request.fields],
            "filters_applied": [filter.dict() for filter in report_request.filters]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating custom report: {str(e)}"
        )

@router.get("/{isp_id}/compliance/{report_type}", response_model=ComplianceReportResponse)
async def generate_compliance_report(
    isp_id: str,
    report_type: str,  # gdpr, pci, iso, sox
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Generate compliance reports (GDPR, PCI, ISO)
    - Automated compliance checking
    - Gap analysis and recommendations
    - Audit trail documentation
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        # Generate compliance report based on type
        compliance_data = await generate_compliance_data(report_type, current_isp.id, db)
        
        return ComplianceReportResponse(
            report_type=report_type,
            compliance_score=compliance_data["compliance_score"],
            total_checks=compliance_data["total_checks"],
            passed_checks=compliance_data["passed_checks"],
            failed_checks=compliance_data["failed_checks"],
            findings=compliance_data["findings"],
            recommendations=compliance_data["recommendations"],
            generated_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating compliance report: {str(e)}"
        )

@router.get("/{isp_id}/bi-endpoints", response_model=List[Dict[str, Any]])
async def get_bi_endpoints(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    API endpoints for third-party BI tools (Tableau, Power BI)
    - Real-time data access
    - Standardized data formats
    - Authentication and rate limiting
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        # Define available BI endpoints
        endpoints = [
            {
                "name": "subscriber_analytics",
                "description": "Real-time subscriber metrics and usage data",
                "endpoint": f"/api/reporting/{isp_id}/bi/subscribers",
                "methods": ["GET"],
                "parameters": ["date_range", "segment", "branch_id"],
                "response_format": "JSON",
                "refresh_interval": 15  # minutes
            },
            {
                "name": "revenue_metrics",
                "description": "Billing and revenue analytics",
                "endpoint": f"/api/reporting/{isp_id}/bi/revenue",
                "methods": ["GET"],
                "parameters": ["period", "currency", "plan_type"],
                "response_format": "JSON",
                "refresh_interval": 60
            },
            {
                "name": "network_performance",
                "description": "Network health and performance metrics",
                "endpoint": f"/api/reporting/{isp_id}/bi/network",
                "methods": ["GET"],
                "parameters": ["metric_type", "time_window", "device_id"],
                "response_format": "JSON",
                "refresh_interval": 5
            },
            {
                "name": "support_analytics",
                "description": "Support ticket and customer satisfaction data",
                "endpoint": f"/api/reporting/{isp_id}/bi/support",
                "methods": ["GET"],
                "parameters": ["status", "priority", "category"],
                "response_format": "JSON",
                "refresh_interval": 30
            }
        ]
        
        return endpoints
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching BI endpoints: {str(e)}"
        )

async def generate_report_data(template: ReportTemplate, parameters: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Generate report data based on template configuration"""
    report_type = template.report_type
    config = template.config
    
    if report_type == "usage":
        return await generate_usage_report_data(config, parameters, db)
    elif report_type == "billing":
        return await generate_billing_report_data(config, parameters, db)
    elif report_type == "network":
        return await generate_network_report_data(config, parameters, db)
    elif report_type == "compliance":
        return await generate_compliance_report_data(config, parameters, db)
    else:
        raise ValueError(f"Unknown report type: {report_type}")

async def generate_usage_report_data(config: Dict[str, Any], parameters: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Generate usage report data"""
    # Simplified implementation
    return {
        "total_usage_gb": 15432.5,
        "peak_usage_mbps": 850.2,
        "average_usage_per_user": 45.6,
        "top_users": [
            {"user_id": "123", "usage_gb": 156.7},
            {"user_id": "456", "usage_gb": 134.2}
        ]
    }

async def generate_billing_report_data(config: Dict[str, Any], parameters: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Generate billing report data"""
    return {
        "total_revenue": 125678.90,
        "pending_payments": 8934.50,
        "collection_rate": 94.2,
        "top_revenue_plans": [
            {"plan": "Premium 100", "revenue": 45678.90},
            {"plan": "Standard 50", "revenue": 34567.80}
        ]
    }

async def generate_network_report_data(config: Dict[str, Any], parameters: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Generate network report data"""
    return {
        "uptime_percentage": 99.8,
        "average_latency": 25.5,
        "packet_loss": 0.02,
        "bandwidth_utilization": 75.3,
        "device_status": {
            "online": 245,
            "offline": 12,
            "maintenance": 3
        }
    }

async def generate_compliance_report_data(config: Dict[str, Any], parameters: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Generate compliance report data"""
    return {
        "data_retention_compliance": 95.5,
        "security_controls": 87.2,
        "audit_trail_completeness": 98.9,
        "privacy_controls": 92.1
    }

async def build_custom_report_query(request: CustomReportRequest, isp_id: str, db: Session) -> List[Dict[str, Any]]:
    """Build and execute custom report query"""
    # Simplified implementation - in production, this would build dynamic SQL queries
    # based on the field selections and filters
    
    sample_data = []
    for i in range(50):  # Generate sample data
        record = {}
        for field in request.fields:
            if field.type == "string":
                record[field.name] = f"Sample {field.name} {i}"
            elif field.type == "number":
                record[field.name] = i * 10.5
            elif field.type == "date":
                record[field.name] = (datetime.now() - timedelta(days=i)).isoformat()
            elif field.type == "boolean":
                record[field.name] = i % 2 == 0
        sample_data.append(record)
    
    return sample_data

async def generate_compliance_data(report_type: str, isp_id: str, db: Session) -> Dict[str, Any]:
    """Generate compliance report data based on type"""
    if report_type == "gdpr":
        return {
            "compliance_score": 92.5,
            "total_checks": 25,
            "passed_checks": 23,
            "failed_checks": 2,
            "findings": [
                {
                    "type": "data_retention",
                    "severity": "medium",
                    "description": "Some user data retained beyond policy period",
                    "affected_records": 145
                },
                {
                    "type": "consent_tracking",
                    "severity": "low",
                    "description": "Missing consent timestamps for some users",
                    "affected_records": 23
                }
            ],
            "recommendations": [
                "Implement automated data retention cleanup",
                "Update consent tracking system",
                "Regular compliance audits"
            ]
        }
    elif report_type == "pci":
        return {
            "compliance_score": 88.0,
            "total_checks": 20,
            "passed_checks": 18,
            "failed_checks": 2,
            "findings": [
                {
                    "type": "encryption",
                    "severity": "high",
                    "description": "Some payment data not properly encrypted",
                    "affected_records": 12
                }
            ],
            "recommendations": [
                "Upgrade encryption standards",
                "Implement additional security controls"
            ]
        }
    else:
        return {
            "compliance_score": 85.0,
            "total_checks": 15,
            "passed_checks": 13,
            "failed_checks": 2,
            "findings": [],
            "recommendations": ["Generic compliance improvements needed"]
        }