"use client";

import { createContext, ReactNode, useEffect, useMemo, useState } from "react";
import { login, logout, verifyTokenClient } from "../services/authServices";

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
            if (!response?.success) {
                console.error("Login failed:", response?.message);
                setUser(null);
                setIsAuthenticated(false);
                return false;
            }

            setUser({ user_id: response.user_id as string });
            setIsAuthenticated(true);
            return true;
        } catch (error) {
            console.error("Login error:", error);
            return false;
        }
    };

    const handleLogout = async () => {
        try {
            const success = await logout();
            if (!success) {
                console.error("Logout failed");
                return;
            }
            setUser(null);
            setIsAuthenticated(false);
        } catch (error) {
            console.error("Logout error:", error);
        }
    };

    // Rehydrate the AuthContext on mount
    useEffect(() => {
        const checkAuthStatus = async () => {
            try {
                const response = await verifyTokenClient();
                if (response?.success && response?.user_id) {
                    setUser({ user_id: response.user_id });
                    setIsAuthenticated(true);
                } else {
                    console.error("Auth rehydration failed:", response?.message);
                    setUser(null);
                    setIsAuthenticated(false);
                }
            } catch (error) {
                console.error("Failed to rehydrate auth:", error);
                setUser(null);
                setIsAuthenticated(false);
            }
        };

        checkAuthStatus();
    }, []);

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
