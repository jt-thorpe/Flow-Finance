import { render, screen } from '@testing-library/react'
import { Card, CardContent } from '../card'

describe('Card Components', () => {
  describe('Card', () => {
    it('renders children correctly', () => {
      render(
        <Card>
          <div data-testid="test-child">Test Content</div>
        </Card>
      )

      expect(screen.getByTestId('test-child')).toBeInTheDocument()
      expect(screen.getByTestId('test-child').textContent).toBe('Test Content')
    })

    it('applies correct styling classes', () => {
      render(
        <Card>
          <div>Content</div>
        </Card>
      )

      const card = screen.getByText('Content').parentElement
      expect(card).toHaveClass('bg-white', 'shadow-md', 'rounded-lg', 'p-4')
    })

    it('renders with multiple children', () => {
      render(
        <Card>
          <div data-testid="child-1">First Child</div>
          <div data-testid="child-2">Second Child</div>
        </Card>
      )

      expect(screen.getByTestId('child-1')).toBeInTheDocument()
      expect(screen.getByTestId('child-2')).toBeInTheDocument()
    })
  })

  describe('CardContent', () => {
    it('renders children correctly', () => {
      render(
        <CardContent>
          <div data-testid="test-child">Test Content</div>
        </CardContent>
      )

      expect(screen.getByTestId('test-child')).toBeInTheDocument()
      expect(screen.getByTestId('test-child').textContent).toBe('Test Content')
    })

    it('applies correct styling classes', () => {
      render(
        <CardContent>
          <div>Content</div>
        </CardContent>
      )

      const content = screen.getByText('Content').parentElement
      expect(content).toHaveClass('p-2')
    })

    it('renders with multiple children', () => {
      render(
        <CardContent>
          <div data-testid="child-1">First Child</div>
          <div data-testid="child-2">Second Child</div>
        </CardContent>
      )

      expect(screen.getByTestId('child-1')).toBeInTheDocument()
      expect(screen.getByTestId('child-2')).toBeInTheDocument()
    })

    it('can be nested inside Card', () => {
      render(
        <Card>
          <CardContent>
            <div data-testid="nested-content">Nested Content</div>
          </CardContent>
        </Card>
      )

      expect(screen.getByTestId('nested-content')).toBeInTheDocument()
      expect(screen.getByTestId('nested-content').textContent).toBe('Nested Content')
    })
  })
}) 