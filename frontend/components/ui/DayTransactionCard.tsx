import React from 'react';
import Transaction from '../../types/Transaction';
import Table from './Table';

interface DayTransactionsCardProps {
    day: string;
    transactions: Transaction[];
}

const DayTransactionsCard: React.FC<DayTransactionsCardProps> = ({ day, transactions }) => {
    return (
        <div className="day-card bg-gray-50 rounded-md p-3 mb-4">
            <h3 className="text-xl font-semibold mb-2">{day}</h3>
            <Table headers={["Amount", "Category", "Frequency", "Description"]} data={transactions.map(transaction => [
                <span key={transaction.date} className={transaction.type === "income" ? "text-green-500" : "text-red-500"}>£{transaction.amount.toFixed(2)}</span>,
                transaction.category,
                transaction.frequency,
                transaction.description,
            ])} />
        </div>
    );
};

export default DayTransactionsCard;
