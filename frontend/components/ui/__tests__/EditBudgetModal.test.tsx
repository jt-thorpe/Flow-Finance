import { render, screen, fireEvent } from '@testing-library/react'
import EditBudgetModal from '../EditBudgetModal'
import BudgetItem from '../../../types/BudgetItem'

describe('EditBudgetModal', () => {
  const mockBudget: BudgetItem = {
    id: '1',
    user_id: '1',
    category: 'Groceries',
    amount: '1000',
    spent: '500',
    remaining: '500',
    frequency: 'Monthly'
  }

  const mockOnSave = jest.fn()
  const mockOnCancel = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders with initial budget data', () => {
    render(
      <EditBudgetModal
        budget={mockBudget}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    )

    // Check modal title
    expect(screen.getByText('Edit Budget')).toBeInTheDocument()

    // Check form fields have initial values
    expect(screen.getByLabelText(/category/i)).toHaveValue('Groceries')
    expect(screen.getByLabelText(/total amount/i)).toHaveValue(1000)
    expect(screen.getByLabelText(/spent/i)).toHaveValue(500)
    expect(screen.getByLabelText(/frequency/i)).toHaveValue('Monthly')

    // Check buttons
    expect(screen.getByRole('button', { name: /save/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument()
  })

  it('updates form fields when user types', () => {
    render(
      <EditBudgetModal
        budget={mockBudget}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    )

    // Update category
    fireEvent.change(screen.getByLabelText(/category/i), { target: { value: 'Food' } })
    expect(screen.getByLabelText(/category/i)).toHaveValue('Food')

    // Update amount
    fireEvent.change(screen.getByLabelText(/total amount/i), { target: { value: '2000' } })
    expect(screen.getByLabelText(/total amount/i)).toHaveValue(2000)

    // Update spent
    fireEvent.change(screen.getByLabelText(/spent/i), { target: { value: '1000' } })
    expect(screen.getByLabelText(/spent/i)).toHaveValue(1000)

    // Update frequency
    fireEvent.change(screen.getByLabelText(/frequency/i), { target: { value: 'Weekly' } })
    expect(screen.getByLabelText(/frequency/i)).toHaveValue('Weekly')
  })

  it('calls onSave with updated budget when save button is clicked', () => {
    render(
      <EditBudgetModal
        budget={mockBudget}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    )

    // Update all fields
    fireEvent.change(screen.getByLabelText(/category/i), { target: { value: 'Food' } })
    fireEvent.change(screen.getByLabelText(/total amount/i), { target: { value: '1500' } })
    fireEvent.change(screen.getByLabelText(/spent/i), { target: { value: '750' } })
    fireEvent.change(screen.getByLabelText(/frequency/i), { target: { value: 'Weekly' } })

    // Click save
    fireEvent.click(screen.getByRole('button', { name: /save/i }))

    // Check if onSave was called with updated values
    expect(mockOnSave).toHaveBeenCalledTimes(1)
    expect(mockOnSave).toHaveBeenCalledWith({
      ...mockBudget,
      category: 'Food',
      amount: '1500',
      spent: '750',
      frequency: 'Weekly'
    })
  })

  it('calls onCancel when cancel button is clicked', () => {
    render(
      <EditBudgetModal
        budget={mockBudget}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    )

    fireEvent.click(screen.getByRole('button', { name: /cancel/i }))
    expect(mockOnCancel).toHaveBeenCalledTimes(1)
  })

  it('prevents event propagation when clicking modal content', () => {
    render(
      <EditBudgetModal
        budget={mockBudget}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    )

    const modalOverlay = screen.getByTestId('modal-overlay')
    const dialogContent = screen.getByRole('dialog')

    // Click the dialog content
    fireEvent.click(dialogContent)

    // The onCancel should not be called when clicking the dialog content
    expect(mockOnCancel).not.toHaveBeenCalled()

    // Click the overlay
    fireEvent.click(modalOverlay)

    // The onCancel should be called when clicking the overlay
    expect(mockOnCancel).toHaveBeenCalledTimes(1)
  })

  it('applies correct styling classes', () => {
    render(
      <EditBudgetModal
        budget={mockBudget}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    )

    // Check modal overlay
    const overlay = screen.getByTestId('modal-overlay')
    expect(overlay).toHaveClass(
      'fixed',
      'inset-0',
      'flex',
      'items-center',
      'justify-center',
      'bg-black',
      'bg-opacity-50',
      'z-50'
    )

    // Check modal content
    const content = screen.getByRole('dialog')
    expect(content).toHaveClass(
      'bg-white',
      'p-6',
      'rounded-md',
      'shadow-md',
      'w-full',
      'max-w-md'
    )

    // Check form inputs
    const inputs = screen.getAllByRole('textbox')
    inputs.forEach(input => {
      expect(input).toHaveClass(
        'border',
        'border-gray-300',
        'p-2',
        'rounded-md',
        'w-full'
      )
    })

    // Check buttons
    const saveButton = screen.getByRole('button', { name: /save/i })
    expect(saveButton).toHaveClass('bg-green-400', 'text-white', 'px-4', 'py-2', 'rounded-md')

    const cancelButton = screen.getByRole('button', { name: /cancel/i })
    expect(cancelButton).toHaveClass('bg-gray-500', 'text-white', 'px-4', 'py-2', 'rounded-md')
  })

  it('has correct form field types', () => {
    render(
      <EditBudgetModal
        budget={mockBudget}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    )

    expect(screen.getByLabelText(/category/i)).toHaveAttribute('type', 'text')
    expect(screen.getByLabelText(/total amount/i)).toHaveAttribute('type', 'number')
    expect(screen.getByLabelText(/spent/i)).toHaveAttribute('type', 'number')
    expect(screen.getByLabelText(/frequency/i)).toHaveAttribute('type', 'text')
  })

  it('maintains accessibility attributes', () => {
    render(
      <EditBudgetModal
        budget={mockBudget}
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    )

    // Check modal role
    expect(screen.getByRole('dialog')).toBeInTheDocument()

    // Check form labels are properly associated with inputs
    const labels = screen.getAllByText(/category|total amount|spent|frequency/i)
    labels.forEach(label => {
      const input = label.nextElementSibling
      expect(input).toHaveAttribute('name')
    })

    // Check button types
    const buttons = screen.getAllByRole('button')
    expect(buttons[0]).toHaveAttribute('type', 'submit')
    expect(buttons[1]).toHaveAttribute('type', 'button')
  })

  describe('Form Validation', () => {
    it('prevents saving with empty category', () => {
      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      const categoryInput = screen.getByLabelText(/category/i)
      fireEvent.change(categoryInput, { target: { value: '' } })
      fireEvent.click(screen.getByRole('button', { name: /save/i }))

      expect(mockOnSave).not.toHaveBeenCalled()
    })

    it('prevents negative numbers in amount and spent fields', () => {
      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      const amountInput = screen.getByLabelText(/total amount/i)
      const spentInput = screen.getByLabelText(/spent/i)

      fireEvent.change(amountInput, { target: { value: '-100' } })
      fireEvent.change(spentInput, { target: { value: '-50' } })

      expect(amountInput).toHaveValue(0)
      expect(spentInput).toHaveValue(0)
    })

    it('prevents special characters in category and frequency', () => {
      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      const categoryInput = screen.getByLabelText(/category/i)
      const frequencyInput = screen.getByLabelText(/frequency/i)

      fireEvent.change(categoryInput, { target: { value: 'Food@#$%' } })
      fireEvent.change(frequencyInput, { target: { value: 'Weekly@#$%' } })

      expect(categoryInput).toHaveValue('Food')
      expect(frequencyInput).toHaveValue('Weekly')
    })
  })

  describe('Keyboard Navigation', () => {
    it('closes modal on escape key', () => {
      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      fireEvent.keyDown(document, { key: 'Escape' })
      expect(mockOnCancel).toHaveBeenCalledTimes(1)
    })

    it('submits form on enter key', () => {
      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      const form = screen.getByRole('dialog').querySelector('form')
      fireEvent.submit(form!)
      expect(mockOnSave).toHaveBeenCalledTimes(1)
    })

    it('maintains correct tab order', () => {
      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      const categoryInput = screen.getByLabelText(/category/i)
      const amountInput = screen.getByLabelText(/total amount/i)
      const spentInput = screen.getByLabelText(/spent/i)
      const frequencyInput = screen.getByLabelText(/frequency/i)
      const saveButton = screen.getByRole('button', { name: /save/i })
      const cancelButton = screen.getByRole('button', { name: /cancel/i })

      expect(categoryInput).toHaveAttribute('tabIndex', '0')
      expect(amountInput).toHaveAttribute('tabIndex', '1')
      expect(spentInput).toHaveAttribute('tabIndex', '2')
      expect(frequencyInput).toHaveAttribute('tabIndex', '3')
      expect(saveButton).toHaveAttribute('tabIndex', '4')
      expect(cancelButton).toHaveAttribute('tabIndex', '5')
    })
  })

  describe('Error Handling', () => {
    it('handles invalid budget data gracefully', () => {
      const invalidBudget = {
        ...mockBudget,
        amount: 'invalid',
        spent: 'invalid'
      }

      render(
        <EditBudgetModal
          budget={invalidBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      const amountInput = screen.getByLabelText(/total amount/i)
      const spentInput = screen.getByLabelText(/spent/i)

      expect(amountInput).toHaveValue(0)
      expect(spentInput).toHaveValue(0)
    })

    it('handles failed save operations', () => {
      mockOnSave.mockImplementationOnce(() => {
        throw new Error('Save failed');
      });

      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      );

      fireEvent.click(screen.getByRole('button', { name: /save/i }));
      expect(mockOnSave).toHaveBeenCalledTimes(1);
    })
  })

  describe('State Management', () => {
    it('resets state when modal is reopened', () => {
      const { rerender } = render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      // Make some changes
      fireEvent.change(screen.getByLabelText(/category/i), { target: { value: 'Food' } })

      // Rerender with a new budget to simulate reopening
      const newBudget = {
        ...mockBudget,
        category: 'Groceries',
        amount: '1000',
        spent: '500',
        frequency: 'Monthly'
      }

      rerender(
        <EditBudgetModal
          budget={newBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      // Check if state is reset
      expect(screen.getByLabelText(/category/i)).toHaveValue('Groceries')
    })

    it('updates state when props change', () => {
      const newBudget = {
        ...mockBudget,
        category: 'Food',
        amount: '2000',
        spent: '1000',
        frequency: 'Weekly'
      }

      const { rerender } = render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      // Rerender with new props
      rerender(
        <EditBudgetModal
          budget={newBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      expect(screen.getByLabelText(/category/i)).toHaveValue('Food')
      expect(screen.getByLabelText(/total amount/i)).toHaveValue(2000)
      expect(screen.getByLabelText(/spent/i)).toHaveValue(1000)
      expect(screen.getByLabelText(/frequency/i)).toHaveValue('Weekly')
    })
  })

  describe('Edge Cases', () => {
    it('handles very large numbers', () => {
      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      const amountInput = screen.getByLabelText(/total amount/i)
      const spentInput = screen.getByLabelText(/spent/i)

      fireEvent.change(amountInput, { target: { value: '999999999999' } })
      fireEvent.change(spentInput, { target: { value: '999999999999' } })

      expect(amountInput).toHaveValue(999999999999)
      expect(spentInput).toHaveValue(999999999999)
    })

    it('handles very long text in category and frequency', () => {
      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      const categoryInput = screen.getByLabelText(/category/i)
      const frequencyInput = screen.getByLabelText(/frequency/i)

      const longText = 'a'.repeat(100)
      fireEvent.change(categoryInput, { target: { value: longText } })
      fireEvent.change(frequencyInput, { target: { value: longText } })

      expect(categoryInput).toHaveValue(longText)
      expect(frequencyInput).toHaveValue(longText)
    })

    it('handles different screen sizes', () => {
      render(
        <EditBudgetModal
          budget={mockBudget}
          onSave={mockOnSave}
          onCancel={mockOnCancel}
        />
      )

      const content = screen.getByRole('dialog')
      expect(content).toHaveClass('max-w-md')
      expect(content).toHaveClass('w-full')
    })
  })
}) 