from pydantic import BaseModel, Field


class Company(BaseModel):
    name: str = Field(description="Company name")

    founder: str = Field(description="Company founder")

    founded_year: int = Field(description="Year company was founded")

    description: str = Field(description="Short company description")
