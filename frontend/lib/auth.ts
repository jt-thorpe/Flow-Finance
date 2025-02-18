import { login as apiLogin, logout as apiLogout, verifyToken as apiVerifyToken, User } from "../services/authServices";

// Context update functions
type SetState<T> = (value: T) => void;

// Infer router type dynamically from `useRouter()`
type RouterType = ReturnType<typeof import("next/navigation").useRouter>;


export const handleLogin = async (
    email: string,
    password: string,
    setUser: (user: any) => void,
    setIsAuthenticated: (auth: boolean) => void,
    router: any
): Promise<void> => {
    console.log("Login triggered"); // Debugging

    try {
        const success = await apiLogin(email, password);

        if (!success) throw new Error("Login failed");

        console.log("Login successful, verifying token...");
        setIsAuthenticated(true);

        // Immediately verify token after login (cookies will be sent automatically)
        await handleVerifyToken(setUser, setIsAuthenticated);

        router.push("/dashboard");
    } catch (error) {
        console.error("Login failed:", error);
        throw error;
    }
};


export const handleLogout = async (
    setUser: SetState<User | null>,
    setIsAuthenticated: SetState<boolean>,
    router: RouterType
): Promise<void> => {
    try {
        await apiLogout();
    } catch (error) {
        console.error("Logout failed:", error);
    } finally {
        setUser(null);
        setIsAuthenticated(false);
        router.push("/login");
    }
};


export const handleVerifyToken = async (
    setUser: (user: User | null) => void,
    setIsAuthenticated: (auth: boolean) => void
): Promise<void> => {
    const userData = await apiVerifyToken();

    if (!userData) {
        setUser(null);
        setIsAuthenticated(false);
        return;
    }

    setUser(userData); // Store user details
    setIsAuthenticated(true);
};