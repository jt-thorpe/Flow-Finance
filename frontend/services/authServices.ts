import { API_URL } from "../config/api";


export const login = async (email: string, password: string): Promise<boolean> => {
    console.log("Attempting API call to login"); // Debugging

    const response = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
        console.error("Login API error:", await response.json()); // Debugging
        return false;
    }

    console.log("Login successful, cookies should now be set.");
    return true;
};


export const logout = async (): Promise<void> => {
    await fetch(`${API_URL}/api/auth/logout`, {
        method: "POST",
        credentials: "include",
    });
};


export interface User {
    user_id: string;
}

export const verifyToken = async (): Promise<User | null> => {
    console.log("Attempting to verify token..."); // Debugging

    const response = await fetch(`${API_URL}/api/auth/verify`, {
        method: "GET",
        credentials: "include",
    });

    if (!response.ok) {
        console.warn("Token verification failed:", await response.json()); // Debugging
        return null;  // Bad token
    }

    return response.json();
};
