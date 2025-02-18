interface CardProps {
    children: React.ReactNode;
}

export function Card({ children }: CardProps) {
    return (
        <div className="bg-white shadow-md rounded-lg p-4">
            {children}
        </div>
    );
}

export function CardContent({ children }: CardProps) {
    return <div className="p-2">{children}</div>;
}

