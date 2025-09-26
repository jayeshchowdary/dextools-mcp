"""
Configuration settings for DEXTools MCP Server
"""

import os
from typing import Dict, Set

# Supported blockchain identifiers
SUPPORTED_CHAINS: Set[str] = {
    "ether", "ethereum", "eth",
    "bsc", "binance-smart-chain", "binance",
    "polygon", "matic",
    "arbitrum", "arbitrum-one",
    "optimism", "op",
    "avalanche", "avax",
    "solana", "sol",
    "base",
    "fantom", "ftm",
    "cronos", "cro",
    "moonbeam", "glmr",
    "moonriver", "movr",
    "harmony", "one",
    "celo",
    "gnosis", "xdai"
}

# Default configuration
DEFAULT_CONFIG: Dict[str, str] = {
    "DEXTOOLS_PLAN": "trial",
    "LOG_LEVEL": "INFO"
}

# Chain ID mappings for common variations
CHAIN_ID_MAPPINGS: Dict[str, str] = {
    "ethereum": "ether",
    "eth": "ether",
    "binance-smart-chain": "bsc",
    "binance": "bsc",
    "matic": "polygon",
    "arbitrum-one": "arbitrum",
    "op": "optimism",
    "avax": "avalanche",
    "sol": "solana",
    "ftm": "fantom",
    "cro": "cronos",
    "glmr": "moonbeam",
    "movr": "moonriver",
    "one": "harmony",
    "xdai": "gnosis"
}

def get_config() -> Dict[str, str]:
    """Get configuration from environment variables."""
    config = DEFAULT_CONFIG.copy()
    
    # Load from environment
    for key in config:
        env_value = os.getenv(key)
        if env_value:
            config[key] = env_value
    
    return config

def normalize_chain_id(chain_id: str) -> str:
    """Normalize chain ID to standard format."""
    chain_id_lower = chain_id.lower()
    
    # Check if it's already in the correct format
    if chain_id_lower in SUPPORTED_CHAINS:
        return chain_id_lower
    
    # Try mapping
    if chain_id_lower in CHAIN_ID_MAPPINGS:
        return CHAIN_ID_MAPPINGS[chain_id_lower]
    
    return chain_id_lower

def is_supported_chain(chain_id: str) -> bool:
    """Check if chain ID is supported."""
    normalized = normalize_chain_id(chain_id)
    return normalized in SUPPORTED_CHAINS
