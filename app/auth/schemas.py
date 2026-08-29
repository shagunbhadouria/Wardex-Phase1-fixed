"""Pydantic schemas for auth routes, matching Blueprint v2 Section 2.4."""

from typing import Optional

from pydantic import BaseModel


class GoogleAuthRequest(BaseModel):
    """Request body for POST /auth/google."""

    code: str


class RefreshTokenRequest(BaseModel):
    """Request body for POST /auth/refresh."""

    refresh_token: str


class UserSummary(BaseModel):
    """Minimal user info returned alongside auth tokens."""

    id: str
    email: str
    role: str


class TokenResponse(BaseModel):
    """Response payload for both /auth/google and /auth/refresh."""

    token: str
    refresh_token: str
    user: Optional[UserSummary] = None
