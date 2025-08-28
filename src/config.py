import os
from typing import Dict, Any

class Config:
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # File upload settings
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB
    ALLOWED_EXTENSIONS = {'.json', '.yml', '.yaml', '.md'}
    
    # Analysis settings
    MAX_CONCURRENT_ANALYSES = int(os.getenv('MAX_CONCURRENT_ANALYSES', 5))
    ANALYSIS_TIMEOUT = int(os.getenv('ANALYSIS_TIMEOUT', 300))  # 5 minutes
    
    @classmethod
    def get_settings(cls) -> Dict[str, Any]:
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'cors_origins': cls.CORS_ORIGINS,
            'max_file_size': cls.MAX_FILE_SIZE,
            'allowed_extensions': cls.ALLOWED_EXTENSIONS
        }