'use client';

import { useEffect, useState } from "react";
import Navbar from '../components/NavBar';
import { useAuth } from '../context/AuthContext';

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
    const { isAuthenticated, loading } = useAuth();
    const [error, setError] = useState('');
    const [userAlias, setUserAlias] = useState<string | null>(null);
    const [userTransactions, setUserTransactions] = useState<Transaction[]>([]);
    const [userIncomesTotal, setUserIncomesTotal] = useState<number | null>(null);
    const [userExpensesTotal, setUserExpensesTotal] = useState<number | null>(null);
    const [userBudgetSummary, setUserBudgetSummary] = useState<BudgetItem[]>([]);
    const [isMobile, setIsMobile] = useState(false);
    const [isNavOpen, setIsNavOpen] = useState(false);

    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
            if (window.innerWidth >= 768) setIsNavOpen(false);
        };
        handleResize();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    useEffect(() => {
        console.log("Dashboard useEffect triggered. loading =", loading, "isAuthenticated =", isAuthenticated);

        if (!loading && isAuthenticated) {
            console.log("Fetching user data...");
            fetchUserData();
        }
    }, [loading, isAuthenticated]);

    const fetchUserData = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/dashboard/load`, {
                method: "GET",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
            });

            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }

            if (response.ok) {
                const data = await response.json();
                setUserAlias(data.user_alias);
                setUserTransactions(data.user_latest_transactions);
                setUserIncomesTotal(data.user_incomes_total);
                setUserExpensesTotal(data.user_expenses_total);
                setUserBudgetSummary(data.user_budget_summary);
            } else {
                setError('Failed to load user data.');
            }
        } catch (error) {
            setError("Error fetching dashboard data");
        }
    }

    return (
        <main className="flex flex-col items-center min-v-screen px-4 py-8 bg-gray-100">
            <div className="flex min-h-screen bg-gray-100 relative">
                {/* === Navbar (Fixed Sidebar for Desktop, Overlay for Mobile) === */}
                <div className={`fixed top-0 left-0 h-screen bg-white shadow-md transition-transform duration-300 ${isMobile ? (isNavOpen ? 'translate-x-0 w-64' : '-translate-x-full w-0') : 'w-64 translate-x-0'}`}>
                    <Navbar />
                </div>

                {/* === Overlay for Mobile Navigation === */}
                {isMobile && isNavOpen && (
                    <div
                        className="fixed inset-0 bg-black bg-opacity-50 z-40"
                        onClick={() => setIsNavOpen(false)}
                    ></div>
                )}

                {/* === Main Content Area === */}
                <div className='flex-1 p-6 transition-all duration-300 md:ml-64'>
                    {/* Dashboard Overview */}
                    <section className="bg-white shadow-md rounded-2xl p-8 w-full max-w-4xl">
                        <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">Welcome back, {userAlias}!</h1>
                        <p className="text-center text-gray-600 mb-4">Your financial overview at a glance.</p>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <OverviewCard title="Total Income" amount={userIncomesTotal} color="text-green-500" />
                            <OverviewCard title="Total Expenses" amount={userExpensesTotal} color="text-red-500" />
                            <OverviewCard title="Total Balance" amount={(userIncomesTotal ?? 0) - (userExpensesTotal ?? 0)} color="text-blue-500" />
                        </div>
                    </section>

                    {/* Budget Summary */}
                    <section className="bg-white shadow-md rounded-2xl p-8 w-full max-w-4xl mt-6">
                        <h2 className="text-xl font-bold mb-4">Budget Summary</h2>
                        <Table headers={["Category", "Budget", "Spent", "Remaining"]} data={userBudgetSummary.map(budget => [budget.category, `£${budget.amount.toFixed(2)}`, `£${budget.spent.toFixed(2)}`, `£${budget.remaining.toFixed(2)}`])} />
                    </section>

                    {/* Recent Transactions */}
                    <section className="bg-white shadow-md rounded-2xl p-8 w-full max-w-4xl mt-6">
                        <h2 className="text-xl font-bold mb-4">Recent Transactions</h2>
                        <Table headers={["Date", "Amount", "Category", "Description"]} data={userTransactions.map(transaction => [
                            transaction.date,
                            <span key={transaction.date} className={transaction.type === "income" ? "text-green-500" : "text-red-500"}>£{transaction.amount.toFixed(2)}</span>,
                            transaction.category,
                            transaction.description
                        ])} />
                    </section>
                </div>
            </div>
        </main>
    );
};


const OverviewCard = ({ title, amount, color }: { title: string; amount: number | null; color: string }) => (
    <div className="bg-white p-6 rounded-2xl shadow-md text-center">
        <h2 className="text-lg font-semibold">{title}</h2>
        <p className={`text-xl font-bold ${color}`}>£{(amount ?? 0).toFixed(2)}</p>
    </div>
);

const Table = ({ headers, data }: { headers: string[], data: any[][] }) => (
    <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left">
            <thead>
                <tr className="bg-gray-200">
                    {headers.map((header, index) => <th key={index} className="p-3 font-semibold">{header}</th>)}
                </tr>
            </thead>
            <tbody>
                {data.length > 0 ? (
                    data.map((row, rowIndex) => (
                        <tr key={rowIndex} className="border-t">
                            {row.map((cell, cellIndex) => <td key={cellIndex} className="p-3">{cell}</td>)}
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan={headers.length} className="p-3 text-center text-gray-500">No data available.</td>
                    </tr>
                )}
            </tbody>
        </table>
    </div>
);

export default Dashboard;
