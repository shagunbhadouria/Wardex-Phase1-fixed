"""Tests for the DB connection/session factory (Rule R-44, R-17).

Scope note: this tests the Phase 2 skeleton (engine, session factory,
get_db dependency) — not the schema. No tables or models exist yet
(Phase 3, Blueprint v2 Section 2.3), so these tests only prove the
connection plumbing itself works against a real Postgres instance.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine, get_db


def test_engine_connects_to_database() -> None:
    """Verifies the configured engine can open a real connection and run a query."""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_get_db_yields_a_working_session_and_closes_it() -> None:
    """Verifies get_db() yields a usable Session and closes it after use."""
    gen = get_db()
    db = next(gen)
    assert isinstance(db, Session)
    assert db.execute(text("SELECT 1")).scalar() == 1

    # Exhaust the generator — this is what FastAPI's Depends() teardown
    # does on every request, and it's what triggers the `finally:
    # db.close()` branch. If close() ever raised, this would fail here.
    close_exception = None
    try:
        next(gen)
    except StopIteration:
        pass
    except Exception as exc:  # pragma: no cover - only fires on a real bug
        close_exception = exc
    assert close_exception is None
