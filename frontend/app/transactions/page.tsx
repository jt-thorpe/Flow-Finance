'use client';

import { useState } from "react";
import Navbar from "../../components/ui/NavBar";
import { Button } from "../../components/ui/button";
import { Card, CardContent } from "../../components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../../components/ui/table";
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
    const [transactions, setTransactions] = useState<Transaction[]>([]);
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
                        <Card>
                            <CardContent>
                                <Table>
                                    <TableHeader>
                                        <TableRow>
                                            <TableHead>Date</TableHead>
                                            <TableHead>Amount</TableHead>
                                            <TableHead>Category</TableHead>
                                            <TableHead>Frequency</TableHead>
                                            <TableHead>Description</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        {transactions.map((tx) => (
                                            <TableRow key={tx.id} className={tx.type === "income" ? "text-green-600" : "text-red-600"}>
                                                <TableCell>{tx.date}</TableCell>
                                                <TableCell>${tx.amount}</TableCell>
                                                <TableCell>{tx.category}</TableCell>
                                                <TableCell>{tx.frequency ?? "-"}</TableCell>
                                                <TableCell>{tx.description}</TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </CardContent>
                        </Card>
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
