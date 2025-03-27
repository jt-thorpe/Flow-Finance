'use client';

import { useState, useEffect } from "react";
import Navbar from "../../components/ui/NavBar";
import TransactionsCard from "../../components/ui/TransactionsCard";
import { Button } from "../../components/ui/button";
import { TransactionModal } from "../../components/ui/transaction_modal";
import useResponsive from "../../hooks/useResponsive";
import { fetchTransactions } from "../../services/transactions";
import Transaction from "../../types/Transaction";

export default function TransactionsPage() {
    const { isMobile, isNavOpen, setIsNavOpen } = useResponsive();
    const [userTransactions, setUserTransactions] = useState<Transaction[]>([]);
    const [page, setPage] = useState<number>(1);
    const [limit, setLimit] = useState<number>(20);
    const [hasMore, setHasMore] = useState<boolean>(true);
    const [modalOpen, setModalOpen] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    useEffect(() => {
        loadTransactions();
    }, []);

    const loadTransactions = async () => {
        try {
            setIsLoading(true);
            setError(null);
            const response = await fetchTransactions(page.toString(), limit.toString());
            
            if (response.transactions.length > 0) {
                setUserTransactions((prev) => [...prev, ...response.transactions]);
                setPage((prev) => prev + 1);
            }
            setHasMore(response.has_more);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to load transactions");
        } finally {
            setIsLoading(false);
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
                <div className="flex-1 p-6 transition-all duration-300 md:ml-64">
                    <section className="bg-green-400 shadow-md rounded-2xl p-4 w-full max-w-4xl">
                        <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">Transactions</h1>
                        <div className="flex justify-between items-center mb-4">
                            <Button onClick={() => setModalOpen(true)}>Add Transaction</Button>
                        </div>
                        {error && (
                            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
                                <span className="block sm:inline">{error}</span>
                            </div>
                        )}
                        <section className="bg-white border-fixed border-black rounded-2xl w-full max-w-4xl mt-6">
                            {isLoading && userTransactions.length === 0 ? (
                                <div className="flex justify-center items-center h-32">
                                    <span className="text-gray-500">Loading transactions...</span>
                                </div>
                            ) : (
                                <TransactionsCard transactions={userTransactions} />
                            )}
                        </section>
                        {hasMore && (
                            <div className="flex justify-center mt-4">
                                <Button 
                                    onClick={loadTransactions}
                                    className={isLoading ? "opacity-50 cursor-not-allowed" : ""}
                                >
                                    {isLoading ? "Loading..." : "Load More"}
                                </Button>
                            </div>
                        )}
                    </section>
                </div>
            </div>
            {modalOpen && <TransactionModal onClose={() => setModalOpen(false)}>
                <div>Add New Transaction</div>
            </TransactionModal>}
        </main>
    );
}
