#!/bin/bash

# DEXTools MCP Server Startup Script
# This script sets the environment variables and starts the MCP server

echo "🚀 Starting DEXTools MCP Server..."

# Set environment variables
export DEXTOOLS_API_KEY="HWG6hhDVfe558Bb7rQpgp3uiDzzbfCCg4rCvXCb0"
export DEXTOOLS_PLAN="trial"

# Verify environment variables
echo "✅ Environment variables set:"
echo "   API Key: $(if [ -n "$DEXTOOLS_API_KEY" ]; then echo "SET"; else echo "NOT SET"; fi)"
echo "   Plan: $DEXTOOLS_PLAN"

# Start the MCP server
echo "🔧 Starting MCP server..."
python dextools_mcp.py
