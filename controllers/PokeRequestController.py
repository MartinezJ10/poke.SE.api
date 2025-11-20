import json
import logging
from fastapi import HTTPException
from models.PokeRequest import PokemonRequest 
from utils.database import execute_query_json
from utils.AQueue import AQueue
from utils.ABlob import ABlob
#configurar el logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def select_pokemon_request(id:int) -> dict:
    try:
        query = "select * from pokequeue.requests where id = ?"
        params = (id,)
        result = await execute_query_json(query, params)
        result_dict = json.loads(result)
        
        return  result_dict
    except Exception as e:
        logger.error(f"Error selecting Pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def delete_pokemon_request(id: int) -> dict:
    try:
        query = "EXEC pokequeue.delete_poke_request @id = ?;"
        params = (id,)
        result = await execute_query_json(query, params, True)
        result_dict = json.loads(result)
    except Exception as db_error:
        logger.error(f"Database deletion failed: {db_error}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to delete request from database"
        )

    try:
        blob = ABlob()
        blob.delete_blob(id)
    except Exception as blob_error:
        logger.warning(f"Blob deletion skipped or failed {blob_error}")

    return result_dict


async def update_pokemon_request(pokemon_request: PokemonRequest) -> dict:
    try:
        query = "exec pokequeue.update_poke_request ?, ?, ?"
        
        if not pokemon_request.url:
            pokemon_request.url = ""
        
        params = (pokemon_request.id, pokemon_request.status, pokemon_request.url)
        result = await execute_query_json(query, params, True)
        result_dict = json.loads(result)
        
        return  result_dict
    except Exception as e:
        logger.error(f"Error updating Pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def insert_pokemon_request(pokemon_request: PokemonRequest) -> dict:
    try:
        query = "exec pokequeue.create_poke_request ?, ? "
        params = (pokemon_request.pokemon_type,pokemon_request.sample_size)
        result = await execute_query_json(query, params, True)
        result_dict = json.loads(result)
        
        await AQueue().insert_message_on_queue(result)
        
        return  result_dict
    except Exception as e:
        logger.error(f"Error inserting Pokemon request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



async def get_all_request() -> dict:
    query = """
        select 
            r.id as ReportId
            , s.description as Status
            , r.type as PokemonType
            , r.url 
            , r.samplesize 
            , r.created 
            , r.updated
        from pokequeue.requests r 
        inner join pokequeue.status s 
        on r.id_status = s.id 
    """
    result = await execute_query_json( query  )
    result_dict = json.loads(result)
    blob = ABlob()
    for record in result_dict:
        id = record['ReportId']
        record['url'] = f"{record['url']}?{blob.generate_sas(id)}"
    return result_dict
