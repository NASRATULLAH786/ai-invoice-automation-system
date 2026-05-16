from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.ai_extractor import extract_invoice_data
from app.database import create_tables, SessionLocal, Invoice

app = FastAPI(title="AI Invoice Automation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvoiceRequest(BaseModel):
    invoice_text: str


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def home():
    return {
        "message": "AI Invoice Automation System is running"
    }


@app.post("/extract-invoice")
def extract_invoice(request: InvoiceRequest):
    result = extract_invoice_data(request.invoice_text)

    if "error" in result:
        return result

    db = SessionLocal()

    invoice = Invoice(
        company_name=result.get("company_name"),
        invoice_number=result.get("invoice_number"),
        date=result.get("date"),
        total_amount=result.get("total_amount")
    )

    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    db.close()

    return {
        "message": "Invoice extracted and saved successfully",
        "invoice": result
    }


@app.get("/invoices")
def get_invoices():
    db = SessionLocal()
    invoices = db.query(Invoice).all()
    db.close()

    return invoices