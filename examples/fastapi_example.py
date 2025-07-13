#!/usr/bin/env python3
"""
FastAPI integration example for telegram-init-data library.

This example demonstrates how to integrate the library with FastAPI
for authentication and authorization in Telegram Mini Apps.

To run this example:
1. pip install fastapi uvicorn
2. Replace YOUR_BOT_TOKEN with your actual bot token
3. python examples/fastapi_example.py
4. Open http://localhost:8000/docs to see the API documentation
"""

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional, Dict, Any
import uvicorn

# Import the library
from telegram_init_data import (
    validate,
    parse,
    sign,
    is_valid,
    TelegramInitDataAuth,
    TelegramInitDataBearer,
    create_init_data_dependency,
    create_optional_init_data_dependency,
    get_telegram_auth,
    InitData,
    TelegramInitDataError
)

# Configuration
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token

# Create FastAPI app
app = FastAPI(
    title="Telegram Init Data API",
    description="Example API demonstrating telegram-init-data library integration",
    version="1.0.0"
)

# Method 1: Using TelegramInitDataAuth class (Authorization header)
auth_header = TelegramInitDataAuth(
    bot_token=BOT_TOKEN,
    scheme_name="tma",
    validate_options={"expires_in": 86400}  # 24 hours
)

# Method 2: Using TelegramInitDataBearer class (Bearer token)
auth_bearer = TelegramInitDataBearer(
    bot_token=BOT_TOKEN,
    validate_options={"expires_in": 86400}
)

# Method 3: Using custom header dependency
auth_custom = create_init_data_dependency(
    bot_token=BOT_TOKEN,
    header_name="X-Telegram-Init-Data",
    validate_options={"expires_in": 86400}
)

# Method 4: Optional authentication dependency
auth_optional = create_optional_init_data_dependency(
    bot_token=BOT_TOKEN,
    header_name="X-Telegram-Init-Data"
)

# Method 5: Using utility function
auth_utility = get_telegram_auth(
    bot_token=BOT_TOKEN,
    auth_type="header",
    validate_options={"expires_in": 86400}
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Telegram Init Data API",
        "version": "1.0.0",
        "endpoints": {
            "auth_header": "/me/header",
            "auth_bearer": "/me/bearer", 
            "auth_custom": "/me/custom",
            "auth_optional": "/me/optional",
            "auth_utility": "/me/utility",
            "create_test_data": "/test/create",
            "manual_validation": "/test/validate"
        },
        "documentation": "/docs"
    }


@app.get("/me/header")
async def get_user_header(init_data: InitData = Depends(auth_header)):
    """
    Get current user info using Authorization header.
    
    Send: Authorization: tma <init_data>
    """
    user = init_data.get("user")
    if not user:
        raise HTTPException(status_code=400, detail="User data not found")
    
    return {
        "method": "Authorization header",
        "user": {
            "id": user.get("id"),
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "username": user.get("username"),
            "language_code": user.get("language_code"),
            "is_premium": user.get("is_premium", False)
        },
        "auth_date": init_data.get("auth_date"),
        "query_id": init_data.get("query_id")
    }


@app.get("/me/bearer")
async def get_user_bearer(init_data: InitData = Depends(auth_bearer)):
    """
    Get current user info using Bearer token.
    
    Send: Authorization: Bearer <init_data>
    """
    user = init_data.get("user")
    if not user:
        raise HTTPException(status_code=400, detail="User data not found")
    
    return {
        "method": "Bearer token",
        "user": {
            "id": user.get("id"),
            "first_name": user.get("first_name"),
            "username": user.get("username")
        },
        "auth_date": init_data.get("auth_date")
    }


@app.get("/me/custom")
async def get_user_custom(init_data: InitData = Depends(auth_custom)):
    """
    Get current user info using custom header.
    
    Send: X-Telegram-Init-Data: <init_data>
    """
    user = init_data.get("user")
    if not user:
        raise HTTPException(status_code=400, detail="User data not found")
    
    return {
        "method": "Custom header",
        "user": user,
        "auth_date": init_data.get("auth_date")
    }


@app.get("/me/optional")
async def get_user_optional(init_data: Optional[InitData] = Depends(auth_optional)):
    """
    Get user info with optional authentication.
    
    Send: X-Telegram-Init-Data: <init_data> (optional)
    """
    if init_data:
        user = init_data.get("user")
        return {
            "method": "Optional authentication",
            "authenticated": True,
            "user": user,
            "auth_date": init_data.get("auth_date")
        }
    else:
        return {
            "method": "Optional authentication",
            "authenticated": False,
            "message": "No authentication provided - showing public content"
        }


@app.get("/me/utility")
async def get_user_utility(init_data: InitData = Depends(auth_utility)):
    """
    Get current user info using utility function.
    
    Send: Authorization: tma <init_data>
    """
    user = init_data.get("user")
    if not user:
        raise HTTPException(status_code=400, detail="User data not found")
    
    return {
        "method": "Utility function",
        "user": user,
        "auth_date": init_data.get("auth_date")
    }


@app.post("/test/create")
async def create_test_data():
    """Create test init data for development/testing."""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise HTTPException(
            status_code=400,
            detail="Please set a real bot token to use this endpoint"
        )
    
    # Create sample init data
    test_data = {
        "query_id": "AAHdF6IQAAAAAN0XohDhrOrc",
        "user": {
            "id": 279058397,
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "language_code": "en",
            "is_premium": False
        },
        "auth_date": datetime.now()
    }
    
    # Sign the test data
    signed_data = sign(test_data, BOT_TOKEN, datetime.now())
    
    return {
        "signed_data": signed_data,
        "usage": {
            "header": f"Authorization: tma {signed_data}",
            "bearer": f"Authorization: Bearer {signed_data}",
            "custom": f"X-Telegram-Init-Data: {signed_data}"
        },
        "note": "Use this signed data to test the authentication endpoints"
    }


@app.post("/test/validate")
async def validate_manual(
    init_data: str,
    custom_expires_in: Optional[int] = None
):
    """
    Manually validate init data.
    
    Body: Raw init data string
    Query param: custom_expires_in (optional)
    """
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise HTTPException(
            status_code=400,
            detail="Please set a real bot token to use this endpoint"
        )
    
    options = {}
    if custom_expires_in is not None:
        options["expires_in"] = custom_expires_in
    
    try:
        # Validate the init data
        validate(init_data, BOT_TOKEN, options)
        
        # Parse the init data
        parsed_data = parse(init_data)
        
        return {
            "valid": True,
            "parsed_data": parsed_data,
            "validation_options": options
        }
        
    except TelegramInitDataError as e:
        return JSONResponse(
            status_code=400,
            content={
                "valid": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "library": "telegram-init-data"
    }


# Custom exception handler
@app.exception_handler(TelegramInitDataError)
async def telegram_init_data_exception_handler(request, exc):
    """Handle telegram init data exceptions."""
    return JSONResponse(
        status_code=401,
        content={
            "error": "Authentication failed",
            "detail": str(exc),
            "error_type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    print("🚀 Starting Telegram Init Data API Example")
    print("=" * 50)
    print()
    print("📋 Available endpoints:")
    print("  • GET  /              - API information")
    print("  • GET  /me/header     - Auth via Authorization header")
    print("  • GET  /me/bearer     - Auth via Bearer token")
    print("  • GET  /me/custom     - Auth via custom header")
    print("  • GET  /me/optional   - Optional authentication")
    print("  • GET  /me/utility    - Auth via utility function")
    print("  • POST /test/create   - Create test init data")
    print("  • POST /test/validate - Manual validation")
    print("  • GET  /health        - Health check")
    print()
    print("📖 Documentation: http://localhost:8000/docs")
    print()
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️  Warning: Please replace YOUR_BOT_TOKEN_HERE with your actual bot token")
        print("   Some endpoints will not work without a real token.")
        print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info") 