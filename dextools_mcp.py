"""
DEXTools MCP Server
A Model Context Protocol server for accessing DEXTools DeFi market data and analysis.
"""

import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from fastmcp import FastMCP
from dextools_python import DextoolsAPIV2
from config import get_config, normalize_chain_id, is_supported_chain

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DEXToolsMCP:
    """DEXTools MCP Server for DeFi market analysis."""
    
    def __init__(self):
        """Initialize the DEXTools MCP server."""
        config = get_config()
        self.api_key = os.getenv("DEXTOOLS_API_KEY")
        self.plan = config["DEXTOOLS_PLAN"]
        
        if not self.api_key:
            raise ValueError("DEXTOOLS_API_KEY environment variable not set.")
        
        try:
            self.client = DextoolsAPIV2(api_key=self.api_key, plan=self.plan)
            logger.info(f"DEXTools API v2 client initialized with plan: {self.plan}")
        except Exception as e:
            logger.error(f"Failed to initialize DEXTools client: {e}")
            raise
    
    def _validate_chain_id(self, chain_id: str) -> bool:
        """Validate if the chain_id is supported."""
        return is_supported_chain(chain_id)
    
    def _validate_address(self, address: str, chain_id: str = None) -> bool:
        """Validate address format based on blockchain type."""
        if not address or not isinstance(address, str):
            return False
        
        # Normalize chain_id for validation
        if chain_id:
            normalized_chain = normalize_chain_id(chain_id)
        else:
            normalized_chain = None
        
        # Ethereum-style addresses (Ethereum, BSC, Polygon, Arbitrum, Optimism, etc.)
        if normalized_chain in ["ether", "bsc", "polygon", "arbitrum", "optimism", "avalanche", "base", "fantom", "cronos", "moonbeam", "moonriver", "harmony", "celo", "gnosis", "xdai"]:
            return address.startswith("0x") and len(address) == 42
        
        # Solana addresses (base58, 32-44 characters)
        elif normalized_chain == "solana":
            # Solana addresses are base58 encoded, typically 32-44 characters
            # They don't start with "0x" and use base58 alphabet
            import re
            base58_pattern = r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
            return bool(re.match(base58_pattern, address))
        
        # Default validation - try to detect format
        else:
            # If no chain specified, try both formats
            ethereum_format = address.startswith("0x") and len(address) == 42
            solana_format = bool(re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', address)) if 're' in globals() else False
            return ethereum_format or solana_format

# Initialize MCP server
mcp = FastMCP("DEXTools Analysis MCP")
dextools = DEXToolsMCP()

@mcp.tool()
def get_trending_pools(chain_id: str) -> Dict[str, Any]:
    """
    Retrieves the list of 'Hot Pairs' currently trending on a specific blockchain.
    
    Args:
        chain_id: The blockchain identifier (e.g., "ether", "solana", "polygon")
    
    Returns:
        Dictionary containing a list of trending pool objects
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_ranking_hotpools(normalized_chain_id)
        logger.info(f"Retrieved trending pools for chain: {chain_id}")
        return result
    except Exception as e:
        logger.error(f"Error getting trending pools: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_top_gainers(chain_id: str) -> Dict[str, Any]:
    """
    Fetches the tokens with the highest positive price change on a given blockchain.
    
    Args:
        chain_id: The blockchain identifier
    
    Returns:
        Dictionary containing a list of top gainer token objects
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_ranking_gainers(normalized_chain_id)
        logger.info(f"Retrieved top gainers for chain: {chain_id}")
        return result
    except Exception as e:
        logger.error(f"Error getting top gainers: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_top_losers(chain_id: str) -> Dict[str, Any]:
    """
    Fetches the tokens with the most significant negative price change on a given blockchain.
    
    Args:
        chain_id: The blockchain identifier
    
    Returns:
        Dictionary containing a list of top loser token objects
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_ranking_losers(normalized_chain_id)
        logger.info(f"Retrieved top losers for chain: {chain_id}")
        return result
    except Exception as e:
        logger.error(f"Error getting top losers: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_pool_details(chain_id: str, pool_address: str) -> Dict[str, Any]:
    """
    Retrieves comprehensive details for a specific liquidity pool.
    
    Args:
        chain_id: The blockchain identifier
        pool_address: The contract address of the liquidity pool
    
    Returns:
        Dictionary with detailed pool metadata
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(pool_address, chain_id):
            return {"error": f"Invalid pool address format: {pool_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_pool(normalized_chain_id, pool_address)
        logger.info(f"Retrieved pool details for: {pool_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting pool details: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_pool_price(chain_id: str, pool_address: str) -> Dict[str, Any]:
    """
    Gets the real-time price information for a specific token pair.
    
    Args:
        chain_id: The blockchain identifier
        pool_address: The contract address of the liquidity pool
    
    Returns:
        Dictionary with price data
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(pool_address, chain_id):
            return {"error": f"Invalid pool address format: {pool_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_pool_price(normalized_chain_id, pool_address)
        logger.info(f"Retrieved pool price for: {pool_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting pool price: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_pool_liquidity(chain_id: str, pool_address: str) -> Dict[str, Any]:
    """
    Fetches the current liquidity data for a pool, including Total Value Locked (TVL).
    
    Args:
        chain_id: The blockchain identifier
        pool_address: The contract address of the liquidity pool
    
    Returns:
        Dictionary with liquidity metrics
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(pool_address, chain_id):
            return {"error": f"Invalid pool address format: {pool_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_pool_liquidity(normalized_chain_id, pool_address)
        logger.info(f"Retrieved pool liquidity for: {pool_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting pool liquidity: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_token_security_audit(chain_id: str, token_address: str) -> Dict[str, Any]:
    """
    Provides security audit results for a token's smart contract.
    Checks for honeypots, verifies source code, and lists buy/sell taxes.
    
    Args:
        chain_id: The blockchain identifier
        token_address: The contract address of the token
    
    Returns:
        Dictionary with security audit flags and details
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(token_address, chain_id):
            return {"error": f"Invalid token address format: {token_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_token_audit(normalized_chain_id, token_address)
        logger.info(f"Retrieved token audit for: {token_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting token audit: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_token_details(chain_id: str, token_address: str) -> Dict[str, Any]:
    """
    Retrieves detailed information about a specific token.
    
    Args:
        chain_id: The blockchain identifier
        token_address: The contract address of the token
    
    Returns:
        Dictionary with token metadata
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(token_address, chain_id):
            return {"error": f"Invalid token address format: {token_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_token_info(normalized_chain_id, token_address)
        logger.info(f"Retrieved token details for: {token_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting token details: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_all_pools_for_token(chain_id: str, token_address: str, from_date: str = "2024-01-01T00:00:00", to_date: str = "2024-12-31T23:59:59") -> Dict[str, Any]:
    """
    Discovers all liquidity pools (trading pairs) associated with a single token.
    
    Args:
        chain_id: The blockchain identifier
        token_address: The contract address of the token
        from_date: Start date for historical data (default: "2024-01-01T00:00:00")
        to_date: End date for historical data (default: "2024-12-31T23:59:59")
    
    Returns:
        Dictionary containing a list of all pools for the specified token
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(token_address, chain_id):
            return {"error": f"Invalid token address format: {token_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        
        # Use current year as default if not provided
        if not from_date or from_date == "":
            from datetime import datetime
            current_year = datetime.now().year
            from_date = f"{current_year}-01-01T00:00:00"
        
        if not to_date or to_date == "":
            from datetime import datetime
            current_year = datetime.now().year
            to_date = f"{current_year}-12-31T23:59:59"
        
        result = dextools.client.get_token_pools(normalized_chain_id, token_address, from_date, to_date)
        logger.info(f"Retrieved all pools for token: {token_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting token pools: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_pool_score(chain_id: str, pool_address: str) -> Dict[str, Any]:
    """
    Gets the DEXTools score for a specific pool.
    
    Args:
        chain_id: The blockchain identifier
        pool_address: The contract address of the liquidity pool
    
    Returns:
        Dictionary with pool score information
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(pool_address, chain_id):
            return {"error": f"Invalid pool address format: {pool_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_pool_score(normalized_chain_id, pool_address)
        logger.info(f"Retrieved pool score for: {pool_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting pool score: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_token_score(chain_id: str, token_address: str) -> Dict[str, Any]:
    """
    Gets the DEXTools score for a specific token.
    
    Args:
        chain_id: The blockchain identifier
        token_address: The contract address of the token
    
    Returns:
        Dictionary with token score information
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(token_address, chain_id):
            return {"error": f"Invalid token address format: {token_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_token_score(normalized_chain_id, token_address)
        logger.info(f"Retrieved token score for: {token_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting token score: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_token_price(chain_id: str, token_address: str) -> Dict[str, Any]:
    """
    Gets the current price information for a specific token.
    
    Args:
        chain_id: The blockchain identifier
        token_address: The contract address of the token
    
    Returns:
        Dictionary with token price data
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(token_address, chain_id):
            return {"error": f"Invalid token address format: {token_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_token_price(normalized_chain_id, token_address)
        logger.info(f"Retrieved token price for: {token_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting token price: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_blockchain_info(chain_id: str) -> Dict[str, Any]:
    """
    Gets blockchain information for a specific chain.
    
    Args:
        chain_id: The blockchain identifier
    
    Returns:
        Dictionary with blockchain information
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_blockchain(normalized_chain_id)
        logger.info(f"Retrieved blockchain info for: {chain_id}")
        return result
    except Exception as e:
        logger.error(f"Error getting blockchain info: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_supported_blockchains() -> Dict[str, Any]:
    """
    Gets the list of all supported blockchains.
    
    Returns:
        Dictionary with list of supported blockchains
    """
    try:
        result = dextools.client.get_blockchains()
        logger.info("Retrieved supported blockchains")
        return result
    except Exception as e:
        logger.error(f"Error getting supported blockchains: {e}")
        return {"error": str(e)}

# Advanced Security & Trust Analysis Tools

@mcp.tool()
def get_pool_liquidity_locks(chain_id: str, pool_address: str) -> Dict[str, Any]:
    """
    Retrieves detailed information about any locked liquidity for a specific trading pair.
    This is a critical tool for identifying potential "rug pulls," as locked liquidity 
    ensures that developers cannot arbitrarily remove it.
    
    Note: Most pools don't have liquidity locks. Empty data is normal and indicates
    the pool doesn't have locked liquidity, which is common for most DEX pools.
    
    Args:
        chain_id: The blockchain identifier
        pool_address: The contract address of the liquidity pool
    
    Returns:
        Dictionary with detailed liquidity lock information, or message indicating no locks found
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(pool_address, chain_id):
            return {"error": f"Invalid pool address format: {pool_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_pool_locks(normalized_chain_id, pool_address)
        
        # Provide better feedback when no locks are found
        if isinstance(result, dict) and "data" in result:
            if not result["data"]:
                result["message"] = "No liquidity locks found for this pool. This is normal - most pools don't have locked liquidity."
                result["data"] = {
                    "hasLocks": False,
                    "note": "Liquidity locks are a security feature where developers lock their liquidity to prevent 'rug pulls'. Most pools don't have this feature."
                }
        
        logger.info(f"Retrieved pool liquidity locks for: {pool_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting pool liquidity locks: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_token_locks(chain_id: str, token_address: str) -> Dict[str, Any]:
    """
    Fetches information about locked tokens for a specific asset, such as those allocated 
    to the development team or for future rewards. This helps assess the risk of a large 
    token dump on the market.
    
    Note: Most tokens don't have token locks. Empty data is normal and indicates
    the token doesn't have locked allocations, which is common for most tokens.
    
    Args:
        chain_id: The blockchain identifier
        token_address: The contract address of the token
    
    Returns:
        Dictionary with token lock information, or message indicating no locks found
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(token_address, chain_id):
            return {"error": f"Invalid token address format: {token_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_token_locks(normalized_chain_id, token_address)
        
        # Provide better feedback when no locks are found
        if isinstance(result, dict) and "data" in result:
            if not result["data"]:
                result["message"] = "No token locks found for this token. This is normal - most tokens don't have locked allocations."
                result["data"] = {
                    "hasLocks": False,
                    "note": "Token locks are a security feature where team tokens or allocations are locked to prevent market dumps. Most tokens don't have this feature."
                }
        
        logger.info(f"Retrieved token locks for: {token_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting token locks: {e}")
        return {"error": str(e)}

# New Asset & DEX Discovery Tools

@mcp.tool()
def find_new_pools_in_range(chain_id: str, from_date: str = "2024-01-01T00:00:00", to_date: str = "2024-12-31T23:59:59", order: str = "asc", sort: str = "creationTime", page: int = 1, page_size: int = 100) -> Dict[str, Any]:
    """
    Discovers all new liquidity pools created within a specific time window or block range 
    on a given chain. This is perfect for strategies that aim to invest in tokens at the 
    earliest possible moment.
    
    Args:
        chain_id: The blockchain identifier
        from_date: Start date for the search range (format: "YYYY-MM-DDTHH:MM:SS")
        to_date: End date for the search range (format: "YYYY-MM-DDTHH:MM:SS")
        order: Sort order ("asc" or "desc")
        sort: Sort field ("creationTime", "liquidity", "volume", etc.)
        page: Page number for pagination (default: 1)
        page_size: Number of results per page (default: 100)
    
    Returns:
        Dictionary containing a list of new pools created in the specified range
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_pools(normalized_chain_id, from_date, to_date, order, sort, page, page_size)
        logger.info(f"Retrieved new pools for chain: {chain_id} from {from_date} to {to_date}")
        return result
    except Exception as e:
        logger.error(f"Error finding new pools: {e}")
        return {"error": str(e)}

@mcp.tool()
def find_new_tokens_in_range(chain_id: str, from_date: str = "2024-01-01T00:00:00", to_date: str = "2024-12-31T23:59:59", order: str = "asc", sort: str = "socialsInfoUpdated", page: int = 1, page_size: int = 100) -> Dict[str, Any]:
    """
    Finds all new token contracts created within a specified time or block range. 
    This allows for analysis even before a token has liquidity.
    
    Args:
        chain_id: The blockchain identifier
        from_date: Start date for the search range (format: "YYYY-MM-DDTHH:MM:SS")
        to_date: End date for the search range (format: "YYYY-MM-DDTHH:MM:SS")
        order: Sort order ("asc" or "desc")
        sort: Sort field ("socialsInfoUpdated", "creationTime", etc.)
        page: Page number for pagination (default: 1)
        page_size: Number of results per page (default: 100)
    
    Returns:
        Dictionary containing a list of new tokens created in the specified range
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_tokens(normalized_chain_id, from_date, to_date, order, sort, page, page_size)
        logger.info(f"Retrieved new tokens for chain: {chain_id} from {from_date} to {to_date}")
        return result
    except Exception as e:
        logger.error(f"Error finding new tokens: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_dex_list_on_chain(chain_id: str, order: str = "asc", sort: str = "name", page: int = 1, page_size: int = 100) -> Dict[str, Any]:
    """
    Retrieves a complete list of all Decentralized Exchanges (DEXs) indexed by DEXTools 
    on a specific blockchain.
    
    Args:
        chain_id: The blockchain identifier
        order: Sort order ("asc" or "desc")
        sort: Sort field ("name", "creationTime", etc.)
        page: Page number for pagination (default: 1)
        page_size: Number of results per page (default: 100)
    
    Returns:
        Dictionary containing a list of all DEXs on the specified chain
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_dexes(normalized_chain_id, order, sort, page, page_size)
        logger.info(f"Retrieved DEX list for chain: {chain_id}")
        return result
    except Exception as e:
        logger.error(f"Error getting DEX list: {e}")
        return {"error": str(e)}

# Deep DEX Infrastructure Analysis Tools

@mcp.tool()
def get_dex_factory_details(chain_id: str, factory_address: str) -> Dict[str, Any]:
    """
    Provides low-level information about a specific DEX's factory contract, which is the 
    smart contract responsible for creating new trading pairs on that exchange.
    
    Args:
        chain_id: The blockchain identifier
        factory_address: The contract address of the DEX factory
    
    Returns:
        Dictionary with detailed factory contract information
    """
    try:
        if not dextools._validate_chain_id(chain_id):
            return {"error": f"Unsupported chain_id: {chain_id}"}
        
        if not dextools._validate_address(factory_address, chain_id):
            return {"error": f"Invalid factory address format: {factory_address}"}
        
        normalized_chain_id = normalize_chain_id(chain_id)
        result = dextools.client.get_dex_factory_info(normalized_chain_id, factory_address)
        logger.info(f"Retrieved DEX factory details for: {factory_address}")
        return result
    except Exception as e:
        logger.error(f"Error getting DEX factory details: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    logger.info("Starting DEXTools MCP Server...")
    mcp.run()
