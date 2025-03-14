interface Transaction {
    id: string
    type: "income" | "expense";
    category: string;
    date: string;
    frequency: string;
    amount: number;
    description: string;
}

export default Transaction