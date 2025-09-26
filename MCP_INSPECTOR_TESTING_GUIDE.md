# DEXTools MCP Server - MCP Inspector Testing Guide

## 🎯 Overview

This guide provides step-by-step instructions to test all 20 DEXTools MCP tools using the MCP Inspector. The MCP Inspector is a tool that allows you to interact with MCP servers and test their functionality.

## 📋 Prerequisites

### 1. Install MCP Inspector
```bash
# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Or install locally
npm install @modelcontextprotocol/inspector
```

### 2. Set Up DEXTools MCP Server
```bash
# Navigate to your project directory
cd "/Users/jayeshkumarchowdary/Desktop/dextools mcp"

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your DEXTools API key
```

### 3. Configure Environment Variables
Edit your `.env` file:
```
DEXTOOLS_API_KEY=your_actual_api_key_here
DEXTOOLS_PLAN=trial
```

## 🚀 Step-by-Step Testing Instructions

### Step 1: Start the MCP Server

**Terminal 1 - Start the MCP Server:**
```bash
cd "/Users/jayeshkumarchowdary/Desktop/dextools mcp"
python dextools_mcp.py
```

You should see output like:
```
INFO:__main__:Starting DEXTools MCP Server...
INFO:dextools_mcp:DEXTools API v2 client initialized with plan: trial
```

### Step 2: Start MCP Inspector

**Terminal 2 - Start MCP Inspector:**
```bash
npx @modelcontextprotocol/inspector
```

This will open the MCP Inspector in your browser.

### Step 3: Connect to the MCP Server

In MCP Inspector:
1. Click "Add Server"
2. Enter server details:
   - **Name:** DEXTools MCP
   - **Command:** `python`
   - **Args:** `["dextools_mcp.py"]`
   - **Working Directory:** `/Users/jayeshkumarchowdary/Desktop/dextools mcp`

### Step 4: Test All 20 Tools

## 🧪 Comprehensive Tool Testing Guide

### **All 20 DEXTools MCP Tools**

## 📊 **1. Market Analysis Tools (8 tools)**

### **1.1 Trending & Rankings**

#### Test `get_trending_pools`
**Purpose:** Get currently trending "Hot Pairs" on a blockchain
**Parameters:**
```json
{
  "chain_id": "ether"
}
```
**Expected Result:** List of trending pools with price data

#### Test `get_top_gainers`
**Purpose:** Get tokens with highest positive price changes
**Parameters:**
```json
{
  "chain_id": "ether"
}
```
**Expected Result:** List of top gaining tokens

#### Test `get_top_losers`
**Purpose:** Get tokens with most significant negative price changes
**Parameters:**
```json
{
  "chain_id": "ether"
}
```
**Expected Result:** List of top losing tokens

### **1.2 Pool Analysis**

#### Test `get_pool_details`
**Purpose:** Get comprehensive details for a specific liquidity pool
**Parameters:**
```json
{
  "chain_id": "ether",
  "pool_address": "0x4637ea6ecf7e16c99e67e941ab4d7d52eac7c73d"
}
```
**Expected Result:** Detailed pool metadata

#### Test `get_pool_price`
**Purpose:** Get real-time price information for a token pair
**Parameters:**
```json
{
  "chain_id": "ether",
  "pool_address": "0x4637ea6ecf7e16c99e67e941ab4d7d52eac7c73d"
}
```
**Expected Result:** Price data for the pool

#### Test `get_pool_liquidity`
**Purpose:** Get current liquidity data and TVL for a pool
**Parameters:**
```json
{
  "chain_id": "ether",
  "pool_address": "0x4637ea6ecf7e16c99e67e941ab4d7d52eac7c73d"
}
```
**Expected Result:** Liquidity metrics including TVL

#### Test `get_pool_score`
**Purpose:** Get DEXTools score for a specific pool
**Parameters:**
```json
{
  "chain_id": "ether",
  "pool_address": "0x4637ea6ecf7e16c99e67e941ab4d7d52eac7c73d"
}
```
**Expected Result:** Pool score information

### **1.3 Token Analysis**

#### Test `get_token_details`
**Purpose:** Get detailed information about a specific token
**Parameters:**
```json
{
  "chain_id": "ether",
  "token_address": "0xA0b86a33E6441b8c4C8C0C4A8e4A8e4A8e4A8e4A"
}
```
**Expected Result:** Token metadata

#### Test `get_token_security_audit`
**Purpose:** Get security audit results for a token's smart contract
**Parameters:**
```json
{
  "chain_id": "ether",
  "token_address": "0xA0b86a33E6441b8c4C8C0C4A8e4A8e4A8e4A8e4A"
}
```
**Expected Result:** Security audit flags and details

#### Test `get_token_price`
**Purpose:** Get current price information for a specific token
**Parameters:**
```json
{
  "chain_id": "ether",
  "token_address": "0xA0b86a33E6441b8c4C8C0C4A8e4A8e4A8e4A8e4A"
}
```
**Expected Result:** Token price data

#### Test `get_token_score`
**Purpose:** Get DEXTools score for a specific token
**Parameters:**
```json
{
  "chain_id": "ether",
  "token_address": "0xA0b86a33E6441b8c4C8C0C4A8e4A8e4A8e4A8e4A"
}
```
**Expected Result:** Token score information

#### Test `get_all_pools_for_token`
**Purpose:** Find all liquidity pools associated with a token
**Parameters:**
```json
{
  "chain_id": "ether",
  "token_address": "0xA0b86a33E6441b8c4C8C0C4A8e4A8e4A8e4A8e4A",
  "from_date": "2024-01-01T00:00:00",
  "to_date": "2024-12-31T23:59:59"
}
```
**Expected Result:** List of all pools for the token

### **1.4 Blockchain Information**

#### Test `get_blockchain_info`
**Purpose:** Get blockchain information for a specific chain
**Parameters:**
```json
{
  "chain_id": "ether"
}
```
**Expected Result:** Blockchain information

#### Test `get_supported_blockchains`
**Purpose:** Get list of all supported blockchains
**Parameters:**
```json
{}
```
**Expected Result:** List of supported blockchains

## 🔒 **2. Advanced Security & Trust Analysis (2 tools)**

#### Test `get_pool_liquidity_locks`
**Purpose:** Check for locked liquidity (rug pull protection)
**Parameters:**
```json
{
  "chain_id": "ether",
  "pool_address": "0x4637ea6ecf7e16c99e67e941ab4d7d52eac7c73d"
}
```
**Expected Result:** Liquidity lock information (may be empty - this is normal)

#### Test `get_token_locks`
**Purpose:** Check for locked token allocations (team token locks)
**Parameters:**
```json
{
  "chain_id": "ether",
  "token_address": "0xA0b86a33E6441b8c4C8C0C4A8e4A8e4A8e4A8e4A"
}
```
**Expected Result:** Token lock information (may be empty - this is normal)

## 🔍 **3. New Asset & DEX Discovery (3 tools)**

#### Test `find_new_pools_in_range`
**Purpose:** Discover new liquidity pools within a time window
**Parameters:**
```json
{
  "chain_id": "ether",
  "from_date": "2024-01-01T00:00:00",
  "to_date": "2024-01-02T00:00:00",
  "page": 1,
  "page_size": 100
}
```
**Expected Result:** List of new pools created in the time range

#### Test `find_new_tokens_in_range`
**Purpose:** Find new token contracts within a time window
**Parameters:**
```json
{
  "chain_id": "ether",
  "from_date": "2024-01-01T00:00:00",
  "to_date": "2024-01-02T00:00:00",
  "page": 1,
  "page_size": 100
}
```
**Expected Result:** List of new tokens created in the time range

#### Test `get_dex_list_on_chain`
**Purpose:** Get all DEXs indexed on a specific blockchain
**Parameters:**
```json
{
  "chain_id": "ether",
  "page": 1,
  "page_size": 100
}
```
**Expected Result:** List of all DEXs on the specified chain

## 🏗️ **4. Deep DEX Infrastructure Analysis (1 tool)**

#### Test `get_dex_factory_details`
**Purpose:** Get low-level information about a DEX's factory contract
**Parameters:**
```json
{
  "chain_id": "ether",
  "factory_address": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
}
```
**Expected Result:** Detailed factory contract information

## 🔍 Testing Different Chain IDs

### Supported Chains (80%+ of major blockchains)
Test with these chain IDs:
- `ether` (Ethereum)
- `solana` (Solana)
- `polygon` (Polygon)
- `arbitrum` (Arbitrum)
- `optimism` (Optimism)
- `avalanche` (Avalanche)
- `base` (Base)
- `fantom` (Fantom)
- `cronos` (Cronos)
- `moonbeam` (Moonbeam)
- `celo` (Celo)
- `gnosis` (Gnosis)
- `mantle` (Mantle)
- `scroll` (Scroll)
- `linea` (Linea)
- `metis` (Metis)
- `shibarium` (Shibarium)
- `near` (Near)
- `hedera` (Hedera)
- `tron` (TRON)
- `ton` (Ton)
- `sui` (Sui)
- `aptos` (Aptos)
- `starknet` (Starknet)
- `filecoin` (Filecoin)

### Chain ID Variations
- `ether` or `ethereum` → Use `ether`
- `bsc` or `bnb` → Use `bsc`
- `polygon` or `matic` → Use `polygon`

## ❌ Error Testing

### Test Invalid Chain ID
```json
{
  "chain_id": "invalid_chain"
}
```
**Expected**: Error message about unsupported chain

### Test Invalid Address
```json
{
  "chain_id": "ether",
  "pool_address": "invalid_address"
}
```
**Expected**: Error message about invalid address format

### Test Missing Parameters
```json
{
  "chain_id": "ether"
}
```
**Expected**: Error message about missing required parameters

## 📊 Expected Results Format

### Successful Response
```json
{
  "statusCode": 200,
  "data": {
    // Actual data here
  }
}
```

### Error Response
```json
{
  "error": "Error message describing what went wrong"
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Failed
- Check if the MCP server is running
- Verify the working directory path
- Ensure Python is in PATH

#### 2. API Key Error
- Verify your API key in `.env` file
- Check if the key is valid and has sufficient quota
- Try using `trial` plan if using `pro`

#### 3. Import Errors
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ required)

#### 4. Network Errors
- Check internet connection
- Verify DEXTools API is accessible
- Try different chain IDs

### Debug Mode
Add logging to see detailed error messages:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## ✅ Success Criteria

### All Tests Should Pass If:
- ✅ Server starts without errors
- ✅ All 20 tools are available in MCP Inspector
- ✅ Tools return data or appropriate error messages
- ✅ Different chain IDs work correctly
- ✅ Error handling works for invalid inputs

### Test Results Checklist
- [ ] Market Analysis Tools (8 tools)
- [ ] Security & Trust Analysis (2 tools)
- [ ] Asset & DEX Discovery (3 tools)
- [ ] Infrastructure Analysis (1 tool)
- [ ] Token Pool Discovery (1 tool)
- [ ] Blockchain Info (2 tools)
- [ ] Error handling
- [ ] Multiple chain support

## 🎯 Advanced Testing

### Load Testing
Test multiple tools simultaneously to check performance.

### Chain Coverage
Test tools across different supported chains to verify compatibility.

### Edge Cases
- Very old dates
- Very new dates
- Invalid addresses
- Rate limiting scenarios

## 📝 Test Documentation

Keep track of:
- Which tools work with which chains
- Any errors or limitations discovered
- Performance characteristics
- API quota usage

## 🎉 Completion

Once all tests pass, your DEXTools MCP server is ready for production use!

### Next Steps
- Deploy to your preferred environment
- Set up monitoring and logging
- Configure rate limiting if needed
- Document any chain-specific considerations
