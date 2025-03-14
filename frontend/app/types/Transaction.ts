interface Transaction {
    category: string;
    date: string;
    amount: number;
    description: string;
    type: "income" | "expense";
}

export default Transaction