import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import { verifyTokenServer } from "./services/authServices";


export const config = {
    matcher: [
        '/dashboard/:path*',
        '/budgets/:path*',
        '/transactions/:path*',
        '/insights/:path*',
        '/settings/:path*'
    ],
};

export async function middleware(req: NextRequest) {
    const token = req.cookies.get("jwt")?.value;

    console.log(`middleware.ts : Running for: ${req.nextUrl.pathname}`);
    console.log(`middleware.ts : JWT is ${token ? "[Present]" : "[Missing]"}`);
    console.log(`middleware.ts : JWT = ${token ?? "Null"}`);

    if (!token) {
        console.warn("middleware.ts : No JWT found. Redirecting.");
        return NextResponse.redirect(new URL("/login", req.url));
    }

    try {
        console.log("middleware.ts : API call to verify JWT.")
        const response = await verifyTokenServer(token);

        if (!response?.user_id) {
            console.warn("middleware.ts : JWT is invalid.");
            return NextResponse.redirect(new URL("/login", req.url));
        }

        console.log("middleware.ts : Success. JWT is authentic.");
    } catch (error) {
        console.error("middleware.ts : Error caught when attempting to verify JWT.", error);
        return NextResponse.redirect(new URL("/login", req.url));
    }

    return NextResponse.next();
}