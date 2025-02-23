import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import { verifyToken } from "./services/authServices";

export async function middleware(req: NextRequest) {
    const token = req.cookies.get("jwt")?.value;

    console.log(`Middleware running for: ${req.nextUrl.pathname}`);
    console.log(`JWT Token: ${token ? "[Present]" : "[Missing]"}`);
    console.log(`Token = ${token ?? "Null"}`);

    const protectedRoutes = ["/dashboard", "/budgets", "/transactions", "/insights", "/settings"];
    const isProtected = protectedRoutes.some((route) => req.nextUrl.pathname.startsWith(route));

    if (isProtected) {
        if (!token) {
            console.warn("No JWT token found. Redirecting to login.");
            return NextResponse.redirect(new URL("/login", req.url));
        }

        try {
            const response = await verifyToken(token); // ✅ Ensure token is valid

            if (!response?.user_id) {
                console.warn("JWT invalid, redirecting to login.");
                return NextResponse.redirect(new URL("/login", req.url));
            }

            console.log("JWT verified, granting access.");
        } catch (error) {
            console.error("Error verifying JWT:", error);
            return NextResponse.redirect(new URL("/login", req.url));
        }
    }

    return NextResponse.next(); // ✅ Allow request to proceed
}
