import { login as apiLogin, logout as apiLogout, verifyTokenClient as apiVerifyTokenClient } from "../services/authServices";


export const handleLogin = async (
    email: string,
    password: string
): Promise<boolean> => {
    console.log("auth/handleLogin : handling login, requesting API call...");

    try {
        const response = await apiLogin(email, password);
        if (!response?.success) {
            console.error("Login failed:", response?.message);
            return false;
        }

        console.log("Login successful. User:", response.user_id);
        return true;
    } catch (error) {
        console.error("Login error:", error);
        return false;
    }
};


export const handleLogout = async (): Promise<boolean> => {
    console.log("auth/handleLogout: Logging out user...");
    
    try {
        const success = await apiLogout();
        if (!success) {
            console.error("auth/handleLogout: Logout failed");
            return false;
        }

        console.log("auth/handleLogout: Logout complete.");
        return true;
    } catch (error) {
        console.error("auth/handleLogout: Error during logout:", error);
        return false;
    }
};


export const handleAuthRefresh = async (): Promise<string | null> => {
    console.log("auth/handleRefresh : handling refresh, calling API...")

    try {
        const response = await apiVerifyTokenClient();
        if (!response?.success || !response?.user_id) {
            console.error("auth/handleRefresh : refresh failed:", response?.message);
            return null;
        }

        console.log("auth/handleRefresh : refresh success");
        return response.user_id;
    } catch (error) {
        console.error("auth.handleAuthRefresh : Error caught", error);
        return null;
    }
}