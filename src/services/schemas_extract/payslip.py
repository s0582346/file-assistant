from pydantic import BaseModel, Field


class PayslipFields(BaseModel):
    """Fields extracted from a German payslip (Gehaltsabrechnung / Lohnabrechnung)."""

    employer: str = Field(default="", description="Employer / company name (Arbeitgeber)")
    employee_name: str = Field(default="", description="Employee name (Arbeitnehmer)")
    employee_id: str = Field(default="", description="Personnel number if present (Personalnummer)")
    period_start: str = Field(default="", description="Pay period start in DD.MM.YYYY format")
    period_end: str = Field(default="", description="Pay period end in DD.MM.YYYY format")
    currency: str = Field(default="EUR", description="ISO currency code")
    gross_amount: str = Field(default="", description="Gross pay for the period (Bruttoverdienst), numeric with 2 decimals")
    net_amount: str = Field(default="", description="Net pay paid out (Auszahlungsbetrag / Netto), numeric with 2 decimals")
    tax_lohnsteuer: str = Field(default="", description="Income tax withheld (Lohnsteuer)")
    tax_solz: str = Field(default="", description="Solidarity surcharge (Solidaritätszuschlag)")
    tax_kirchensteuer: str = Field(default="", description="Church tax (Kirchensteuer) if applicable")
    social_kv: str = Field(default="", description="Health insurance contribution (Krankenversicherung)")
    social_rv: str = Field(default="", description="Pension contribution (Rentenversicherung)")
    social_av: str = Field(default="", description="Unemployment insurance contribution (Arbeitslosenversicherung)")
    social_pv: str = Field(default="", description="Long-term care insurance contribution (Pflegeversicherung)")
    ytd_gross: str = Field(default="", description="Year-to-date gross if present")
    ytd_net: str = Field(default="", description="Year-to-date net if present")
    tax_class: str = Field(default="", description="Tax class (Steuerklasse), e.g. '1', '3', '4'")
