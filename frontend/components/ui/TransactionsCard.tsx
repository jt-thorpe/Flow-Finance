import React from 'react';
import Transaction from '../../types/Transaction';
import MonthTransactionsCard from './MonthTransactionsCard';

const DashboardTransactions: React.FC<{ transactions: Transaction[] }> = ({ transactions }) => {
    const transactionsByMonth = groupByMonth(transactions);

    return (
        <div>
            {Object.keys(transactionsByMonth).map(month => (
                <MonthTransactionsCard key={month} month={month} transactions={transactionsByMonth[month]} />
            ))}
        </div>
    );
};

const groupByMonth = (transactions: Transaction[]) => {
    return transactions.reduce((acc, transaction) => {
        const dateObj = new Date(transaction.date);
        const monthKey = dateObj.toLocaleString('default', { month: 'long', year: 'numeric' });
        if (!acc[monthKey]) {
            acc[monthKey] = [];
        }
        acc[monthKey].push(transaction);
        return acc;
    }, {} as Record<string, Transaction[]>);
};

export default DashboardTransactions;
