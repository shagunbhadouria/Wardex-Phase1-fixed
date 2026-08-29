"""Demo database seeding entrypoint — invoked by `make seed`.

TECH DEBT: DATA-001 — not yet implemented. Seeding requires the six
ORM models (services, metric_snapshots, deployments, incidents,
remediations, llm_call_log) and their Alembic migrations, both of
which are Phase 3 deliverables (Blueprint v2 Section 2.3) and do not
exist yet at this point in the build. Per Rule R-07, this must fail
loudly and explain why rather than silently do nothing or pretend to
seed data that was never written.

Fix plan: once Phase 3 lands the six tables, replace the
NotImplementedError below with real inserts — a handful of services,
a few days of metric_snapshots, and a small number of deployments and
incidents, sized for the "dozens of rows" demo corpus described in
Blueprint v2 Section 1.2. Remove this TECH DEBT marker at that point.
"""


def seed_demo_data() -> None:
    """Populates the database with demo data. Not implemented until Phase 3."""
    raise NotImplementedError(
        "seed_demo_data() requires the Phase 3 database schema "
        "(services, metric_snapshots, deployments, incidents, "
        "remediations, llm_call_log), which has not been built yet. "
        "See TECH DEBT: DATA-001 in this file."
    )


if __name__ == "__main__":
    seed_demo_data()
