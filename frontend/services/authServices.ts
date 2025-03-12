import { API_URL } from "../config/api";


export const login = async (email: string, password: string): Promise<{ user_id: string; expires_at: number } | null> => {
    console.log("authServices/login : calling backend API...");

    const response = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include"
    });

    if (!response.ok) {
        console.error("authServices/login : Login API error:", await response.json());
        return null;
    }

    const data = await response.json();
    console.log("authServices/login : Login successful, cookies should now be set.", data);
    return { user_id: data.user_id, expires_at: data.expires_at };
};


async function verifyTokenBase(options: { token?: string; client?: boolean } = {}): Promise<{ user_id: string } | null> {
    const url = `${API_URL}/api/auth/verify`;

    // If a token is provided (server context), send it via the Authorization header.
    if (options.token) {
        return await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${options.token}`,
            },
        }).then((res) => res.json());
    }

    // If no token is provided but client flag is true, assume client context
    // so rely on the browser to send the cookie automatically.
    if (options.client) {
        return await fetch(url, {
            method: 'GET',
            credentials: 'include', // Browser will attach the http-only cookie.
        }).then((res) => res.json());
    }

    throw new Error('Token required for server-side verification');
}


// Client wrapper: used on the browser.
export async function verifyTokenClient(): Promise<{ user_id: string } | null> {
    return verifyTokenBase({ client: true });
}


// TODO: Given the other functions here are all called client-side currently
// perhaps I migh want to move his out of here and keep it client-side only
// Server wrapper: used in middleware or other server contexts.
export async function verifyTokenServer(token: string): Promise<{ user_id: string } | null> {
    return verifyTokenBase({ token: token });
}


export const logout = async (): Promise<void> => {
    console.log("authServices/logout: Logging out user...");
    await fetch(`${API_URL}/api/auth/logout`, {
        method: "POST",
        credentials: "include",
    });

    console.log("authServices/logout: Logout complete, clearing state...");
};