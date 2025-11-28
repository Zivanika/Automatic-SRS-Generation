from datetime import datetime
from typing import Optional
from bson import ObjectId

class SRSDocument:
    """SRS Document model matching the MongoDB schema"""
    
    def __init__(
        self,
        owner: str,  # User ID or username
        name: str,
        description: str,
        status: str = "Pending",
        pdf_url: str = "",
        word_url: str = "",
        rating: Optional[int] = None,
        praises: Optional[list] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id
        self.owner = owner
        self.name = name
        self.description = description
        self.status = status
        self.pdf_url = pdf_url
        self.word_url = word_url
        self.rating = rating
        self.praises = praises or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB insertion"""
        # Convert owner string to ObjectId if it looks like a valid ObjectId
        owner_value = self.owner
        if isinstance(self.owner, str) and len(self.owner) == 24:
            try:
                owner_value = ObjectId(self.owner)
            except Exception:
                # If conversion fails, keep as string
                owner_value = self.owner
        
        doc = {
            "owner": owner_value,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "pdf_url": self.pdf_url,
            "word_url": self.word_url,
            "rating": self.rating,
            "praises": self.praises,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }
        
        if self._id:
            doc["_id"] = self._id
        
        return doc
    
    @staticmethod
    def from_dict(doc: dict) -> 'SRSDocument':
        """Create SRSDocument from MongoDB document"""
        # Convert ObjectId owner to string for Python processing
        owner_value = doc["owner"]
        if isinstance(owner_value, ObjectId):
            owner_value = str(owner_value)
        
        return SRSDocument(
            _id=doc.get("_id"),
            owner=owner_value,
            name=doc["name"],
            description=doc["description"],
            status=doc.get("status", "Pending"),
            pdf_url=doc.get("pdf_url", ""),
            word_url=doc.get("word_url", ""),
            rating=doc.get("rating"),
            praises=doc.get("praises", []),
            created_at=doc.get("createdAt"),
            updated_at=doc.get("updatedAt")
        )


class SRSRepository:
    """Repository for SRS database operations"""
    
    def __init__(self, db):
        self.collection = db["srs"]
    
    def create(self, srs: SRSDocument) -> str:
        """Insert new SRS document"""
        result = self.collection.insert_one(srs.to_dict())
        return str(result.inserted_id)
    
    def update(self, srs_id: str, updates: dict) -> bool:
        """Update SRS document"""
        updates["updatedAt"] = datetime.utcnow()
        result = self.collection.update_one(
            {"_id": ObjectId(srs_id)},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    def find_by_owner(self, owner: str) -> list[SRSDocument]:
        """Find all SRS documents by owner"""
        # Convert owner string to ObjectId for query
        owner_query = ObjectId(owner) if len(owner) == 24 else owner
        docs = self.collection.find({"owner": owner_query}).sort("createdAt", -1)
        return [SRSDocument.from_dict(doc) for doc in docs]
    
    def find_latest_by_owner(self, owner: str) -> Optional[SRSDocument]:
        """Find the most recent SRS document by owner"""
        # Convert owner string to ObjectId for query
        owner_query = ObjectId(owner) if len(owner) == 24 else owner
        doc = self.collection.find_one(
            {"owner": owner_query},
            sort=[("createdAt", -1)]
        )
        return SRSDocument.from_dict(doc) if doc else None
    
    def find_by_id(self, srs_id: str) -> Optional[SRSDocument]:
        """Find SRS document by ID"""
        doc = self.collection.find_one({"_id": ObjectId(srs_id)})
        return SRSDocument.from_dict(doc) if doc else None

