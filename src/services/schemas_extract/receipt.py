from pydantic import BaseModel, Field


class ReceiptFields(BaseModel):
    """Fields extracted from a receipt (Quittung / Kassenbon)."""

    receipt_number: str = Field(default="", description="Receipt number / Belegnummer if present")
    date: str = Field(default="", description="Receipt date in DD.MM.YYYY format (Belegdatum)")
    vendor: str = Field(default="", description="Vendor / merchant name")
    category: str = Field(default="", description="Spend category, e.g. Büromaterial, Lebensmittel, Reisekosten")
    currency: str = Field(default="EUR", description="ISO currency code, e.g. EUR, USD")
    tax_amount: str = Field(default="", description="Tax amount as numeric with 2 decimals (Steuerbetrag)")
    gross_amount: str = Field(default="", description="Gross / total amount as numeric with 2 decimals (Bruttobetrag)")
    tax_rate: str = Field(default="", description="VAT rate in percent, e.g. '19' or '7'")
    payment_method: str = Field(default="", description="e.g. Bar, EC-Karte, Kreditkarte, PayPal")
