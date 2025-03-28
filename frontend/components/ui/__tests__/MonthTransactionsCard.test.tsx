import { render, screen } from '@testing-library/react';
import MonthTransactionsCard from '../MonthTransactionsCard';
import Transaction from '../../../types/Transaction';

describe('MonthTransactionsCard', () => {
    const mockTransactions: Transaction[] = [
        {
            id: '1',
            amount: 50.00,
            type: 'expense',
            category: 'Groceries',
            description: 'Weekly shop',
            frequency: 'Weekly',
            date: '2024-03-27'
        },
        {
            id: '2',
            amount: 1000.00,
            type: 'income',
            category: 'Salary',
            description: 'Monthly salary',
            frequency: 'Monthly',
            date: '2024-03-27'
        },
        {
            id: '3',
            amount: 25.00,
            type: 'expense',
            category: 'Entertainment',
            description: 'Movie night',
            frequency: 'One-off',
            date: '2024-03-28'
        }
    ];

    it('renders the month heading correctly', () => {
        render(
            <MonthTransactionsCard
                month="March 2024"
                transactions={mockTransactions}
            />
        );

        expect(screen.getByText('March 2024')).toBeInTheDocument();
    });

    it('groups transactions by day and renders day cards', () => {
        render(
            <MonthTransactionsCard
                month="March 2024"
                transactions={mockTransactions}
            />
        );

        // Check that day cards are rendered for both days
        expect(screen.getByRole('region', { name: '27/03/2024' })).toBeInTheDocument();
        expect(screen.getByRole('region', { name: '28/03/2024' })).toBeInTheDocument();

        // Check that transactions are correctly grouped
        const day1Transactions = screen.getByRole('region', { name: '27/03/2024' });
        expect(day1Transactions).toHaveTextContent('Groceries');
        expect(day1Transactions).toHaveTextContent('Salary');

        const day2Transactions = screen.getByRole('region', { name: '28/03/2024' });
        expect(day2Transactions).toHaveTextContent('Entertainment');
    });

    it('renders correctly with no transactions', () => {
        render(
            <MonthTransactionsCard
                month="March 2024"
                transactions={[]}
            />
        );

        expect(screen.getByText('March 2024')).toBeInTheDocument();
        // No day cards should be rendered
        expect(screen.queryByText('27/03/2024')).not.toBeInTheDocument();
        expect(screen.queryByText('28/03/2024')).not.toBeInTheDocument();
    });

    it('applies correct styling classes', () => {
        render(
            <MonthTransactionsCard
                month="March 2024"
                transactions={mockTransactions}
            />
        );

        const card = screen.getByRole('region', { name: 'March 2024' });
        expect(card).toHaveClass(
            'month-card',
            'border',
            'border-fixed',
            'border-black',
            'bg-blue-400',
            'shadow-md',
            'rounded-xl',
            'p-4',
            'mb-6'
        );
    });
}); 