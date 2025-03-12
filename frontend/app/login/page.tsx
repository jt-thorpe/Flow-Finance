'use client';

import { useRouter } from 'next/navigation';
import { useContext, useState } from 'react';
import { AuthContext } from "../../context/AuthContext";


export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const auth = useContext(AuthContext);
    const router = useRouter();

    if (!auth) {
        console.log("AuthContext is null! AuthProvider missing!");
        return <p>Critical Error: Login Page Unavailable</p>;
    }

    const handleLoginSubmit = async (event: React.FormEvent) => {
        event.preventDefault();

        if (!email || !password) {
            setError("Please provide your email and password.");
            return;
        }

        console.log("Submitting login request...");
        const success = await auth.login(email, password);

        if (success) {
            console.log("Login successful, redirecting to dashboard...");
            router.push("/dashboard"); // Middleware will now verify the token
        } else {
            setError("Invalid credentials, please try again.");
        }
    };


    return (
        <main className="flex flex-col items-center justify-center min-h-screen px-4 py-8 bg-gray-100">
            <section className="bg-white shadow-md rounded-2xl p-8 max-w-md w-full">
                <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">Login</h1>
                {error && <p className="text-red-500 text-sm text-center">{error}</p>}
                <form className="space-y-4" onSubmit={handleLoginSubmit}>
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
