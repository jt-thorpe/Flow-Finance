import { useRouter } from "next/router";
import { useEffect, useState } from "react";

interface Transaction {
    category: string;
    date: string;
    amount: number;
    description: string;
    type: "income" | "expense";
}


interface BudgetItem {
    category: string;
    amount: number;
    spent: number;
    remaining: number;
}

const Dashboard = () => {
    const router = useRouter();
    const [error, setError] = useState('');
    const [userAlias, setUserAlias] = useState<string | null>(null);
    const [userTransactions, setUserTransactions] = useState<Transaction[]>([]);
    const [userIncomesTotal, setUserIncomesTotal] = useState<number | null>(null);
    const [userExpensesTotal, setUserExpensesTotal] = useState<number | null>(null);
    const [userBudgetSummary, setUserBudgetSummary] = useState<BudgetItem[]>([]);


    useEffect(() => {
        fetchUserData();
    }, []);

    const fetchUserData = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/dashboard/load`, {
                method: "GET",
                headers: { "Content-Type": "application/json" },
                credentials: "include", // Send cookie (JWT)
            });

            if (response.ok) {
                const data = await response.json();
                setUserAlias(data.user_alias)
                setUserTransactions(data.user_latest_transactions)
                setUserIncomesTotal(data.user_incomes_total)
                setUserExpensesTotal(data.user_expenses_total)
                setUserBudgetSummary(data.user_budget_summary)
            } else {
                setError('Failed to load user data.');
            }
        } catch (error) {
            setError('Error fetching user data.');
        }
    };

    return (
        <div className="min-h-screen bg-gray-100">
            {/* Navbar */}
            <nav className="bg-blue-600 p-4 flex justify-between items-center text-white">
                <div className="text-lg font-bold">Flow</div>
                <ul className="flex space-x-4">
                    <li><a href="/dashboard" className="hover:underline">Dashboard</a></li>
                    <li><a href="/budgets" className="hover:underline">Budgets</a></li>
                    <li><a href="/transactions" className="hover:underline">Transactions</a></li>
                    <li><a href="/settings" className="hover:underline">Settings</a></li>
                </ul>
                <button className="bg-red-500 px-3 py-1 rounded" onClick={() => router.push("/logout")}>
                    Logout
                </button>
            </nav>

            {/* Dashboard Content */}
            <div className="p-6">
                {/* Header */}
                <div className="mb-6">
                    <h1 className="text-2xl font-bold">Welcome back, {userAlias}!</h1>
                    <p className="text-gray-600">Your financial overview at a glance.</p>
                </div>

                {/* Overview Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-white p-4 rounded shadow">
                        <h2 className="text-lg font-semibold">Total Income</h2>
                        <p className="text-green-500 text-xl">£{(userIncomesTotal ?? 0) / 100}</p>
                    </div>
                    <div className="bg-white p-4 rounded shadow">
                        <h2 className="text-lg font-semibold">Total Expenses</h2>
                        <p className="text-red-500 text-xl">£{(userExpensesTotal ?? 0) / 100}</p>
                    </div>
                    <div className="bg-white p-4 rounded shadow">
                        <h2 className="text-lg font-semibold">Total Balance</h2>
                        <p className="text-blue-500 text-xl">£{((userIncomesTotal ?? 0) - (userExpensesTotal ?? 0)) / 100}</p>
                    </div>
                </div>

                {/* Recent Transactions */}
                <div className="mt-6">
                    <h2 className="text-xl font-bold">Recent Transactions</h2>
                    <div className="overflow-x-auto bg-white p-4 rounded shadow mt-2">
                        <table className="w-full border-collapse">
                            <thead>
                                <tr className="bg-gray-200">
                                    <th className="p-2">Date</th>
                                    <th className="p-2">Amount</th>
                                    <th className="p-2">Category</th>
                                    <th className="p-2">Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                {userTransactions.length > 0 ? (
                                    userTransactions.map((transaction, index) => (
                                        <tr key={index} className="border-t">
                                            <td className="p-2">{transaction.date}</td>
                                            <td className={`p-2 ${transaction.type === "income" ? "text-green-500" : "text-red-500"}`}>
                                                £{transaction.amount.toFixed(2)}
                                            </td>
                                            <td className="p-2">{transaction.category}</td>
                                            <td className="p-2">{transaction.description}</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={4} className="p-2 text-center text-gray-500">
                                            No recent transactions available.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Budget Categories */}
                <div className="mt-6">
                    <h2 className="text-xl font-bold">Budget Categories</h2>
                    <div className="overflow-x-auto bg-white p-4 rounded shadow mt-2">
                        <table className="w-full border-collapse">
                            <thead>
                                <tr className="bg-gray-200">
                                    <th className="p-2">Category</th>
                                    <th className="p-2">Budget</th>
                                    <th className="p-2">Spent</th>
                                    <th className="p-2">Remaining</th>
                                </tr>
                            </thead>
                            <tbody>
                                {userBudgetSummary.length > 0 ? (
                                    userBudgetSummary.map((budget, index) => (
                                        <tr key={index} className="border-t">
                                            <td className="p-2">{budget.category}</td>
                                            <td className="p-2">£{budget.amount.toFixed(2)}</td>
                                            <td className="p-2">£{budget.spent.toFixed(2)}</td>
                                            <td className="p-2">£{budget.remaining.toFixed(2)}</td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={4} className="p-2 text-center text-gray-500">No budget information available.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
