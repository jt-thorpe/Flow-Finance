'use client';

import { useState } from "react";
import Navbar from "../../components/ui/NavBar";
import TransactionsCard from "../../components/ui/TransactionsCard";
import { Button } from "../../components/ui/button";
import { TransactionModal } from "../../components/ui/transaction_modal";
import useResponsive from "../../hooks/useResponsive";
import { fetchTransactions } from "../../services/transactions";

interface Transaction {
    id: string;
    date: string;
    amount: number;
    category: string;
    frequency?: string;
    description: string;
    type: "income" | "expense";
}

export default function TransactionsPage() {
    const { isMobile, isNavOpen, setIsNavOpen } = useResponsive();
    const [userTransactions, setTransactions] = useState<Transaction[]>([]);
    const [page, setPage] = useState<number>(1);
    const [limit, setLimit] = useState<number>(20)
    const [hasMore, setHasMore] = useState<boolean>(true);
    const [modalOpen, setModalOpen] = useState<boolean>(false);

    const loadTransactions = async () => {
        const response = await fetchTransactions(page.toString(), limit.toString());
        if (response.transactions.length > 0) {
            setTransactions((prev) => [...prev, ...response.transactions]);
            setPage((prev) => prev + 1);
        }
        setHasMore(response.has_more);
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
                <div className="flex-1 p-6 transition-all duration-300 md:ml-64">
                    <section className="bg-white shadow-md rounded-2xl p-8 w-full max-w-4xl">
                        <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">Transactions</h1>
                        <div className="flex justify-between items-center mb-4">
                            <Button onClick={() => setModalOpen(true)}>Add Transaction</Button>
                        </div>
                        <section className="bg-white shadow-md rounded-2xl p-8 w-full max-w-4xl mt-6">
                            <h2 className="text-xl font-bold mb-4">Recent Transactions</h2>
                            <TransactionsCard transactions={userTransactions} />
                        </section>
                        {hasMore && (
                            <div className="flex justify-center mt-4">
                                <Button onClick={loadTransactions}>Load More</Button>
                            </div>
                        )}
                    </section>
                </div>
            </div>
            {modalOpen && <TransactionModal onClose={() => setModalOpen(false)}> </TransactionModal>}
        </main>
    );
}
