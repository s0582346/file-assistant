from pydantic import BaseModel, Field


class InvoiceFields(BaseModel):
    """Fields extracted from an invoice (Rechnung)."""

    invoice_number: str = Field(default="", description="Invoice number / Rechnungsnummer")
    issue_date: str = Field(default="", description="Issue date in DD.MM.YYYY format")
    due_date: str = Field(default="", description="Due date in DD.MM.YYYY format (Fälligkeitsdatum)")
    vendor: str = Field(default="", description="Issuer / vendor name (Rechnungssteller)")
    customer: str = Field(default="", description="Recipient / customer name (Rechnungsempfänger)")
    category: str = Field(default="", description="Spend category, e.g. Büromaterial, Reisekosten, IT")
    currency: str = Field(default="EUR", description="ISO currency code, e.g. EUR, USD")
    net_amount: str = Field(default="", description="Net amount as numeric with 2 decimals, e.g. '100.00'")
    tax_amount: str = Field(default="", description="Tax amount as numeric with 2 decimals (Steuerbetrag)")
    gross_amount: str = Field(default="", description="Gross amount as numeric with 2 decimals (Bruttobetrag)")
    tax_rate: str = Field(default="", description="VAT rate in percent, e.g. '19' or '7'")
    iban: str = Field(default="", description="Payment IBAN if present")
    vat_id: str = Field(default="", description="VAT ID of the vendor (USt-IdNr.)")
    payment_terms: str = Field(default="", description="Free-text payment terms if present")
