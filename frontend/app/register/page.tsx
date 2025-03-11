'use client';

import { useRouter } from 'next/navigation';
import { useState } from "react";
import { useForm } from "react-hook-form";
import EmailInput from '../../components/ui/EmailInput';

interface FormData {
    alias: string;
    email: string;
    password: string;
    confirmPassword: string;
}

const RegisterPage: React.FC = () => {
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors },
    } = useForm<FormData>();

    const router = useRouter();
    const email = watch("email") || "";
    const password = watch("password");
    const [apiError, setApiError] = useState<string | null>(null);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);

    const onSubmit = async (data: FormData) => {
        setApiError(null);
        setSuccessMessage(null);

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    alias: data.alias,
                    email: data.email,
                    password: data.password,
                }),
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || "Failed to register");
            }

            setSuccessMessage("Registration successful! 🎉");
            router.push('/login');
        } catch (error: any) {
            setApiError(error.message || "Something went wrong.");
        }
    };

    return (
        <main className="flex flex-col items-center justify-center min-h-screen px-4 py-8 bg-gray-100">
            <section className="bg-white shadow-md rounded-2xl p-8 max-w-md w-full">
                <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">Register</h1>
                <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                    {/* Alias Input */}
                    <input
                        type="text"
                        {...register("alias", { required: "Name is required" })}
                        placeholder="Enter your name"
                        className="border p-3 rounded w-full"
                    />
                    {errors.alias && <p className="text-red-500 text-sm">{errors.alias.message}</p>}

                    {/* Email Input - Pass validation error */}
                    <EmailInput register={register} emailValue={email} error={errors.email} />

                    {/* Password Input */}
                    <input
                        type="password"
                        {...register("password", { required: "Password is required" })}
                        placeholder="Enter password"
                        className="border p-3 rounded w-full"
                    />
                    {errors.password && <p className="text-red-500 text-sm">{errors.password.message}</p>}

                    {/* Confirm Password Input */}
                    <input
                        type="password"
                        {...register("confirmPassword", {
                            required: "Please confirm password",
                            validate: (value) => value === password || "Passwords do not match",
                        })}
                        placeholder="Confirm password"
                        className="border p-3 rounded w-full"
                    />
                    {errors.confirmPassword && <p className="text-red-500 text-sm">{errors.confirmPassword.message}</p>}

                    {/* Error & Success Messages */}
                    {apiError && <p className="text-red-500 text-sm text-center">{apiError}</p>}
                    {successMessage && <p className="text-green-500 text-sm text-center">{successMessage}</p>}

                    {/* Submit Button */}
                    <button
                        type="submit"
                        className="bg-green-400 text-white p-3 rounded w-full hover:bg-green-500 transition"
                    >
                        Register
                    </button>
                </form>
            </section>
        </main>
    );
};

export default RegisterPage;
