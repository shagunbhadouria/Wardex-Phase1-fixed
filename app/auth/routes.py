"""Auth routes (Blueprint v2 Section 2.4).

Phase 2 stubs: accept the locked request/response shape and return the
standard envelope. Real Google OAuth exchange, JWT issuance, and Redis
refresh-token blacklisting are Phase 4 (Auth & Security) — see R-69/R-77.
"""

from fastapi import APIRouter, status

from app.auth.schemas import GoogleAuthRequest, RefreshTokenRequest, TokenResponse
from app.shared.types import ApiResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/google",
    response_model=ApiResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Exchange Google OAuth code for tokens",
)
async def google_auth(payload: GoogleAuthRequest) -> ApiResponse[TokenResponse]:
    """Phase 2 stub — Google OAuth code exchange is wired up in Phase 4."""
    return ApiResponse[TokenResponse](
        success=True,
        data=TokenResponse(
            token="stub-not-issued",
            refresh_token="stub-not-issued",
            user=None,
        ),
    )


@router.post(
    "/refresh",
    response_model=ApiResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Refresh an expired access token",
)
async def refresh_token(payload: RefreshTokenRequest) -> ApiResponse[TokenResponse]:
    """Phase 2 stub — refresh rotation against Redis is wired up in Phase 4."""
    return ApiResponse[TokenResponse](
        success=True,
        data=TokenResponse(
            token="stub-not-issued",
            refresh_token="stub-not-issued",
            user=None,
        ),
    )
