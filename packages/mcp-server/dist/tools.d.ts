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
export interface MCPToolDefinition {
    name: string;
    description: string;
    inputSchema: {
        type: string;
        properties: Record<string, any>;
        required?: string[];
    };
}
export declare const TOOLS_REGISTRY: MCPToolDefinition[];
export declare function getToolByName(name: string): MCPToolDefinition | undefined;
