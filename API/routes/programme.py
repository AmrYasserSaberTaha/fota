from fastapi import APIRouter, HTTPException
from API.utils import split_into_chunks
from API.validators.programme_validator import ProgrammeValidator
from firebase_storage import get_ref_child, get_item_by_name
from typing import Any, Dict

programmeRouter: APIRouter = APIRouter(
    prefix="/programmes",
    tags=["Programmes"]
)


@programmeRouter.get(path="/all")
async def get_programmes():
    """
    A function to retrieve all programmes from Firebase and return the data.
    """
    ref = get_ref_child("Programmes")
    data = ref.get()
    return {"data": data}


@programmeRouter.get("/{programme_id}")
async def get_programme(programme_id: str):
    """
    Get a programme by its ID.

    Args:
        programme_id (str): The ID of the programme to retrieve.

    Returns:
        dict: The programme data.
    Raises:
        HTTPException: If the programme is not found.
    """

    ref = get_ref_child("Programmes")
    programme_ref = ref.child(programme_id)
    data = programme_ref.get()
    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return data


@programmeRouter.get("/search/{programme_name}")
async def get_programme_by_name(programme_name: str):
    """
    Get a programme by its name.

    Args:
        programme_name (str): The name of the programme to search for.

    Returns:
        dict: A dictionary containing the data of the programme.

    Raises:
        HTTPException: If the programme is not found, raise status code 404 with detail "Item not found".
    """
    data = get_item_by_name(programme_name)
    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"data": data}


@programmeRouter.post("/programme")
async def post_programme(request: ProgrammeValidator):
    """
    Endpoint to create a new programme.

    Args:
    - request: ProgrammeValidator - The request body containing the programme data.

    Returns:
    - dict: A dictionary containing the unique key of the newly created programme.
    """
    # Check if the item with the same name already exists
    if get_item_by_name(request.name) is not None:
        raise HTTPException(status_code=400, detail="Item already exists")

    # Get reference to the 'Programmes' child in the database
    ref = get_ref_child("Programmes")

    # Prepare the programme data and split it into chunks if needed
    data = request.model_dump()
    data_chunks = split_into_chunks(data["data"].strip())
    data["data"] = data_chunks

    # Push the data to the database and retrieve the unique key
    key = ref.push(data).key

    return {"unique_key": str(key)}


@programmeRouter.get("/programme/flash/{programme_id}")
async def flash_programme(programme_id: str, index: int = 0) -> Dict[str, Any]:
    """
    Get programme data and format it for flash display.

    Args:
    - programme_id (str): The ID of the programme.
    - index (int): The index of the data to display.

    Returns:
    - Dict[str, Any]: A dictionary with the next index, formatted data string, and its size.
    """
    programme_data = await get_programme(programme_id)

    if not programme_data or index < 0 or index >= len(programme_data.get("data")):
        raise HTTPException(status_code=400, detail="Invalid index value")

    data = programme_data.get("data")[index]
    next_data = programme_data.get("data")[index + 1] if index < len(programme_data.get("data")) - 1 else "N/A"
    data_string = "\n".join(data)
    next_data_string = "\n".join(next_data) if next_data != "N/A" else "N/A"

    next_index = -1 if index == len(programme_data.get("data")) - 1 else index + 1
    response = {
        "number of junks": len(programme_data.get("data")),
        "next": next_index,
        "data": data_string,
        "number of records in junk": len(data),
        "size": len(data_string),
        "next size": len(next_data_string) if next_data_string != "N/A" else "N/A",
    }

    return response


@programmeRouter.get("/programme/flash/name/{programme_name}")
async def flash_programme_by_name(programme_name: str, index: int = 0) -> dict:
    """
    Retrieves a programme by its name and returns the programme data at the specified index.

    Parameters:
    - programme_name: str, the name of the programme to retrieve
    - index: int, optional, the index of the programme data to retrieve (default is 0)

    Returns:
    - dict: A dictionary containing the number of programme data items, the next index, the combined data string, and the size of the data string.
    """
    # Check if the programme exists
    programme_data = get_programme_by_name(programme_name)
    if programme_data is None:
        raise HTTPException(status_code=400, detail="Cannot find programme")

    # Check for valid index and retrieve data
    programme_data_items = programme_data.get("data")
    if index < 0 or index >= len(programme_data_items):
        raise HTTPException(status_code=400, detail="Invalid index value")

    # Generate data string and prepare response
    data = programme_data_items[index]
    data_string = "\n".join(data)
    next_index = index + 1 if index < len(data) - 1 else -1
    response = {
        "number of junks": len(programme_data_items),
        "next index": next_index,
        "data": data_string,
        "size": len(data_string),
        "number of records in junk": len(programme_data_items[index]),
        "next junk size": len(programme_data_items[next_index]) if next_index != -1 else "N/A"
    }

    return response
