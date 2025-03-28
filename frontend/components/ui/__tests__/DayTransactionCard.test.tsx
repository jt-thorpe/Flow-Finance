import { render, screen } from '@testing-library/react';
import DayTransactionsCard from '../DayTransactionCard';
import Transaction from '../../../types/Transaction';

describe('DayTransactionsCard', () => {
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
        }
    ];

    it('renders the day heading correctly', () => {
        render(
            <DayTransactionsCard
                day="27 March 2024"
                transactions={mockTransactions}
            />
        );

        expect(screen.getByText('27 March 2024')).toBeInTheDocument();
    });

    it('displays transaction amounts with correct formatting and colours', () => {
        render(
            <DayTransactionsCard
                day="27 March 2024"
                transactions={mockTransactions}
            />
        );

        // Check expense (red)
        const expenseAmount = screen.getByText('£50.00');
        expect(expenseAmount).toHaveClass('text-red-500');

        // Check income (green)
        const incomeAmount = screen.getByText('£1000.00');
        expect(incomeAmount).toHaveClass('text-green-500');
    });

    it('displays all transaction details in the table', () => {
        render(
            <DayTransactionsCard
                day="27 March 2024"
                transactions={mockTransactions}
            />
        );

        // Check headers
        expect(screen.getByText('Amount')).toBeInTheDocument();
        expect(screen.getByText('Category')).toBeInTheDocument();
        expect(screen.getByText('Frequency')).toBeInTheDocument();
        expect(screen.getByText('Description')).toBeInTheDocument();

        // Check transaction details
        expect(screen.getByText('Groceries')).toBeInTheDocument();
        expect(screen.getByText('Weekly')).toBeInTheDocument();
        expect(screen.getByText('Weekly shop')).toBeInTheDocument();
        expect(screen.getByText('Salary')).toBeInTheDocument();
        expect(screen.getByText('Monthly')).toBeInTheDocument();
        expect(screen.getByText('Monthly salary')).toBeInTheDocument();
    });

    it('renders correctly with no transactions', () => {
        render(
            <DayTransactionsCard
                day="27 March 2024"
                transactions={[]}
            />
        );

        expect(screen.getByText('27 March 2024')).toBeInTheDocument();
        // Table should still be rendered but empty
        expect(screen.getByRole('table')).toBeInTheDocument();
    });

    it('applies correct styling classes', () => {
        render(
            <DayTransactionsCard
                day="27 March 2024"
                transactions={mockTransactions}
            />
        );

        const card = screen.getByRole('region', { name: '27 March 2024' });
        expect(card).toHaveClass(
            'day-card',
            'border',
            'border-fixed',
            'border-black',
            'bg-yellow-400',
            'rounded-md',
            'p-3',
            'mb-4'
        );
    });
}); 