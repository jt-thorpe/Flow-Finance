import React from 'react';
import Transaction from '../../types/Transaction';
import DayTransactionsCard from './DayTransactionCard';

interface MonthTransactionsCardProps {
    month: string;
    transactions: Transaction[];
}

const MonthTransactionsCard: React.FC<MonthTransactionsCardProps> = ({ month, transactions }) => {
    // Group transactions by day within this month
    const transactionsByDay = groupByDay(transactions);

    return (
        <div className="month-card border border-fixed border-black bg-blue-400 shadow-md rounded-xl p-4 mb-6">
            <h2 className="text-2xl font-bold mb-4">{month}</h2>
            {Object.keys(transactionsByDay).map(day => (
                <DayTransactionsCard key={day} day={day} transactions={transactionsByDay[day]} />
            ))}
        </div>
    );
};

// Include the helper here or import it if defined elsewhere
const groupByDay = (transactions: Transaction[]) => {
    return transactions.reduce((acc, transaction) => {
        const dayKey = new Date(transaction.date).toLocaleDateString();
        if (!acc[dayKey]) {
            acc[dayKey] = [];
        }
        acc[dayKey].push(transaction);
        return acc;
    }, {} as Record<string, Transaction[]>);
};

export default MonthTransactionsCard;
