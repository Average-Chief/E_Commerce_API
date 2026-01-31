import os


class Settings:
    # 🔐 Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    JWT_ALGORITHM = "HS256"

    # ⏱ Token expiry (seconds)
    ACCESS_TOKEN_EXPIRE_SECONDS = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 1800)  # 30 minutes
    )

    REFRESH_TOKEN_EXPIRE_SECONDS = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS", 60 * 60 * 24 * 7)  # 7 days
    )

    # 🌍 Environment
    ENV = os.getenv("ENV", "development")
    DEBUG = ENV == "development"


settings = Settings()
