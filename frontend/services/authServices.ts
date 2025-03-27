import { API_URL } from "../config/api";

interface AuthResponse {
    success: boolean;
    message: string;
    user_id?: string;
    expires_at?: number;
}

export const login = async (email: string, password: string): Promise<{ user_id: string; expires_at: number } | null> => {
    console.log("authServices/login : calling backend API...");

    const response = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include"
    });

    const data: AuthResponse = await response.json();
    
    if (!response.ok || !data.success) {
        console.error("authServices/login : Login API error:", data.message);
        return null;
    }

    if (!data.user_id || !data.expires_at) {
        console.error("authServices/login : Missing required data in response");
        return null;
    }

    console.log("authServices/login : Login successful, cookies should now be set.", data);
    return { user_id: data.user_id, expires_at: data.expires_at };
};


async function verifyTokenBase(options: { token?: string; client?: boolean } = {}): Promise<{ user_id: string } | null> {
    const url = `${API_URL}/api/auth/verify`;

    // If a token is provided (server context), send it via the Authorization header.
    if (options.token) {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${options.token}`,
            },
        });
        const data: AuthResponse = await response.json();
        
        if (!response.ok || !data.success) {
            console.error("authServices/verifyTokenBase : Verification failed:", data.message);
            return null;
        }

        if (!data.user_id) {
            console.error("authServices/verifyTokenBase : Missing user_id in response");
            return null;
        }

        return { user_id: data.user_id };
    }

    // If no token is provided but client flag is true, assume client context
    // so rely on the browser to send the cookie automatically.
    if (options.client) {
        const response = await fetch(url, {
            method: 'GET',
            credentials: 'include', // Browser will attach the http-only cookie.
        });
        const data: AuthResponse = await response.json();
        
        if (!response.ok || !data.success) {
            console.error("authServices/verifyTokenBase : Verification failed:", data.message);
            return null;
        }

        if (!data.user_id) {
            console.error("authServices/verifyTokenBase : Missing user_id in response");
            return null;
        }

        return { user_id: data.user_id };
    }

    throw new Error('Token required for server-side verification');
}


// Client wrapper: used on the browser.
export async function verifyTokenClient(): Promise<{ user_id: string } | null> {
    return verifyTokenBase({ client: true });
}


// Server wrapper: used in middleware or other server contexts.
export async function verifyTokenServer(token: string): Promise<{ user_id: string } | null> {
    return verifyTokenBase({ token: token });
}


export const logout = async (): Promise<boolean> => {
    console.log("authServices/logout: Logging out user...");
    
    const response = await fetch(`${API_URL}/api/auth/logout`, {
        method: "POST",
        credentials: "include",
    });

    const data: AuthResponse = await response.json();
    
    if (!response.ok || !data.success) {
        console.error("authServices/logout: Logout failed:", data.message);
        return false;
    }

    console.log("authServices/logout: Logout complete, clearing state...");
    return true;
};