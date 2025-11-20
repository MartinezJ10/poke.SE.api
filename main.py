import uvicorn
import json
from fastapi import FastAPI
from utils.database import execute_query_json
from controllers.PokeRequestController import insert_pokemon_request,delete_pokemon_request,update_pokemon_request,select_pokemon_request,get_all_request
from models.PokeRequest import PokemonRequest
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/")
async def root():
    query = "select * from pokequeue.MESSAGES"
    results = await execute_query_json(query)
    result_dict = json.loads(results)
    return result_dict

@app.get("/api/version")
async def version():
    return {"version": "0.3.0"}

@app.get("/api/request/{id}")
async def select_request(id: int):
    result = await select_pokemon_request(id)
    return result

@app.delete("/api/request/{id}")
async def delete_request(id: int):
    result = await delete_pokemon_request(id)
    return result

@app.get("/api/request")
async def select_all_request():
    return await get_all_request()

@app.post("/api/request")
async def create_request(pokemon_request: PokemonRequest):
    result = await insert_pokemon_request(pokemon_request)
    return result

@app.put("/api/request")
async def update_request(pokemon_request: PokemonRequest):
    result = await update_pokemon_request(pokemon_request)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)