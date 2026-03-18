from pathlib import Path

from src.document_reader import list_documents, read_document

RESOURCES_DIR = Path(__file__).parent.parent / "resources"


def register_tools(mcp):
    """Register all MCP tools on the given FastMCP instance."""

    @mcp.tool()
    def scan_documents(directory: str = "") -> str:
        """List all supported receipt/invoice files in a directory.

        Args:
            directory: Path to scan. Defaults to the resources folder.
        """
        target = directory if directory else str(RESOURCES_DIR)

        try:
            files = list_documents(target)
        except NotADirectoryError as e:
            return str(e)

        if not files:
            return f"No supported documents found in '{target}'."

        lines = [f"{i + 1}. {Path(f).name}" for i, f in enumerate(files)]
        return f"Found {len(files)} document(s):\n" + "\n".join(lines)

    @mcp.tool()
    def extract_receipt(file_name: str) -> str:
        """Extract structured data from a receipt or invoice in the resources folder.

        Args:
            file_name: Name of the file in the resources folder (e.g. 'invoice.pdf').
        """
        file_path = RESOURCES_DIR / file_name

        if not file_path.exists():
            return f"Error: file '{file_name}' not found in resources."

        try:
            data = read_document(str(file_path))
        except ValueError as e:
            return f"Error: {e}"

        lines = [f"{key}: {value}" for key, value in data.items()]
        return "\n".join(lines)
