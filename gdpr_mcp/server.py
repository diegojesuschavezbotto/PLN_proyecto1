from mcp.server.fastmcp import FastMCP
from pipeline.auditor import audit_company_text

mcp = FastMCP("gdpr-auditor")


@mcp.tool()
def audit_gdpr_compliance(company_text: str) -> str:
    """
    Analiza texto empresarial y verifica cumplimiento con GDPR.
    """

    from io import StringIO
    import sys

    buffer = StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buffer

    try:
        audit_company_text(company_text)
    finally:
        sys.stdout = sys_stdout

    return buffer.getvalue()


if __name__ == "__main__":
    mcp.run()