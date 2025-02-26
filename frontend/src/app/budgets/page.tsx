'use client';

import { useEffect, useState } from "react";
import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";
import Navbar from "../components/ui/NavBar";
import { useAuth } from "../context/AuthContext";

interface BudgetItem {
    category: string;
    amount: number;
    spent: number;
    remaining: number;
    frequency: string;
}

const Budgets = () => {
    const { isAuthenticated, loading } = useAuth();
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
        if (!loading && isAuthenticated) {
            fetchUserBudgets();
        }
    }, [loading, isAuthenticated]);

    const fetchUserBudgets = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/budgets/load`, {
                method: "GET",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
            });

            if (response.status === 401) {
                window.location.href = "/login";
                return;
            }

            if (response.ok) {
                const data = await response.json();
                setUserBudgetSummary(data || []); // Ensure it's an array
            }
        } catch (error) {
            console.error("Error fetching budget data", error);
            setUserBudgetSummary([]); // Fallback to empty array
        }
    };

    return (
        <main className="flex flex-col items-center min-v-screen px-4 py-8 bg-gray-100">
            <div className="flex min-h-screen bg-gray-100 relative">
                <div className={`fixed top-0 left-0 h-screen bg-white shadow-md transition-transform duration-300 ${isMobile ? (isNavOpen ? 'translate-x-0 w-64' : '-translate-x-full w-0') : 'w-64 translate-x-0'}`}>
                    <Navbar />
                </div>
                {isMobile && isNavOpen && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 z-40" onClick={() => setIsNavOpen(false)}></div>
                )}
                <div className='flex-1 p-6 transition-all duration-300 md:ml-64'>
                    <section className="bg-white shadow-md rounded-2xl p-8 w-full max-w-4xl">
                        <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">Your Budgets</h1>
                        <div className="flex flex-col gap-6">
                            {userBudgetSummary.length > 0 ? (
                                userBudgetSummary.map((budget, index) => (
                                    <BudgetCard key={index} budget={budget} isMobile={isMobile} />
                                ))
                            ) : (
                                <p className="text-center text-gray-500">No budgets available.</p>
                            )}
                        </div>
                    </section>
                </div>
            </div>
        </main>
    );
};

const BudgetCard = ({ budget, isMobile }: { budget: Record<string, any>, isMobile: boolean }) => {
    const data = [
        { name: "Spent", value: budget.spent },
        { name: "Remaining", value: budget.remaining },
    ];
    const COLORS = ["#FF6B6B", "#4CAF50"];

    return (
        <div className={`bg-white p-6 rounded-2xl shadow-md ${isMobile ? 'flex flex-col items-center' : 'flex items-center w-full'}`}>
            <div className={`${isMobile ? 'w-full mb-4 flex justify-center' : 'w-1/4 flex justify-center'}`}>
                <ResponsiveContainer width={100} height={100}>
                    <PieChart>
                        <Pie data={data} cx="50%" cy="100%" startAngle={180} endAngle={0} innerRadius={30} outerRadius={45} paddingAngle={2} dataKey="value">
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                        </Pie>
                    </PieChart>
                </ResponsiveContainer>
            </div>
            <div className={`${isMobile ? 'w-full text-center' : 'w-1/4 pl-4'}`}>
                <h2 className="text-lg font-semibold">{budget.category}</h2>
                <p className="text-gray-700">Total: £{budget.amount.toFixed(2)}</p>
                <p className="text-red-500">Spent: £{budget.spent.toFixed(2)}</p>
                <p className="text-green-500">Remaining: £{budget.remaining.toFixed(2)}</p>
                <p className="text-gray-500 text-sm">Frequency: {budget.frequency}</p>
            </div>
            <div className={`${isMobile ? 'w-full mt-4 bg-gray-100 p-3 rounded-md text-gray-600 text-sm' : 'w-2/4 bg-gray-100 p-3 rounded-md text-gray-600 text-sm ml-4'}`}>
                <ul>
                    <li>• There are {0} remaining days of this budget.</li>
                    <li>• There are {0} many scheduled payments remaining for the month.</li>
                </ul>
            </div>
        </div>
    );
};

export default Budgets;
