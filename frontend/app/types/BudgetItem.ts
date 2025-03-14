interface BudgetItem {
    id: number; // Ideally a unique ID for each budget.
    category: string;
    amount: number;
    spent: number;
    remaining: number;
    frequency: string;
}

export default BudgetItem