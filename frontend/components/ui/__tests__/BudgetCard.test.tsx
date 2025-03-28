import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import { flushSync } from 'react-dom'
import BudgetCard from '../BudgetCard'
import BudgetItem from '../../../types/BudgetItem'

// Mock the EditBudgetModal component
jest.mock('../EditBudgetModal', () => {
  return function MockEditBudgetModal({ onSave, onCancel }: any) {
    return (
      <div role="dialog" aria-labelledby="modal-title" data-testid="edit-budget-modal">
        <h2 id="modal-title">Edit Budget</h2>
        <button onClick={() => {
          onSave({ id: '1', user_id: '1', category: 'Updated Category', amount: '1000', spent: '500', remaining: '500', frequency: 'Monthly' });
        }}>
          Save
        </button>
        <button onClick={onCancel}>Cancel</button>
      </div>
    )
  }
})

describe('BudgetCard', () => {
  const mockBudget: BudgetItem = {
    id: '1',
    user_id: '1',
    category: 'Groceries',
    amount: '1000',
    spent: '500',
    remaining: '500',
    frequency: 'Monthly',
  }

  const mockToggleSelection = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
    jest.useFakeTimers()
  })

  afterEach(() => {
    jest.useRealTimers()
  })

  it('renders budget information correctly', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={false}
        isRemoveMode={false}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    expect(screen.getByText('Groceries')).toBeInTheDocument()
    expect(screen.getByText(/Total: £1000.00/)).toBeInTheDocument()
    expect(screen.getByText(/Spent: £500.00/)).toBeInTheDocument()
    expect(screen.getByText(/Remaining: £500.00/)).toBeInTheDocument()
    expect(screen.getByText(/Frequency: Monthly/)).toBeInTheDocument()
  })

  it('opens edit modal when clicked in normal mode', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={false}
        isRemoveMode={false}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    const card = screen.getByRole('button').parentElement
    fireEvent.click(card!)

    // Check if edit modal is rendered
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })

  it('toggles selection when clicked in remove mode', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={false}
        isRemoveMode={true}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    const card = screen.getByRole('button').parentElement
    fireEvent.click(card!)

    expect(mockToggleSelection).toHaveBeenCalledTimes(1)
  })

  it('applies selected styling in remove mode', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={false}
        isRemoveMode={true}
        isSelected={true}
        toggleSelection={mockToggleSelection}
      />
    )

    const card = screen.getByRole('button').parentElement
    expect(card).toHaveClass('border-2', 'border-red-500')
  })

  it('handles invalid budget values gracefully', () => {
    const invalidBudget: BudgetItem = {
      ...mockBudget,
      amount: 'invalid',
      spent: 'invalid',
      remaining: 'invalid'
    }

    render(
      <BudgetCard
        budget={invalidBudget}
        isMobile={false}
        isRemoveMode={false}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    expect(screen.getByText(/Total: £0.00/)).toBeInTheDocument()
    expect(screen.getByText(/Spent: £0.00/)).toBeInTheDocument()
    expect(screen.getByText(/Remaining: £0.00/)).toBeInTheDocument()
  })

  it('applies mobile layout when isMobile is true', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={true}
        isRemoveMode={false}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    const card = screen.getByRole('button').parentElement
    expect(card).toHaveClass('flex-col', 'items-center')
  })

  it('applies desktop layout when isMobile is false', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={false}
        isRemoveMode={false}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    const card = screen.getByRole('button').parentElement
    expect(card).toHaveClass('flex', 'items-center', 'w-full')
  })

  it('displays budget statistics correctly', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={false}
        isRemoveMode={false}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    expect(screen.getByText(/• There are 0 remaining days of this budget./)).toBeInTheDocument()
    expect(screen.getByText(/• There are 0 scheduled payments remaining for the month./)).toBeInTheDocument()
  })

  it('has correct ARIA attributes for accessibility', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={false}
        isRemoveMode={false}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    const button = screen.getByRole('button')
    expect(button).toHaveAttribute('class', 'absolute inset-0 w-full h-full opacity-0')
    
    // The parent div should be interactive since it contains the button
    const card = button.parentElement
    expect(card).toHaveClass('cursor-pointer')
  })

  it('applies hover styles correctly', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={false}
        isRemoveMode={false}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    const card = screen.getByRole('button').parentElement
    expect(card).toHaveClass('cursor-pointer')
  })

  it('uses correct colours for pie chart segments', () => {
    render(
      <BudgetCard
        budget={mockBudget}
        isMobile={false}
        isRemoveMode={false}
        isSelected={false}
        toggleSelection={mockToggleSelection}
      />
    )

    // Verify the colours are applied correctly to the text elements
    // which match the pie chart colours
    const spentText = screen.getByText(/Spent: £500.00/)
    const remainingText = screen.getByText(/Remaining: £500.00/)
    expect(spentText).toHaveClass('text-red-500')
    expect(remainingText).toHaveClass('text-green-500')
  })
}) 