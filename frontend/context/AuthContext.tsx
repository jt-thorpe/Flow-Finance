"use client";

import { createContext, ReactNode, useMemo, useState } from "react";
import { login, logout } from "../services/authServices";

interface AuthContextType {
    user: { user_id: string } | null;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<boolean>;
    logout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<{ user_id: string } | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const handleLogin = async (email: string, password: string): Promise<boolean> => {
        try {
            const response = await login(email, password);
            if (!response) {
                setUser(null)
                setIsAuthenticated(false)
                return false
            }
            setUser({ user_id: response.user_id });
            setIsAuthenticated(true);
            return true;
        } catch (error) {
            console.error("Login error:", error);
            return false;
        }
    };

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
