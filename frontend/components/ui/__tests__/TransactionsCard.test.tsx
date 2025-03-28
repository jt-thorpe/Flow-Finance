import { render, screen } from '@testing-library/react';
import TransactionsCard from '../TransactionsCard';
import Transaction from '../../../types/Transaction';

describe('TransactionsCard', () => {
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
            date: '2024-02-15'
        }
    ];

    it('groups transactions by month and renders month cards', () => {
        render(<TransactionsCard transactions={mockTransactions} />);

        // Check that month cards are rendered for both months
        expect(screen.getByRole('region', { name: 'March 2024' })).toBeInTheDocument();
        expect(screen.getByRole('region', { name: 'February 2024' })).toBeInTheDocument();

        // Check that transactions are correctly grouped
        const marchTransactions = screen.getByRole('region', { name: 'March 2024' });
        expect(marchTransactions).toHaveTextContent('Groceries');
        expect(marchTransactions).toHaveTextContent('Salary');

        const februaryTransactions = screen.getByRole('region', { name: 'February 2024' });
        expect(februaryTransactions).toHaveTextContent('Entertainment');
    });

    it('renders correctly with no transactions', () => {
        render(<TransactionsCard transactions={[]} />);

        // No month cards should be rendered
        expect(screen.queryByText('March 2024')).not.toBeInTheDocument();
        expect(screen.queryByText('February 2024')).not.toBeInTheDocument();
    });

    it('formats month names correctly', () => {
        const transactionsWithDifferentMonths: Transaction[] = [
            {
                id: '1',
                amount: 50.00,
                type: 'expense',
                category: 'Groceries',
                description: 'Weekly shop',
                frequency: 'Weekly',
                date: '2024-01-01'
            },
            {
                id: '2',
                amount: 1000.00,
                type: 'income',
                category: 'Salary',
                description: 'Monthly salary',
                frequency: 'Monthly',
                date: '2024-12-31'
            }
        ];

        render(<TransactionsCard transactions={transactionsWithDifferentMonths} />);

        // Check that month names are formatted correctly
        expect(screen.getByRole('region', { name: 'January 2024' })).toBeInTheDocument();
        expect(screen.getByRole('region', { name: 'December 2024' })).toBeInTheDocument();
    });
}); 