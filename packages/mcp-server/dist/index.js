/**
 * Module: index.ts
 *
 * Purpose:
 * Core entry point for Node.js MCP Server transport gateway.
 *
 * Dependencies:
 * - @modelcontextprotocol/sdk
 * - axios
 *
 * Usage:
 * Run: node dist/index.js
 *
 * Notes:
 * Uses STDIO transport pipeline for local IDE communication.
 *
 * Future Improvements:
 * - Implement Server-Sent Events (SSE) server options
 * - Dynamic middleware pipelines support
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema, } from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";
import dotenv from "dotenv";
import { TOOLS_REGISTRY } from "./tools.js";
import { Authenticator } from "./auth.js";
// Load local environmental files
dotenv.config();
// ============================================
// PURPOSE
// ============================================
// Binds standard STDIO interface pipelines to the MCP SDK server, processing
// incoming request streams and forwarding commands to the FastAPI endpoint.
// ============================================
// BUSINESS LOGIC
// ============================================
const CORE_API_URL = process.env.CORE_API_URL || "http://localhost:8000";
const API_TOKEN = process.env.API_BEARER_TOKEN || "default_dev_token";
const mcpServer = new Server({
    name: "pinterest-visual-mcp",
    version: "1.0.0",
}, {
    capabilities: {
        tools: {},
    },
});
const authenticator = new Authenticator(CORE_API_URL);
// Registry Tool discovery route handler
mcpServer.setRequestHandler(ListToolsRequestSchema, async () => {
    /**
     * Returns supported tools schemas.
     *
     * Parameters:
     *   None.
     *
     * Returns:
     *   List of supported tools objects.
     */
    return {
        tools: TOOLS_REGISTRY
    };
});
// Tool execution route handler
mcpServer.setRequestHandler(CallToolRequestSchema, async (request) => {
    /**
     * Executes tools functions matching parameters.
     *
     * Parameters:
     *   request: Tool call parameters request schema.
     *
     * Returns:
     *   Tool execution result content JSON.
     */
    const { name, arguments: args } = request.params;
    // Validate agent permissions before execution
    const session = await authenticator.validateToken(API_TOKEN);
    if (!session.isValid) {
        return {
            content: [{ type: "text", text: "Error: Session authorization failed." }],
            isError: true
        };
    }
    try {
        let response;
        switch (name) {
            case "search_pins":
                response = await axios.post(`${CORE_API_URL}/v1/search/pins`, args, {
                    headers: { Authorization: `Bearer ${API_TOKEN}` }
                });
                break;
            case "create_board":
                response = await axios.post(`${CORE_API_URL}/v1/boards`, args, {
                    headers: { Authorization: `Bearer ${API_TOKEN}` }
                });
                break;
            case "save_pin":
                response = await axios.post(`${CORE_API_URL}/v1/pins`, args, {
                    headers: { Authorization: `Bearer ${API_TOKEN}` }
                });
                break;
            case "analyze_style":
                response = await axios.post(`${CORE_API_URL}/v1/analysis/style`, args, {
                    headers: { Authorization: `Bearer ${API_TOKEN}` }
                });
                break;
            default:
                throw new Error(`Tool target '${name}' not implemented.`);
        }
        return {
            content: [{ type: "text", text: JSON.stringify(response.data) }]
        };
    }
    catch (error) {
        const errorMsg = error.response?.data?.detail || error.message;
        return {
            content: [{ type: "text", text: `Error calling tool ${name}: ${errorMsg}` }],
            isError: true
        };
    }
});
async function runServer() {
    /**
     * Launches transport process loop.
     *
     * Parameters:
     *   None.
     *
     * Returns:
     *   None.
     */
    const transport = new StdioServerTransport();
    await mcpServer.connect(transport);
    console.error("Pinterest Visual MCP server loaded successfully on STDIO transport.");
}
runServer().catch(console.error);
// ============================================
// AGENT INTERACTION
// ============================================
// IDE clients boot this process using standard node runners.
// ============================================
// SECURITY NOTES
// ============================================
// Ensure CORE_API_URL uses secure SSL layers in live deployments.
// ============================================
// FUTURE ENHANCEMENTS
// ============================================
// Transition switch statements to dynamically resolved handler registry classes.
// ============================================
// FUTURE IMPROVEMENTS
// ============================================
//
// 1. Switch block refactor to dictionary router mappings
// 2. Add request correlation context IDs tracking
// 3. Enable SSE transport connection options
// 4. Local validation of arguments prior to network dispatch
//
// ============================================
//# sourceMappingURL=index.js.map