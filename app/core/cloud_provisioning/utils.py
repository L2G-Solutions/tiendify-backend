def build_database_url(host: str, username: str, password: str) -> str:
    return f"postgresql://{username}:{password}@{host}"
