"use client";

import { useRouter } from "next/navigation";
import { createContext, ReactNode, useEffect, useMemo, useState } from "react";
import { handleLogin, handleLogout, handleVerifyToken } from "../lib/auth";
import { User } from "../services/authServices";

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const router = useRouter();

    // Check authentication state on app load
    useEffect(() => {
        const checkAuth = async () => {
            await handleVerifyToken(setUser, setIsAuthenticated);
        };
        checkAuth();
    }, []);

    // Use `useMemo` to prevent re-creation of the context value
    const contextValue = useMemo(
        () => ({
            user,
            isAuthenticated,
            login: (email: string, password: string) =>
                handleLogin(email, password, setUser, setIsAuthenticated, router),
            logout: () => handleLogout(setUser, setIsAuthenticated, router),
        }),
        [user, isAuthenticated, router]
    );

    return <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>;
};
