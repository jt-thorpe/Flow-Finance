'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function LoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const decodeToken = (token: string) => {
        try {
            const base64Url = token.split('.')[1]; // Extract payload
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            return JSON.parse(atob(base64)); // Decode and parse JSON
        } catch (error) {
            return null;
        }
    };

    useEffect(() => {
        const token = localStorage.getItem('token');

        if (token) {
            const decoded = decodeToken(token);

            if (decoded && decoded.exp * 1000 > Date.now()) {
                router.push('/dashboard'); // Token is valid
            } else {
                localStorage.removeItem('token'); // Remove expired/invalid token
            }
        }
    }, [router]);

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
            router.push('/dashboard');
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
