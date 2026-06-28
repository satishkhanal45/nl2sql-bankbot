# app/db/repositories/entity_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.models.entity import Entity, Attribute, EntityValue
from typing import Optional


def get_entity_by_name_and_fact(
    db: Session,
    entity_name: str,
    fact: str,
) -> Optional[Entity]:
    """
    Fetch a single entity by its name and fact.

    Example:
        get_entity_by_name_and_fact(db, "bank", "home_loan")
        → <Entity(id=2, entity_name='bank', fact='home_loan')>
    """
    return (
        db.query(Entity)
        .filter(
            Entity.entity_name == entity_name,
            Entity.fact == fact,
        )
        .first()
    )


def get_attribute_by_label(
    db: Session,
    label: str,
) -> Optional[Attribute]:
    """
    Fetch a single attribute by its label.

    Example:
        get_attribute_by_label(db, "interest_rate")
        → <Attribute(id=4, label='interest_rate')>
    """
    return (
        db.query(Attribute)
        .filter(Attribute.label == label)
        .first()
    )


def get_entity_value(
    db: Session,
    entity_id: int,
    attribute_id: int,
) -> Optional[EntityValue]:
    """
    Fetch a value by entity_id and attribute_id.

    Example:
        get_entity_value(db, entity_id=2, attribute_id=4)
        → <EntityValue(value='8.5', type='numeric')>
    """
    return (
        db.query(EntityValue)
        .filter(
            EntityValue.entity_id == entity_id,
            EntityValue.attribute_id == attribute_id,
        )
        .first()
    )


def get_value_by_entity_fact_attribute(
    db: Session,
    entity_name: str,
    fact: str,
    attribute: str,
) -> Optional[dict]:
    """
    The main query function used by the chatbot.

    Given an entity, fact, and attribute — returns the matching value.

    Example:
        get_value_by_entity_fact_attribute(
            db,
            entity_name="bank",
            fact="home_loan",
            attribute="interest_rate",
        )
        → {"value": "8.5", "type": "numeric", "path_name": "bank.home_loan.interest_rate"}

    Returns None if no match is found.
    """
    result = (
        db.query(
            EntityValue.value,
            EntityValue.type,
            EntityValue.path_name,
        )
        .join(Entity, Entity.id == EntityValue.entity_id)
        .join(Attribute, Attribute.id == EntityValue.attribute_id)
        .filter(
            Entity.entity_name == entity_name,
            Entity.fact == fact,
            Attribute.label == attribute,
        )
        .first()
    )

    if result is None:
        return None

    return {
        "value": result.value,
        "type": result.type,
        "path_name": str(result.path_name) if result.path_name else None,
    }


def get_all_facts_for_entity(
    db: Session,
    entity_name: str,
) -> list[dict]:
    """
    Returns all facts and their values for a given entity.
    Useful for listing everything we know about 'bank'.

    Example:
        get_all_facts_for_entity(db, "bank")
        → [
            {"fact": "home_loan", "attribute": "interest_rate", "value": "8.5"},
            {"fact": "home_loan", "attribute": "loan_amount", "value": "5000000"},
            ...
          ]
    """
    results = (
        db.query(
            Entity.fact,
            Attribute.label.label("attribute"),
            EntityValue.value,
            EntityValue.type,
            EntityValue.path_name,
        )
        .join(Entity, Entity.id == EntityValue.entity_id)
        .join(Attribute, Attribute.id == EntityValue.attribute_id)
        .filter(Entity.entity_name == entity_name)
        .order_by(Entity.fact, Attribute.label)
        .all()
    )

    return [
        {
            "fact": row.fact,
            "attribute": row.attribute,
            "value": row.value,
            "type": row.type,
            "path_name": str(row.path_name) if row.path_name else None,
        }
        for row in results
    ]


def get_values_by_ltree_path(
    db: Session,
    path_prefix: str,
) -> list[dict]:
    """
    Uses LTREE's <@ operator to fetch all values under a path.

    Example:
        get_values_by_ltree_path(db, "bank.home_loan")
        → all values whose path starts with 'bank.home_loan'

    This is the power of LTREE — hierarchical queries.
    """
    results = db.execute(
        text("""
            SELECT
                ev.path_name,
                ev.value,
                ev.type,
                a.label AS attribute
            FROM entity_value ev
            JOIN attribute a ON a.id = ev.attribute_id
            WHERE ev.path_name <@ CAST(:path AS ltree)
            ORDER BY ev.path_name
        """),
        {"path": path_prefix},
    ).fetchall()

    return [
        {
            "path_name": str(row.path_name),
            "attribute": row.attribute,
            "value": row.value,
            "type": row.type,
        }
        for row in results
    ]