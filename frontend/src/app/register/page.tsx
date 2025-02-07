'use client';

import EmailInput from "@/app/components/EmailInput";
import { useRouter } from 'next/navigation';
import { useState } from "react";
import { useForm } from "react-hook-form";

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
        <div className="max-w-md mx-auto mt-10">
            <h1 className="text-2xl font-bold mb-4">Register</h1>
            <form onSubmit={handleSubmit(onSubmit)}>
                {/* Alias Input */}
                <input
                    type="text"
                    {...register("alias", { required: "Name is required" })}
                    placeholder="Enter your name"
                    className="border p-2 rounded w-full"
                />
                {errors.alias && <p className="text-red-500">{errors.alias.message}</p>}

                {/* Email Input - Pass validation error */}
                <EmailInput register={register} emailValue={email} error={errors.email} />

                {/* Password Input */}
                <input
                    type="password"
                    {...register("password", { required: "Password is required" })}
                    placeholder="Enter password"
                    className="border p-2 rounded w-full mt-2"
                />
                {errors.password && <p className="text-red-500">{errors.password.message}</p>}

                {/* Confirm Password Input */}
                <input
                    type="password"
                    {...register("confirmPassword", {
                        required: "Please confirm password",
                        validate: (value) =>
                            value === password || "Passwords do not match",
                    })}
                    placeholder="Confirm password"
                    className="border p-2 rounded w-full mt-2"
                />
                {errors.confirmPassword && <p className="text-red-500">{errors.confirmPassword.message}</p>}

                {/* Error & Success Messages */}
                {apiError && <p className="text-red-500">{apiError}</p>}
                {successMessage && <p className="text-green-500">{successMessage}</p>}

                {/* Submit Button */}
                <button
                    type="submit"
                    className="bg-blue-500 text-white p-2 rounded mt-4 w-full"
                >
                    Register
                </button>
            </form>
        </div>
    );
};

export default RegisterPage;
