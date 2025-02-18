
interface TableProps {
    children: React.ReactNode;
}

export function Table({ children }: Readonly<TableProps>) {
    return (
        <table className="w-full border-collapse border border-gray-300">
            {children}
        </table>
    );
}

export function TableHeader({ children }: Readonly<TableProps>) {
    return <thead className="bg-gray-200">{children}</thead>;
}

interface TableRowProps {
    children: React.ReactNode;
    className?: string;
}

export function TableRow({ children, className = "" }: Readonly<TableRowProps>) {
    return <tr className={`border-b border-gray-300 ${className}`}>{children}</tr>;
}


export function TableHead({ children }: Readonly<TableProps>) {
    return <th className="p-2 text-left">{children}</th>;
}

export function TableBody({ children }: Readonly<TableProps>) {
    return <tbody>{children}</tbody>;
}

export function TableCell({ children }: Readonly<TableProps>) {
    return <td className="p-2 border-r border-gray-300">{children}</td>;
}
