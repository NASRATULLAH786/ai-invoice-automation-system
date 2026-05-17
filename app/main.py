from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.ai_extractor import extract_invoice_data
from app.database import create_tables, SessionLocal, Invoice


app = FastAPI(
    title="AI Invoice Automation System",
    description="AI-powered invoice extraction and workflow automation platform.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvoiceRequest(BaseModel):
    invoice_text: str = Field(
        ...,
        min_length=10,
        description="Raw invoice text that will be processed by the AI extractor.",
        example="Invoice Number: INV-1001\nCompany: ABC Ltd\nDate: 2026-05-16\nTotal: $250.00",
    )


@app.on_event("startup")
def startup():
    create_tables()


@app.get(
    "/",
    summary="Health check",
    description="Checks whether the AI Invoice Automation backend is running.",
)
def home():
    return {"message": "AI Invoice Automation System is running"}


@app.post(
    "/extract-invoice",
    summary="Extract invoice information",
    description="Processes invoice text and extracts structured invoice data using AI-powered automation.",
)
def extract_invoice(request: InvoiceRequest):
    try:
        result = extract_invoice_data(request.invoice_text)

        if not isinstance(result, dict):
            raise HTTPException(
                status_code=500,
                detail="AI extractor returned an invalid response format.",
            )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        db = SessionLocal()

        invoice = Invoice(
            company_name=result.get("company_name"),
            invoice_number=result.get("invoice_number"),
            date=result.get("date"),
            total_amount=result.get("total_amount"),
        )

        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        return {
            "message": "Invoice extracted and saved successfully",
            "invoice": {
                "id": invoice.id,
                "company_name": invoice.company_name,
                "invoice_number": invoice.invoice_number,
                "date": invoice.date,
                "total_amount": invoice.total_amount,
            },
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if "db" in locals():
            db.close()


@app.get(
    "/invoices",
    summary="Get saved invoices",
    description="Returns all invoices saved in the local database.",
)
def get_invoices():
    try:
        db = SessionLocal()
        invoices = db.query(Invoice).all()

        return [
            {
                "id": invoice.id,
                "company_name": invoice.company_name,
                "invoice_number": invoice.invoice_number,
                "date": invoice.date,
                "total_amount": invoice.total_amount,
            }
            for invoice in invoices
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if "db" in locals():
            db.close()