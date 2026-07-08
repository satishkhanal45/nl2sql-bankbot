# app/db/models/entity.py
from sqlalchemy import (
    String, Integer, DateTime, Text,
    UniqueConstraint, ForeignKey, Index, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.db.models.base import Base


class Entity(Base):
    """
    Represents an entity and its fact.
    Example: entity_name='bank', fact='home_loan'
    """
    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_name: Mapped[str] = mapped_column(String(100), nullable=False)
    fact: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )

    # One entity can have many values
    values: Mapped[list["EntityValue"]] = relationship(
        "EntityValue",
        back_populates="entity",
        cascade="all, delete",
    )

    __table_args__ = (
        UniqueConstraint("entity_name", "fact", name="uq_entity_fact"),
        Index("idx_entity_name", "entity_name"),
        Index("idx_entity_fact", "fact"),
    )

    def __repr__(self) -> str:
        return f"<Entity(id={self.id}, entity_name='{self.entity_name}', fact='{self.fact}')>"


class Attribute(Base):
    """
    Represents a type of attribute.
    Example: label='interest_rate', label='address'
    """
    __tablename__ = "attribute"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )

    # One attribute can appear in many values
    values: Mapped[list["EntityValue"]] = relationship(
        "EntityValue",
        back_populates="attribute",
        cascade="all, delete",
    )

    __table_args__ = (
        UniqueConstraint("label", name="uq_attribute_label"),
        Index("idx_attribute_label", "label"),
    )

    def __repr__(self) -> str:
        return f"<Attribute(id={self.id}, label='{self.label}')>"


class EntityValue(Base):
    __tablename__ = "entity_value"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("entity.id", ondelete="CASCADE"),
        nullable=False,
    )
    attribute_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("attribute.id", ondelete="CASCADE"),
        nullable=False,
    )
    path_name: Mapped[str | None] = mapped_column(String, nullable=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="string",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )

    entity: Mapped["Entity"] = relationship("Entity", back_populates="values")
    attribute: Mapped["Attribute"] = relationship("Attribute", back_populates="values")

    __table_args__ = (
        # Changed from (entity_id, attribute_id) to (entity_id, path_name)
        UniqueConstraint("entity_id", "path_name", name="uq_entity_path"),
        Index("idx_ev_entity_id", "entity_id"),
        Index("idx_ev_attribute_id", "attribute_id"),
        CheckConstraint(
            "type IN ('string', 'numeric', 'boolean', 'date')",
            name="ck_entity_value_type",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<EntityValue(id={self.id}, "
            f"entity_id={self.entity_id}, "
            f"attribute_id={self.attribute_id}, "
            f"value='{self.value}')>"
        )