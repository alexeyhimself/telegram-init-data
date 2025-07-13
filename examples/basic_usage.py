#!/usr/bin/env python3
"""
Basic usage example of telegram-init-data library.

This example demonstrates the core functionality of the library:
- Validating init data
- Parsing init data
- Signing init data
- Error handling
"""

from telegram_init_data import (
    validate,
    parse,
    sign,
    is_valid,
    hash_token,
    sign_data,
    TelegramInitDataError
)
from datetime import datetime
import json


def main():
    """Main example function."""
    print("🚀 Telegram Init Data Python Library - Basic Usage Example")
    print("=" * 60)
    print()
    
    # Your bot token (replace with actual token)
    bot_token = "YOUR_BOT_TOKEN_HERE"
    
    # Example 1: Creating and signing init data
    print("📝 Example 1: Creating and signing init data")
    print("-" * 40)
    
    # Sample init data
    init_data = {
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
    
    # Sign the init data
    signed_data = sign(init_data, bot_token, datetime.now())
    print(f"✅ Signed data: {signed_data[:100]}...")
    print()
    
    # Example 2: Validating init data
    print("🔍 Example 2: Validating init data")
    print("-" * 40)
    
    # Method 1: Using validate() function (throws exceptions)
    try:
        validate(signed_data, bot_token)
        print("✅ Validation successful using validate()")
    except TelegramInitDataError as e:
        print(f"❌ Validation failed: {e}")
    
    # Method 2: Using is_valid() function (returns boolean)
    if is_valid(signed_data, bot_token):
        print("✅ Validation successful using is_valid()")
    else:
        print("❌ Validation failed using is_valid()")
    print()
    
    # Example 3: Parsing init data
    print("📊 Example 3: Parsing init data")
    print("-" * 40)
    
    parsed_data = parse(signed_data)
    print("Parsed data structure:")
    print(json.dumps(parsed_data, indent=2, default=str))
    print()
    
    # Example 4: Working with individual components
    print("🔧 Example 4: Working with individual components")
    print("-" * 40)
    
    # Hash token
    hashed_token = hash_token(bot_token)
    print(f"Token hash: {hashed_token.hex()[:32]}...")
    
    # Sign data manually
    check_string = "auth_date=1234567890\nquery_id=test"
    signature = sign_data(check_string, bot_token)
    print(f"Manual signature: {signature[:32]}...")
    print()
    
    # Example 5: Error handling
    print("⚠️  Example 5: Error handling")
    print("-" * 40)
    
    # Test with invalid data
    invalid_data = "invalid_init_data"
    
    try:
        validate(invalid_data, bot_token)
        print("This shouldn't print")
    except TelegramInitDataError as e:
        print(f"✅ Caught expected error: {type(e).__name__}: {e}")
    
    # Test with boolean result
    if not is_valid(invalid_data, bot_token):
        print("✅ is_valid() correctly returned False for invalid data")
    print()
    
    # Example 6: Custom validation options
    print("⚙️  Example 6: Custom validation options")
    print("-" * 40)
    
    # Create init data with custom expiration
    options = {"expires_in": 3600}  # 1 hour instead of default 24 hours
    
    try:
        validate(signed_data, bot_token, options)
        print("✅ Validation with custom options successful")
    except TelegramInitDataError as e:
        print(f"❌ Validation with custom options failed: {e}")
    
    # Disable expiration check
    options_no_expire = {"expires_in": 0}
    try:
        validate(signed_data, bot_token, options_no_expire)
        print("✅ Validation with no expiration check successful")
    except TelegramInitDataError as e:
        print(f"❌ Validation with no expiration check failed: {e}")
    print()
    
    print("✨ All examples completed successfully!")
    print()
    print("💡 Next steps:")
    print("   - Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token")
    print("   - Check out the FastAPI integration examples")
    print("   - Read the full documentation in README.md")


if __name__ == "__main__":
    main() 