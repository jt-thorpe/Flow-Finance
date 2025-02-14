/* TODO: Consider SWR caching and if appropriate with Redis on backend */
/* TODO: Look at what optimisations can be made with the authorisation process */

'use client';

import { usePathname, useRouter } from "next/navigation";
import { createContext, useContext, useMemo } from "react";
import useSWR from "swr";

interface AuthContextType {
    isAuthenticated: boolean | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<boolean>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
    isAuthenticated: null,
    loading: true,
    login: async () => false,
    logout: () => { },
});

// Fetch function for SWR (handles authentication checking)
const fetcher = async (url: string) => {
    const res = await fetch(url, { credentials: "include" });

    if (res.status === 401) {
        if (typeof window !== "undefined") {
            window.location.href = "/login"; // Redirect on auth failure
        }
        throw new Error("Unauthorized");
    }

    if (!res.ok) throw new Error("Failed to fetch");
    return res.json();
};

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const router = useRouter();
    const pathname = usePathname();

    const shouldFetchAuth = pathname !== "/login";

    // Only fetch auth if NOT on the login page
    const { data, error, mutate } = useSWR(
        shouldFetchAuth ? `${process.env.NEXT_PUBLIC_API_URL}/api/auth/verify` : null,
        fetcher
    );

    const isAuthenticated = data?.auth ?? null;
    const loading = shouldFetchAuth && !data && !error;

    // Function to handle login
    const login = async (email: string, password: string): Promise<boolean> => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
                credentials: "include",
            });

            if (!response.ok) return false;

            // Re-fetch auth state after successful login
            await mutate();
            router.push("/dashboard");
            return true;
        } catch (error) {
            console.error("Login failed:", error);
            return false;
        }
    };

    // Function to handle logout
    const logout = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/logout`, {
                method: "POST",
                credentials: "include",
            });

            if (response.ok) {
                await mutate(null, false); // Reset auth state
                router.push("/login");
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
        login,
        logout,
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
