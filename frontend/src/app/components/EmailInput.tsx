import { useEffect, useState } from "react";
import { FieldError, UseFormRegister } from "react-hook-form";

interface EmailInputProps {
    register: UseFormRegister<any>;
    emailValue: string;
    error?: FieldError;
}

const EmailInput: React.FC<EmailInputProps> = ({ register, emailValue, error }) => {
    const [emailError, setEmailError] = useState<string | null>(null);

    useEffect(() => {
        setEmailError(null);

        if (!emailValue.includes("@")) return; // improve validation

        const checkEmailAvailability = async () => {
            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/check-taken?email=${encodeURIComponent(emailValue)}`);
                const data = await response.json();

                if (data.taken) {
                    setEmailError("Email is already taken.");
                } else {
                    setEmailError(null);
                }
            } catch (error) {
                console.error("Error checking email:", error);
            }
        };

        const debounceTimeout = setTimeout(checkEmailAvailability, 750); // Debounce API call
        return () => clearTimeout(debounceTimeout);
    }, [emailValue]);

    return (
        <div>
            <input
                type="email"
                {...register("email", {
                    required: "Email is required",
                    pattern: {
                        value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                        message: "Invalid email format",
                    },
                })}
                placeholder="Enter your email"
                className="border p-2 rounded w-full"
            />
            {error && <p className="text-red-500">{error.message}</p>}
            {emailError && <p className="text-red-500">{emailError}</p>}
        </div>
    );
};

export default EmailInput;
