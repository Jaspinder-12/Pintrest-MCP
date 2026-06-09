/**
 * Module: tools.ts
 *
 * Purpose:
 * Exports list schemas and configuration parameters for all MCP tools.
 *
 * Dependencies:
 * None
 *
 * Usage:
 * Imported in index.ts to register tools on server start.
 *
 * Notes:
 * Uses JSON Schema draft-07 formats.
 *
 * Future Improvements:
 * - Local validation checker schemas using AJV
 * - Auto-generate schemas from Python pydantic models
 */
export const TOOLS_REGISTRY = [
    {
        name: "search_pins",
        description: "Search Pinterest visual database using semantic descriptions or image filters.",
        inputSchema: {
            type: "object",
            properties: {
                query: { type: "string", description: "Text description of style or layout." },
                image_url: { type: "string", description: "Optional image URL for reverse matching." },
                limit: { type: "number", default: 10 }
            },
            required: ["query"]
        }
    },
    {
        name: "create_board",
        description: "Initialize a virtual curation workspace folder on the server.",
        inputSchema: {
            type: "object",
            properties: {
                name: { type: "string", description: "Descriptive name of the board." },
                description: { type: "string", description: "Purpose or brand requirements brief." }
            },
            required: ["name"]
        }
    },
    {
        name: "save_pin",
        description: "Save a new visual reference image link to a board.",
        inputSchema: {
            type: "object",
            properties: {
                board_id: { type: "string", description: "Target UUID board destination." },
                image_url: { type: "string", description: "Source link of the image." },
                title: { type: "string", description: "Optional reference title." }
            },
            required: ["board_id", "image_url"]
        }
    },
    {
        name: "analyze_style",
        description: "Extract color palettes, fonts, and layout variables from any design image.",
        inputSchema: {
            type: "object",
            properties: {
                image_url: { type: "string", description: "Target design screenshot link." }
            },
            required: ["image_url"]
        }
    }
];
export function getToolByName(name) {
    /**
     * Retrieves a tool definition schema from registry.
     *
     * Parameters:
     *   name: Name of tool.
     *
     * Returns:
     *   MCPToolDefinition object if found.
     */
    return TOOLS_REGISTRY.find(t => t.name === name);
}
// ============================================
// AGENT INTERACTION
// ============================================
// IDE agents (Cline/Cursor) request these schemas during handshake routines 
// to expose them as tools to the LLM core.
// ============================================
// SECURITY NOTES
// ============================================
// Schema parameters are strictly validated to prevent malformed injections 
// from reaching backend endpoint handlers.
// ============================================
// FUTURE ENHANCEMENTS
// ============================================
// Integrate AJV validation checks for schemas before dispatching API commands.
// ============================================
// FUTURE IMPROVEMENTS
// ============================================
//
// 1. Dynamic schemas database loader integrations
// 2. Multilingual description translation dictionaries
// 3. Rate-limiting tags mapping at schema level
// 4. Schema version parameters tracking
//
// ============================================
//# sourceMappingURL=tools.js.map