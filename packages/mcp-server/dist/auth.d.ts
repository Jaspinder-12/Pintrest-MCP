/**
 * Module: auth.ts
 *
 * Purpose:
 * Validates agent session authorization tokens.
 *
 * Dependencies:
 * - axios
 *
 * Usage:
 * Imported in index.ts to authorize API requests.
 *
 * Notes:
 * Session parameters are cached locally to reduce authentication latency.
 *
 * Future Improvements:
 * - OAuth 2.0 PKCE auth flow integration
 * - Encrypted token cache storage
 */
export interface AgentSession {
    isValid: boolean;
    agentId: string;
    permissions: string[];
}
export declare class Authenticator {
    private coreApiUrl;
    constructor(coreApiUrl: string);
    validateToken(token: string): Promise<AgentSession>;
}
