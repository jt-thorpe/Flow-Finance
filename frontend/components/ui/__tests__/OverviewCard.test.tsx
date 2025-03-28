import { render, screen } from '@testing-library/react';
import OverviewCard from '../OverviewCard';

describe('OverviewCard', () => {
    it('renders the title correctly', () => {
        render(
            <OverviewCard
                title="Total Income"
                amount={1000.00}
                color="text-green-500"
            />
        );

        expect(screen.getByText('Total Income')).toBeInTheDocument();
    });

    it('formats amount with correct currency symbol and decimal places', () => {
        render(
            <OverviewCard
                title="Total Income"
                amount={1000.50}
                color="text-green-500"
            />
        );

        expect(screen.getByText('£1000.50')).toBeInTheDocument();
    });

    it('applies the correct colour class to the amount', () => {
        render(
            <OverviewCard
                title="Total Income"
                amount={1000.00}
                color="text-green-500"
            />
        );

        const amountElement = screen.getByText('£1000.00');
        expect(amountElement).toHaveClass('text-green-500');
    });

    it('handles null amount by displaying £0.00', () => {
        render(
            <OverviewCard
                title="Total Income"
                amount={null}
                color="text-green-500"
            />
        );

        expect(screen.getByText('£0.00')).toBeInTheDocument();
    });

    it('applies correct styling classes', () => {
        render(
            <OverviewCard
                title="Total Income"
                amount={1000.00}
                color="text-green-500"
            />
        );

        const card = screen.getByRole('region', { name: 'Total Income' });
        expect(card).toHaveClass(
            'bg-white',
            'p-6',
            'rounded-2xl',
            'shadow-md',
            'text-center'
        );
    });
}); 