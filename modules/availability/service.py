from sqlalchemy.orm import Session

from modules.availability.model import AvailabilityBlock
from modules.availability.schema import AvailabilityCreate


def create_block(db: Session, data: AvailabilityCreate) -> AvailabilityBlock:
    block = AvailabilityBlock(**data.dict())
    db.add(block)
    db.commit()
    db.refresh(block)
    return block


def list_blocks(db: Session, vehicle_id: int | None = None) -> list[AvailabilityBlock]:
    query = db.query(AvailabilityBlock)
    if vehicle_id:
        query = query.filter(AvailabilityBlock.vehicle_id == vehicle_id)
    return query.order_by(AvailabilityBlock.start_date).all()


def get_block(db: Session, block_id: int) -> AvailabilityBlock | None:
    return db.query(AvailabilityBlock).filter(AvailabilityBlock.id == block_id).first()


def delete_block(db: Session, block: AvailabilityBlock) -> None:
    db.delete(block)
    db.commit()
