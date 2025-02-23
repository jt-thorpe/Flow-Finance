import { API_URL } from "../config/api";


export const login = async (email: string, password: string): Promise<{ user_id: string; expires_at: number } | null> => {
    console.log("authServices/login : calling backend API...");

    const response = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
        credentials: "include",
    });

    if (!response.ok) {
        console.error("authServices/login : Login API error:", await response.json());
        return null;
    }

    const data = await response.json();
    console.log("authServices/login : Login successful, cookies should now be set.", data);
    return { user_id: data.user_id, expires_at: data.expires_at };
};


export const verifyToken = async (token: string): Promise<{ user_id: string } | null> => {
    console.log("authServices/verifyToken: calling backend API...");

    try {
        const response = await fetch(`${API_URL}/api/auth/verify`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `${token}`,
            },
        });

        if (!response.ok) {
            console.warn("authServices/verifyToken: User not authenticated.");
            return null;
        }

        const data = await response.json();
        console.log("authServices/verifyToken: User verified:", data);
        return { user_id: data.user_id };
    } catch (error) {
        console.error("authServices/verifyToken: Error verifying authentication.", error);
        return null;
    }
};


export const logout = async (): Promise<void> => {
    console.log("authServices/logout: Logging out user...");
    await fetch(`${API_URL}/api/auth/logout`, {
        method: "POST",
        credentials: "include",
    });

    console.log("authServices/logout: Logout complete, clearing state...");
};