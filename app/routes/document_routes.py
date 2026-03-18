from fastapi import APIRouter

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/")
def get_documents():
    return {"message": "documents endpoint working"}