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
        <div className="flex h-screen items-center justify-center bg-white">
            <form className="bg-grey-300 p-8 rounded-lg shadow-lg" onSubmit={handleLogin}>
                <h2 className="text-2xl mb-4">Login</h2>
                {error && <p className="text-red-500">{error}</p>}
                <input
                    type="email"
                    className="block w-full p-2 border rounded mb-2"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    className="block w-full p-2 border rounded mb-2"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button className="w-full bg-blue-500 text-white p-2 rounded" type="submit">Login</button>
            </form>
        </div>
    );
}
