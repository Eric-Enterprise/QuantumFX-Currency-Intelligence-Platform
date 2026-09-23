# Security and privacy

The current desktop release is version 2.2.1. There is no guaranteed support period or automatic updater.

The application makes read-only HTTPS requests to api.frankfurter.dev. Certificates are verified using Python's standard TLS configuration. Conversion amounts, fees, and history are not sent through rate requests.

Cache files are parsed as JSON, structurally validated, and replaced atomically. Local files are never executed as code. CSV exports neutralize leading formula characters. Local data is not encrypted and can be read by other processes running with the user's permissions. Error logs have size limits.

When reporting an issue, do not publish personal conversion history without reviewing it. The application version, a description of the problem, and sanitized log excerpts are usually sufficient. Do not share access to your computer or data folder.

The EXE is not digitally signed. Published SHA256 checksums verify file integrity; they do not replace a publisher signature.
