'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
    const router = useRouter();
    const { isAuthenticated, loading } = useAuth();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        let hasNavigated = false;

        if (isAuthenticated && !hasNavigated) {
            hasNavigated = true;
            router.push("/dashboard");
        }
    }, [isAuthenticated]);


    const handleLogin = async (event: React.FormEvent) => {
        event.preventDefault();

        if (!email || !password) {
            setError('Please provide your email and password.');
            return;
        }

        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
            credentials: "include",
        });

        if (response.ok) {
            console.log("Login successful. Redirecting to dashboard...");
            router.push('/dashboard'); // Redirect first

            // Force reloading the auth state
            setTimeout(() => {
                window.location.reload(); // Reload ensures `AuthContext` verifies the session
            }, 500);
        } else {
            setError('Invalid credentials, please try again.');
        }
    };



    return (
        <main className="flex flex-col items-center justify-center min-h-screen px-4 py-8 bg-gray-100">
            <section className="bg-white shadow-md rounded-2xl p-8 max-w-md w-full">
                <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">Login</h1>
                {error && <p className="text-red-500 text-sm text-center">{error}</p>}
                <form className="space-y-4" onSubmit={handleLogin}>
                    {/* Email input */}
                    <input
                        type="email"
                        className="border p-3 rounded w-full"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    {/* Password input */}
                    <input
                        type="password"
                        className="border p-3 rounded w-full"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <button className="bg-green-400 text-white p-3 rounded w-full hover:bg-green-500 transition" type="submit">
                        Login
                    </button>
                </form>
            </section>
        </main>
    );
}
