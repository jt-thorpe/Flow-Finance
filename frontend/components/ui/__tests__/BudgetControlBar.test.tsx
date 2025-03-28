import { render, screen, fireEvent } from '@testing-library/react'
import BudgetControls from '../BudgetControlBar'

describe('BudgetControls', () => {
  const mockOnAdd = jest.fn()
  const mockOnToggleRemove = jest.fn()
  const mockOnConfirmRemove = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders add and remove buttons in normal mode', () => {
    render(
      <BudgetControls
        onAdd={mockOnAdd}
        onToggleRemove={mockOnToggleRemove}
        isRemoveMode={false}
        selectedCount={0}
        onConfirmRemove={mockOnConfirmRemove}
      />
    )

    const addButton = screen.getByRole('button', { name: '+' })
    const removeButton = screen.getByRole('button', { name: '-' })
    
    expect(addButton).toBeInTheDocument()
    expect(removeButton).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Remove' })).not.toBeInTheDocument()
  })

  it('renders add, cancel, and remove buttons in remove mode with selections', () => {
    render(
      <BudgetControls
        onAdd={mockOnAdd}
        onToggleRemove={mockOnToggleRemove}
        isRemoveMode={true}
        selectedCount={2}
        onConfirmRemove={mockOnConfirmRemove}
      />
    )

    const addButton = screen.getByRole('button', { name: '+' })
    const cancelButton = screen.getByRole('button', { name: 'Cancel' })
    const removeButton = screen.getByRole('button', { name: 'Remove' })
    
    expect(addButton).toBeInTheDocument()
    expect(cancelButton).toBeInTheDocument()
    expect(removeButton).toBeInTheDocument()
  })

  it('renders add and cancel buttons in remove mode without selections', () => {
    render(
      <BudgetControls
        onAdd={mockOnAdd}
        onToggleRemove={mockOnToggleRemove}
        isRemoveMode={true}
        selectedCount={0}
        onConfirmRemove={mockOnConfirmRemove}
      />
    )

    const addButton = screen.getByRole('button', { name: '+' })
    const cancelButton = screen.getByRole('button', { name: 'Cancel' })
    
    expect(addButton).toBeInTheDocument()
    expect(cancelButton).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Remove' })).not.toBeInTheDocument()
  })

  it('calls onAdd when add button is clicked', () => {
    render(
      <BudgetControls
        onAdd={mockOnAdd}
        onToggleRemove={mockOnToggleRemove}
        isRemoveMode={false}
        selectedCount={0}
        onConfirmRemove={mockOnConfirmRemove}
      />
    )

    const addButton = screen.getByRole('button', { name: '+' })
    fireEvent.click(addButton)
    
    expect(mockOnAdd).toHaveBeenCalledTimes(1)
  })

  it('calls onToggleRemove when remove/cancel button is clicked', () => {
    render(
      <BudgetControls
        onAdd={mockOnAdd}
        onToggleRemove={mockOnToggleRemove}
        isRemoveMode={false}
        selectedCount={0}
        onConfirmRemove={mockOnConfirmRemove}
      />
    )

    const removeButton = screen.getByRole('button', { name: '-' })
    fireEvent.click(removeButton)
    
    expect(mockOnToggleRemove).toHaveBeenCalledTimes(1)
  })

  it('calls onConfirmRemove when remove button is clicked in remove mode', () => {
    render(
      <BudgetControls
        onAdd={mockOnAdd}
        onToggleRemove={mockOnToggleRemove}
        isRemoveMode={true}
        selectedCount={2}
        onConfirmRemove={mockOnConfirmRemove}
      />
    )

    const removeButton = screen.getByRole('button', { name: 'Remove' })
    fireEvent.click(removeButton)
    
    expect(mockOnConfirmRemove).toHaveBeenCalledTimes(1)
  })

  it('applies correct styling classes', () => {
    render(
      <BudgetControls
        onAdd={mockOnAdd}
        onToggleRemove={mockOnToggleRemove}
        isRemoveMode={true}
        selectedCount={2}
        onConfirmRemove={mockOnConfirmRemove}
      />
    )

    // Check container
    const container = screen.getByRole('button', { name: 'Cancel' }).parentElement
    expect(container).toHaveClass('flex', 'justify-center', 'mb-4', 'gap-4')

    // Check normal buttons
    const addButton = screen.getByRole('button', { name: '+' })
    const cancelButton = screen.getByRole('button', { name: 'Cancel' })
    expect(addButton).toHaveClass('bg-green-400', 'text-white', 'px-4', 'py-2', 'rounded-md')
    expect(cancelButton).toHaveClass('bg-green-400', 'text-white', 'px-4', 'py-2', 'rounded-md')

    // Check remove button
    const removeButton = screen.getByRole('button', { name: 'Remove' })
    expect(removeButton).toHaveClass('bg-red-700', 'text-white', 'px-4', 'py-2', 'rounded-md')
  })

  it('has accessible button names', () => {
    render(
      <BudgetControls
        onAdd={mockOnAdd}
        onToggleRemove={mockOnToggleRemove}
        isRemoveMode={true}
        selectedCount={2}
        onConfirmRemove={mockOnConfirmRemove}
      />
    )

    expect(screen.getByRole('button', { name: '+' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Cancel' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Remove' })).toBeInTheDocument()
  })
}) 