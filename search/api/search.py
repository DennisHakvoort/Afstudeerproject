from fastapi import APIRouter
from pydantic.main import BaseModel

from delegator.delegator import execute_search

router = APIRouter(
    prefix="/search"
)


class SearchRequest(BaseModel):
    query: str
    user_id: str


@router.post("/")
def search_request(search_request: SearchRequest):
    return execute_search(search_request.query, search_request.user_id)
