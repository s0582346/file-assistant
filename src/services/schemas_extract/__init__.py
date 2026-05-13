from src.models.document import DocumentType
from src.services.schemas_extract.invoice import InvoiceFields
from src.services.schemas_extract.payslip import PayslipFields
from src.services.schemas_extract.receipt import ReceiptFields

SCHEMA_BY_TYPE = {
    DocumentType.invoice: InvoiceFields,
    DocumentType.receipt: ReceiptFields,
    DocumentType.payslip: PayslipFields,
}

__all__ = [
    "InvoiceFields",
    "PayslipFields",
    "ReceiptFields",
    "SCHEMA_BY_TYPE",
]
