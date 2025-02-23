import { login as apiLogin, logout as apiLogout } from "../services/authServices";


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

        return true; // ✅ Only return success/failure, middleware will confirm session
    } catch (error) {
        console.error("Login error:", error);
        return false;
    }
};


export const handleLogout = async (): Promise<void> => {
    console.log("auth/handleLogout: Logging out user...");
    await apiLogout(); // ✅ Calls backend logout

    console.log("auth/handleLogout: Logout complete.");
};
