from pathlib import Path

from src.config import settings
from src.services.document_reader import list_documents, read_document


def register_tools(mcp):
    """Register all MCP tools on the given FastMCP instance."""

    @mcp.tool()
    def scan_documents(directory: str = "") -> str:
        """List all supported business document files in a directory.

        Args:
            directory: Path to scan. Defaults to the resources folder.
        """
        target = directory if directory else str(settings.resources_dir)

        try:
            files = list_documents(target)
        except NotADirectoryError as e:
            return str(e)

        if not files:
            return f"No supported documents found in '{target}'."

        lines = [f"{i + 1}. {Path(f).name}" for i, f in enumerate(files)]
        return f"Found {len(files)} document(s):\n" + "\n".join(lines)

    @mcp.tool()
    def extract_document(file_name: str) -> str:
        """Classify and extract structured data from a business document.

        Auto-detects whether the document is an invoice, receipt, or payslip and
        extracts the matching field set. Supports PDF and image files (PNG, JPG,
        JPEG, WEBP, GIF).

        Args:
            file_name: Name of the file in the resources folder (e.g. 'invoice.pdf').
        """
        file_path = settings.resources_dir / file_name

        if not file_path.exists():
            return f"Error: file '{file_name}' not found in resources."

        try:
            doc_type, fields = read_document(str(file_path))
        except ValueError as e:
            return f"Error: {e}"

        header = f"Document type: {doc_type.value}"
        if not fields:
            return header + "\n(no fields extracted)"
        lines = [f"{key}: {value}" for key, value in fields.items()]
        return header + "\n" + "\n".join(lines)