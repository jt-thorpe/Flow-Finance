interface ButtonProps {
    children: React.ReactNode;
    onClick?: () => void;
    type?: "button" | "submit" | "reset";
    className?: string;
}

export function Button({ children, onClick, type = "button", className = "" }: ButtonProps) {
    return (
        <button
            type={type}
            onClick={onClick}
            className={`bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 ${className}`}
        >
            {children}
        </button>
    );
}

