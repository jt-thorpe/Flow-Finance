import { render, screen, fireEvent } from '@testing-library/react'
import AddBudgetModal from '../AddBudgetModal'
import BudgetItem from '../../../types/BudgetItem'

describe('AddBudgetModal', () => {
  const mockOnSave = jest.fn()
  const mockOnCancel = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders the modal with all form fields', () => {
    render(<AddBudgetModal onSave={mockOnSave} onCancel={mockOnCancel} />)
    
    expect(screen.getByText(/add new budget/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/category/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/total amount/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/spent/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/frequency/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /save/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument()
  })

  it('updates form fields when user types', () => {
    render(<AddBudgetModal onSave={mockOnSave} onCancel={mockOnCancel} />)
    
    const categoryInput = screen.getByLabelText(/category/i)
    const amountInput = screen.getByLabelText(/total amount/i)
    const spentInput = screen.getByLabelText(/spent/i)
    const frequencyInput = screen.getByLabelText(/frequency/i)

    fireEvent.change(categoryInput, { target: { value: 'Groceries' } })
    fireEvent.change(amountInput, { target: { value: '500' } })
    fireEvent.change(spentInput, { target: { value: '200' } })
    fireEvent.change(frequencyInput, { target: { value: 'Monthly' } })

    expect(categoryInput).toHaveValue('Groceries')
    expect(amountInput).toHaveValue(500)
    expect(spentInput).toHaveValue(200)
    expect(frequencyInput).toHaveValue('Monthly')
  })

  it('calls onSave with form data when save button is clicked', () => {
    render(<AddBudgetModal onSave={mockOnSave} onCancel={mockOnCancel} />)
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText(/category/i), { target: { value: 'Groceries' } })
    fireEvent.change(screen.getByLabelText(/total amount/i), { target: { value: '500' } })
    fireEvent.change(screen.getByLabelText(/spent/i), { target: { value: '200' } })
    fireEvent.change(screen.getByLabelText(/frequency/i), { target: { value: 'Monthly' } })

    // Click save button
    fireEvent.click(screen.getByRole('button', { name: /save/i }))

    // Verify onSave was called with the correct data
    expect(mockOnSave).toHaveBeenCalledTimes(1)
    const savedBudget = mockOnSave.mock.calls[0][0]
    expect(savedBudget).toMatchObject({
      category: 'Groceries',
      amount: 500,
      spent: 200,
      frequency: 'Monthly',
      remaining: 0,
    })
    expect(savedBudget.id).toBeDefined()
  })

  it('calls onCancel when cancel button is clicked', () => {
    render(<AddBudgetModal onSave={mockOnSave} onCancel={mockOnCancel} />)
    
    fireEvent.click(screen.getByRole('button', { name: /cancel/i }))
    
    expect(mockOnCancel).toHaveBeenCalledTimes(1)
  })

  it('handles numeric input correctly', () => {
    render(<AddBudgetModal onSave={mockOnSave} onCancel={mockOnCancel} />)
    
    const amountInput = screen.getByLabelText(/total amount/i)
    const spentInput = screen.getByLabelText(/spent/i)

    // Test decimal numbers
    fireEvent.change(amountInput, { target: { value: '500.50' } })
    fireEvent.change(spentInput, { target: { value: '200.75' } })

    expect(amountInput).toHaveValue(500.5)
    expect(spentInput).toHaveValue(200.75)
  })
}) 