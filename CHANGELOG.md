# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-01-XX

### Added
- Initial release of `telegram-init-data` Python library
- Core functionality for validating Telegram Mini App init data
- Support for parsing init data strings into structured Python objects
- Signature validation using HMAC-SHA256 with bot token
- Expiration checking with configurable timeout
- Type definitions for `InitData`, `User`, `Chat`, and other Telegram objects
- Comprehensive error handling with custom exception classes:
  - `TelegramInitDataError` - Base exception class
  - `AuthDateInvalidError` - Invalid or missing auth_date
  - `SignatureInvalidError` - Invalid signature
  - `SignatureMissingError` - Missing signature/hash
  - `ExpiredError` - Init data has expired
- Functions for working with init data:
  - `validate()` - Validate init data (throws exceptions)
  - `is_valid()` - Check validity (returns boolean)
  - `parse()` - Parse init data string to structured object
  - `sign()` - Sign init data for testing/development
  - `hash_token()` - Generate HMAC key from bot token
  - `sign_data()` - Create HMAC-SHA256 signature
- 3rd party validation support:
  - `validate3rd()` - Validate using bot ID and custom verification function
  - `is_valid3rd()` - Check 3rd party validity (returns boolean)
- FastAPI integration with multiple authentication methods:
  - `TelegramInitDataAuth` - Authorization header authentication
  - `TelegramInitDataBearer` - Bearer token authentication
  - `create_init_data_dependency()` - Custom header dependency
  - `create_optional_init_data_dependency()` - Optional validation dependency
  - `get_telegram_auth()` - Quick setup utility function
- Comprehensive test suite with 100% code coverage
- Full type hints and mypy compatibility
- Support for Python 3.8+ 
- MIT license
- Detailed documentation and examples

### Features
- **Validation**: Verify signature and expiration of Telegram Mini App init data
- **Parsing**: Convert URL-encoded init data to structured Python objects  
- **Signing**: Create signed init data for testing and development
- **Type Safety**: Full type hints and validation for all data structures
- **FastAPI Integration**: Ready-to-use middleware and dependencies
- **3rd Party Support**: Validate data signed by Telegram directly
- **Flexible Configuration**: Customizable expiration times and validation options
- **Error Handling**: Comprehensive exception hierarchy for different failure modes

### Technical Details
- Compatible with [@telegram-apps/init-data-node](https://docs.telegram-mini-apps.com/packages/telegram-apps-init-data-node/2-x) Node.js package
- Uses HMAC-SHA256 for signature validation
- Supports all Telegram Mini App init data fields
- Follows Telegram's official validation algorithm
- Zero external dependencies (FastAPI is optional)
- Comprehensive test coverage with pytest
- Code formatting with black and isort
- Type checking with mypy
- Linting with flake8

[Unreleased]: https://github.com/telegram-init-data/telegram-init-data-python/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/telegram-init-data/telegram-init-data-python/releases/tag/v1.0.0 