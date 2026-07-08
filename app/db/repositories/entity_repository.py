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


def get_all_facts_for_entity(
    db: Session,
    entity_name: str,
) -> list[dict]:
    """
    Returns all facts and their values for a given entity.

    Example:
        get_all_facts_for_entity(db, "bank")
        → [
            {"fact": "home_loan", "attribute": "interest_rate", "value": "8.5"},
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


def search_by_query_type(
    db: Session,
    entity_name: str,
    fact: str,
    instance: Optional[str],
    attribute: Optional[str],
) -> dict:
    """
    Handles both specific and broad queries using 4-level LTREE paths.

    Path structure: bank.<category>.<instance>.<attribute>
    Examples:
        bank.loan.home_loan.interest_rate   ← specific
        bank.loan.home_loan                 ← broad (all home loan details)
        bank.loan                           ← broad (all loans)
        bank.branch.anamnagar.address       ← specific
        bank.branch.anamnagar               ← broad (all anamnagar details)
    """
    if attribute and instance:
        # ── SPECIFIC QUERY ─────────────────────────────────
        path = f"{entity_name}.{fact}.{instance}.{attribute}"

        result = db.execute(
            text("""
                SELECT
                    ev.value,
                    ev.type,
                    ev.path_name::text AS path_name
                FROM entity_value ev
                WHERE ev.path_name = CAST(:path AS ltree)
            """),
            {"path": path},
        ).fetchone()

        if result is None:
            return {"query_type": "specific", "found": False, "data": None}

        return {
            "query_type": "specific",
            "found": True,
            "data": {
                "value": result.value,
                "type": result.type,
                "path_name": result.path_name,
            },
        }

    else:
        # ── BROAD QUERY ────────────────────────────────────
        # Build prefix based on what we know
        if instance:
            # e.g. bank.loan.home_loan — all details of one product
            path_prefix = f"{entity_name}.{fact}.{instance}"
        else:
            # e.g. bank.loan — all products in a category
            path_prefix = f"{entity_name}.{fact}"

        results = db.execute(
            text("""
                SELECT
                    ev.path_name::text AS path_name,
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

        if not results:
            return {"query_type": "broad", "found": False, "data": []}

        return {
            "query_type": "broad",
            "found": True,
            "data": [
                {
                    "path_name": row.path_name,
                    "attribute": row.attribute,
                    "value": row.value,
                    "type": row.type,
                }
                for row in results
            ],
        }