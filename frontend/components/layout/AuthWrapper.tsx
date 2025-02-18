"use client";

import { usePathname } from "next/navigation";
import { AuthProvider } from "../../context/AuthContext";

export default function AuthWrapper({ children }: { children: React.ReactNode }) {
    const pathname = usePathname();
    const protectedRoutes = ["/dashboard", "/budgets", "/transactions", "/insights", "/settings"];
    const isProtected = protectedRoutes.some((route) => pathname.startsWith(route));

    return isProtected ? <AuthProvider>{children}</AuthProvider> : <>{children}</>;
}
