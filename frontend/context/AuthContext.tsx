"use client";

import { createContext, ReactNode, useMemo, useState } from "react";
import { login, logout } from "../services/authServices";

interface AuthContextType {
    user: { user_id: string } | null;
    isAuthenticated: boolean;
    login: (email: string, password: string) => void;
    logout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<{ user_id: string } | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    /** ✅ Handles login */
    const handleLogin = async (email: string, password: string): Promise<boolean> => {
        try {
            await login(email, password);
            setUser({ user_id: "authenticated" }); // ✅ Middleware will handle real validation
            setIsAuthenticated(true);
            return true; // ✅ Return success
        } catch (error) {
            console.error("Login error:", error);
            return false; // ✅ Return failure
        }
    };


    /** ✅ Handles logout */
    const handleLogout = async () => {
        await logout();
        setUser(null);
        setIsAuthenticated(false);
    };

    const contextValue = useMemo(() => ({
        user,
        isAuthenticated,
        login: handleLogin,
        logout: handleLogout
    }), [user, isAuthenticated]);

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
};
