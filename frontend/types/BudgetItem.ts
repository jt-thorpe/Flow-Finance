interface BudgetItem {
    id: string;
    category: string;
    amount: number;
    spent: number;
    remaining: number;
    frequency: string;
}

export default BudgetItem