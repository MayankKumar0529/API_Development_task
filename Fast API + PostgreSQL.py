
!pip install asyncpg fastapi sqlalchemy uvicorn

from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, JSON
import asyncio

# Database config
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/dbname"  # change this

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Database models
class BogieChecksheet(Base):
    __tablename__ = "bogie_checksheet"
    id = Column(Integer, primary_key=True, index=True)
    form_number = Column(String, unique=True, index=True)
    inspection_by = Column(String)
    inspection_date = Column(String)
    bmbc_checksheet = Column(JSON)
    bogie_checksheet = Column(JSON)
    bogie_details = Column(JSON)

class WheelSpecification(Base):
    __tablename__ = "wheel_specifications"
    id = Column(Integer, primary_key=True, index=True)
    form_number = Column(String, unique=True, index=True)
    submitted_by = Column(String)
    submitted_date = Column(String)
    fields = Column(JSON)

# Pydantic schemas
class BogieChecksheetSchema(BaseModel):
    formNumber: str
    inspectionBy: str
    inspectionDate: str
    bmbcChecksheet: Optional[Dict]
    bogieChecksheet: Optional[Dict]
    bogieDetails: Optional[Dict]

class BogieChecksheetResponseData(BaseModel):
    formNumber: str
    inspectionBy: str
    inspectionDate: str
    status: str

class BogieChecksheetResponse(BaseModel):
    success: bool
    message: str
    data: BogieChecksheetResponseData

class WheelSpecificationSchema(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: str
    fields: Optional[Dict]

# Moved the definition before it is used
class WheelSpecificationResponseData(BaseModel):
    formNumber: str
    status: str
    submittedBy: str
    submittedDate: str

class WheelSpecificationResponse(BaseModel):
    success: bool
    message: str
    data: WheelSpecificationResponseData


class WheelSpecItem(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: str
    fields: Optional[Dict]

class WheelSpecListResponse(BaseModel):
    success: bool
    message: str
    data: List[WheelSpecItem]


# FastAPI app
app = FastAPI()

# Create tables at startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

# API endpoints

# 1 POST /api/forms/bogie-checksheet
@app.post("/api/forms/bogie-checksheet", response_model=BogieChecksheetResponse, status_code=201)
async def create_bogie_checksheet(data: BogieChecksheetSchema, db: AsyncSession = Depends(get_db)):
    new_item = BogieChecksheet(
        form_number=data.formNumber,
        inspection_by=data.inspectionBy,
        inspection_date=data.inspectionDate,
        bmbc_checksheet=data.bmbcChecksheet,
        bogie_checksheet=data.bogieChecksheet,
        bogie_details=data.bogieDetails
    )
    db.add(new_item)
    await db.commit()
    return BogieChecksheetResponse(
        success=True,
        message="Bogie checksheet submitted successfully.",
        data=BogieChecksheetResponseData(
            formNumber=data.formNumber,
            inspectionBy=data.inspectionBy,
            inspectionDate=data.inspectionDate,
            status="Saved"
        )
    )

# 2 POST /api/forms/wheel-specifications
@app.post("/api/forms/wheel-specifications", response_model=WheelSpecificationResponse, status_code=201)
async def create_wheel_spec(data: WheelSpecificationSchema, db: AsyncSession = Depends(get_db)):
    new_item = WheelSpecification(
        form_number=data.formNumber,
        submitted_by=data.submittedBy,
        submitted_date=data.submittedDate,
        fields=data.fields
    )
    db.add(new_item)
    await db.commit()
    return WheelSpecificationResponse(
        success=True,
        message="Wheel specification submitted successfully.",
        data=WheelSpecificationResponseData(
            formNumber=data.formNumber,
            submittedBy=data.submittedBy,
            submittedDate=data.submittedDate,
            status="Saved"
        )
    )

# 3 GET /api/forms/wheel-specifications?formNumber=...&submittedBy=...&submittedDate=...
@app.get("/api/forms/wheel-specifications", response_model=WheelSpecListResponse)
async def get_wheel_specs(
    formNumber: Optional[str] = Query(None),
    submittedBy: Optional[str] = Query(None),
    submittedDate: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    filters = []
    params = {}

    if formNumber:
        filters.append("form_number=:formNumber")
        params["formNumber"] = formNumber
    if submittedBy:
        filters.append("submitted_by=:submittedBy")
        params["submittedBy"] = submittedBy
    if submittedDate:
        filters.append("submitted_date=:submittedDate")
        params["submittedDate"] = submittedDate

    filter_query = " AND ".join(filters) if filters else "TRUE"

    result = await db.execute(
        f"SELECT * FROM wheel_specifications WHERE {filter_query}",
        params
    )
    rows = result.fetchall()

    data = [
        WheelSpecItem(
            formNumber=row.form_number,
            submittedBy=row.submitted_by,
            submittedDate=row.submitted_date,
            fields=row.fields
        )
        for row in rows
    ]

    return WheelSpecListResponse(
        success=True,
        message="Filtered wheel specification forms fetched successfully.",
        data=data
    )