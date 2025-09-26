# DEXTools MCP Server

A comprehensive Model Context Protocol (MCP) server that provides access to DEXTools DeFi market data and analysis tools. This server offers 20 powerful tools for analyzing cryptocurrency markets, discovering new assets, and performing security audits.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- DEXTools API key (get one at [dextools.io](https://dextools.io))

### Installation

1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   ```bash
   cp env.example .env
   # Edit .env and add your DEXTools API key
   ```

4. **Start the server:**
   ```bash
   python dextools_mcp.py
   ```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with your DEXTools API credentials:

```env
DEXTOOLS_API_KEY=your_api_key_here
DEXTOOLS_PLAN=trial
```

### Supported Plans
- `trial` - Free tier with limited requests
- `pro` - Professional tier with higher limits
- `enterprise` - Enterprise tier with maximum access

## 📊 Available Tools

The server provides 20 tools organized into 4 categories:

### 1. Market Analysis Tools (8 tools)

#### Trending & Rankings
- **`get_trending_pools`** - Get currently trending "Hot Pairs" on any blockchain
- **`get_top_gainers`** - Find tokens with highest positive price changes
- **`get_top_losers`** - Find tokens with most significant negative price changes

#### Pool Analysis
- **`get_pool_details`** - Get comprehensive details for a specific liquidity pool
- **`get_pool_price`** - Get real-time price information for a token pair
- **`get_pool_liquidity`** - Get current liquidity data and TVL for a pool
- **`get_pool_score`** - Get DEXTools score for a specific pool

#### Token Analysis
- **`get_token_details`** - Get detailed information about a specific token
- **`get_token_price`** - Get current price information for a token
- **`get_token_score`** - Get DEXTools score for a specific token
- **`get_token_security_audit`** - Get security audit results for a token's smart contract

#### Blockchain Information
- **`get_blockchain_info`** - Get blockchain information for a specific chain
- **`get_supported_blockchains`** - Get list of all supported blockchains

### 2. Advanced Security & Trust Analysis (2 tools)

- **`get_pool_liquidity_locks`** - Check for locked liquidity (rug pull protection)
- **`get_token_locks`** - Check for locked token allocations (team token locks)

### 3. New Asset & DEX Discovery (3 tools)

- **`find_new_pools_in_range`** - Discover new liquidity pools within a time window
- **`find_new_tokens_in_range`** - Find new token contracts within a time window
- **`get_dex_list_on_chain`** - Get all DEXs indexed on a specific blockchain

### 4. Deep DEX Infrastructure Analysis (1 tool)

- **`get_dex_factory_details`** - Get low-level information about a DEX's factory contract

### 5. Token Pool Discovery (1 tool)

- **`get_all_pools_for_token`** - Find all liquidity pools associated with a token

## 🌐 Supported Blockchains

The server supports 80%+ of major blockchains (tested with 24+ chains from a list of 98):

### **✅ Fully Supported Chains:**
- **Ethereum** (`ether`)
- **Solana** (`solana`)
- **Polygon** (`polygon`)
- **Arbitrum** (`arbitrum`)
- **Optimism** (`optimism`)
- **Avalanche** (`avalanche`)
- **Base** (`base`)
- **Fantom** (`fantom`)
- **Cronos** (`cronos`)
- **Moonbeam** (`moonbeam`)
- **Moonriver** (`moonriver`)
- **Harmony** (`harmony`)
- **Celo** (`celo`)
- **Gnosis** (`gnosis`)
- **Mantle** (`mantle`)
- **Scroll** (`scroll`)
- **Linea** (`linea`)
- **Metis** (`metis`)
- **Shibarium** (`shibarium`)
- **Near** (`near`)
- **Hedera** (`hedera`)
- **TRON** (`tron`)
- **Ton** (`ton`)
- **Sui** (`sui`)
- **Aptos** (`aptos`)
- **Starknet** (`starknet`)
- **Filecoin** (`filecoin`)
- **Binance Smart Chain** (`bsc`)
- **Aurora** (`aurora`)
- **Bitrock** (`bitrock`)
- **Blast** (`blast`)
- **Berachain** (`berachain`)
- **Bitlayer** (`bitlayer`)
- **Apechain** (`apechain`)
- **BitTorrent** (`bittorrent`)
- **Canto** (`canto`)
- **Boba** (`boba`)
- **Alvey** (`alvey`)
- **Abstract** (`abstract`)
- **Bitgert** (`bitgert`)
- **Avax DFK** (`dfk`)

### **❌ Not Supported:**
- KCC, MultiversX, Cardano, Algorand, Cosmos, Osmosis, and a few others

**Note:** The `get_supported_blockchains` tool only shows a subset of actually supported chains. Most major blockchains work even if not listed in the API response.

## 🔍 Usage Examples

### Basic Market Analysis
```python
# Get trending pools on Ethereum
get_trending_pools(chain_id="ether")

# Get top gainers on Solana
get_top_gainers(chain_id="solana")

# Get pool details for a specific address
get_pool_details(chain_id="ether", pool_address="0x...")
```

### Security Analysis
```python
# Check for liquidity locks (rug pull protection)
get_pool_liquidity_locks(chain_id="ether", pool_address="0x...")

# Check for token locks (team allocation locks)
get_token_locks(chain_id="ether", token_address="0x...")

# Run security audit on a token
get_token_security_audit(chain_id="ether", token_address="0x...")
```

### Discovery & Research
```python
# Find new pools created in the last 24 hours
find_new_pools_in_range(
    chain_id="ether",
    from_date="2024-01-01T00:00:00",
    to_date="2024-01-02T00:00:00"
)

# Find all pools for a specific token
get_all_pools_for_token(
    chain_id="ether",
    token_address="0x...",
    from_date="2024-01-01T00:00:00",
    to_date="2024-12-31T23:59:59"
)
```

## 🛠️ Running the Server

### Method 1: Direct Python
```bash
python dextools_mcp.py
```

### Method 2: Using the Start Script
```bash
chmod +x start_mcp.sh
./start_mcp.sh
```

### Method 3: With Environment Variables
```bash
export DEXTOOLS_API_KEY=your_api_key_here
export DEXTOOLS_PLAN=trial
python dextools_mcp.py
```

## 🧪 Testing with MCP Inspector

For detailed testing instructions, see the [MCP Inspector Testing Guide](MCP_INSPECTOR_TESTING_GUIDE.md).

### Quick Start:
1. **Install MCP Inspector:**
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

2. **Start the MCP server:**
   ```bash
   python dextools_mcp.py
   ```

3. **Connect MCP Inspector:**
   - Open MCP Inspector
   - Add new server with:
     - **Name:** DEXTools MCP
     - **Command:** `python`
     - **Args:** `["dextools_mcp.py"]`
     - **Working Directory:** `/path/to/your/project`

4. **Test the tools:**
   - Try `get_supported_blockchains()` first
   - Test `get_trending_pools(chain_id="ether")`
   - Explore other tools as needed

## 📝 Important Notes

### Address Formats
- **Ethereum-style addresses:** Start with `0x`, 42 characters long
- **Solana addresses:** Base58 encoded, 32-44 characters long

### Date Formats
- Use ISO 8601 format: `"YYYY-MM-DDTHH:MM:SS"`
- Example: `"2024-01-01T00:00:00"`

### Pagination
- `page`: Page number (default: 1)
- `page_size`: Results per page (default: 100)

### Empty Data Responses
Some tools may return empty data, which is normal:
- **Liquidity locks:** Most pools don't have locked liquidity
- **Token locks:** Most tokens don't have locked allocations
- **New assets:** May be empty if no new assets in the time range

## 🔧 Troubleshooting

### Common Issues

1. **"Forbidden" errors:**
   - Check your API key is correct
   - Verify your plan has sufficient quota
   - Try using `trial` plan if using `pro`

2. **"Invalid address format" errors:**
   - Ensure addresses match the blockchain format
   - Ethereum: `0x...` (42 characters)
   - Solana: Base58 (32-44 characters)

3. **"Input validation error" errors:**
   - Don't leave required parameters empty
   - Use proper date formats
   - Check parameter types

4. **Empty data responses:**
   - This is normal for many tools
   - Try different time ranges
   - Use different addresses

### Getting Help

- Check the [DEXTools API documentation](https://docs.dextools.io)
- Verify your API key and plan
- Test with known working addresses
- Check the server logs for detailed error messages

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Happy DeFi Analysis! 🚀**