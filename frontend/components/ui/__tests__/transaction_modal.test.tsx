import { render, screen, fireEvent } from '@testing-library/react'
import { TransactionModal } from '../transaction_modal'

describe('TransactionModal', () => {
  const mockOnClose = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders children correctly', () => {
    render(
      <TransactionModal onClose={mockOnClose}>
        <div data-testid="test-child">Test Content</div>
      </TransactionModal>
    )

    expect(screen.getByTestId('test-child')).toBeInTheDocument()
    expect(screen.getByTestId('test-child').textContent).toBe('Test Content')
  })

  it('applies correct styling classes', () => {
    render(
      <TransactionModal onClose={mockOnClose}>
        <div>Content</div>
      </TransactionModal>
    )

    // Check overlay styling
    const overlay = screen.getByText('Content').parentElement?.parentElement
    expect(overlay).toHaveClass(
      'fixed',
      'inset-0',
      'bg-black',
      'bg-opacity-50',
      'flex',
      'justify-center',
      'items-center',
      'z-50'
    )

    // Check modal content styling
    const modalContent = screen.getByText('Content').parentElement
    expect(modalContent).toHaveClass(
      'bg-white',
      'rounded-lg',
      'shadow-lg',
      'p-6',
      'relative',
      'w-1/3'
    )

    // Check close button styling
    const closeButton = screen.getByText('✖')
    expect(closeButton).toHaveClass(
      'absolute',
      'top-2',
      'right-2',
      'text-gray-500',
      'hover:text-gray-700'
    )
  })

  it('calls onClose when close button is clicked', () => {
    render(
      <TransactionModal onClose={mockOnClose}>
        <div>Content</div>
      </TransactionModal>
    )

    const closeButton = screen.getByText('✖')
    fireEvent.click(closeButton)
    expect(mockOnClose).toHaveBeenCalledTimes(1)
  })

  it('renders with multiple children', () => {
    render(
      <TransactionModal onClose={mockOnClose}>
        <div data-testid="child-1">First Child</div>
        <div data-testid="child-2">Second Child</div>
      </TransactionModal>
    )

    expect(screen.getByTestId('child-1')).toBeInTheDocument()
    expect(screen.getByTestId('child-2')).toBeInTheDocument()
  })

  it('maintains proper z-index and positioning', () => {
    render(
      <TransactionModal onClose={mockOnClose}>
        <div>Content</div>
      </TransactionModal>
    )

    const overlay = screen.getByText('Content').parentElement?.parentElement
    expect(overlay).toHaveClass('z-50')
    expect(overlay).toHaveClass('fixed', 'inset-0')
  })
}) 