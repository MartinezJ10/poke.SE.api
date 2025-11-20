from pydantic import BaseModel, Field
from typing import Optional

class PokemonRequest(BaseModel):
    id: Optional[int] = Field(None, ge=1, description="The unique identifier for the poke request")
    sample_size: Optional[int] = Field(None, gt=0, description="sample size of pokemon to report")
    pokemon_type: Optional[str] = Field(None, pattern="^[a-zA-Z0-9_]+$", description="The type of the Pokémon")
    url: Optional[str] = Field(None, pattern="^https?://[^\s]+$", description="The URL associated with the poke request")
    status: Optional[str] = Field(None, pattern="^(sent|completed|failed|inprogress)$", description="The status of the poke request")
    