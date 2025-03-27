import { login as apiLogin, logout as apiLogout, verifyTokenClient as apiVerifyTokenClient } from "../services/authServices";


export const handleLogin = async (
    email: string,
    password: string
): Promise<boolean> => {
    console.log("auth/handleLogin : handling login, requesting API call...");

    try {
        const data = await apiLogin(email, password);
        if (!data) {
            console.error("Login failed");
            return false;
        }

        console.log("Login successful. User:", data.user_id);

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
        const data = await apiVerifyTokenClient();
        if (!data) {
            console.error("auth/handleRefresh : refresh failed");
            return null
        }

        console.log("auth/handleRefresh : refresh success")
        return data.user_id
    } catch (error) {
        console.error("auth.handleAuthRefresh : Error caught", error)
        return null
    }
}