import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import { API_URL } from "../config/api";


export async function middleware(req: NextRequest) {
    const token = req.cookies.get("jwt")?.value; // ✅ Get token from cookies
    const protectedRoutes = ["/dashboard", "/budgets", "/transactions", "/insights", "/settings"];
    const isProtected = protectedRoutes.some((route) => req.nextUrl.pathname.startsWith(route));

    if (isProtected) {
        if (!token) {
            console.log("No token here bitch")
            return NextResponse.redirect(new URL("/login", req.url)); // ✅ Redirect if no token
        }

        try {
            const response = await fetch(`${API_URL}/api/auth/verify`, {
                method: "GET",
                headers: { Authorization: `Bearer ${token}` }, // ✅ Verify token
                cache: "no-store",
            });

            if (!response.ok) {
                return NextResponse.redirect(new URL("/login", req.url)); // ✅ Redirect if token is invalid
            }
        } catch (error) {
            console.error("Token verification failed in middleware:", error);
            return NextResponse.redirect(new URL("/login", req.url));
        }
    }

    return NextResponse.next();
}

export const config = {
    matcher: ["/dashboard/:path*", "/budgets/:path*", "/transactions/:path*", "/insights/:path*", "/settings/:path*"], // ✅ Protect only these routes
};
