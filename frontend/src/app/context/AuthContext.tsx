'use client';

import { usePathname } from "next/navigation";
import { createContext, useContext, useEffect, useMemo, useState } from "react";

interface AuthContextType {
    isAuthenticated: boolean | null;
    loading: boolean;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
    isAuthenticated: null,
    loading: true,
    logout: () => { }
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const pathname = usePathname();
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let isMounted = true;

        if (pathname === "/") {
            setIsAuthenticated(null);
            setLoading(false);
            return;
        }

        const fetchAuthStatus = async () => {
            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/verify`, {
                    method: "GET",
                    credentials: "include",
                });

                if (!response.ok) {
                    if (isMounted) setIsAuthenticated(false);
                } else {
                    const data = await response.json();
                    if (isMounted) setIsAuthenticated(data.auth === true);
                }
            } catch (error) {
                if (isMounted) setIsAuthenticated(false);
            } finally {
                if (isMounted) {
                    console.log("Auth check complete. Setting loading to false.");
                    setLoading(false); // ✅ Ensure this runs
                }
            }
        };

        fetchAuthStatus();

        return () => {
            isMounted = false;
        };
    }, []);




    const logout = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/logout`, {
                method: "POST",
                credentials: "include",
            });

            if (response.ok) {
                setIsAuthenticated(false);
                window.location.href = "/login"; // Force full page reload
            } else {
                console.error("Logout failed");
            }
        } catch (error) {
            console.error("Logout error:", error);
        }
    };

    const authContextValue = useMemo(() => ({
        isAuthenticated,
        loading,
        logout
    }), [isAuthenticated, loading]);

    return (
        <AuthContext.Provider value={authContextValue}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};
