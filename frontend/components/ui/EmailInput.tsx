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
            if (!emailValue || !emailValue.includes('@')) {
                setEmailError('');
                return;
            }

            try {
                const response = await fetch(`/api/users/check-taken?email=${encodeURIComponent(emailValue)}`);
                const data = await response.json();

                if (!response.ok || !data.success) {
                    console.error("Error checking email availability:", data.message);
                    setEmailError(data.message);
                    return;
                }

                if (data.taken) {
                    setEmailError("Email is already taken");
                } else {
                    setEmailError("");
                }
            } catch (error) {
                console.error(error);
                setEmailError(error instanceof Error ? error.message : "Error checking email availability");
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
