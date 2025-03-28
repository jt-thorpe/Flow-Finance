import { render, screen } from '@testing-library/react'
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '../table'

describe('Table Components', () => {
  describe('Table', () => {
    it('renders children correctly', () => {
      render(
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Test Content</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      )

      expect(screen.getByText('Test Content')).toBeInTheDocument()
    })

    it('applies correct styling classes', () => {
      render(
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Content</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      )

      const table = screen.getByText('Content').closest('table')
      expect(table).toHaveClass('w-full', 'border-collapse', 'border', 'border-gray-300')
    })
  })

  describe('TableHeader', () => {
    it('renders children correctly', () => {
      render(
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Test Content</TableHead>
            </TableRow>
          </TableHeader>
        </Table>
      )

      expect(screen.getByText('Test Content')).toBeInTheDocument()
    })

    it('applies correct styling classes', () => {
      render(
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Content</TableHead>
            </TableRow>
          </TableHeader>
        </Table>
      )

      const header = screen.getByText('Content').closest('thead')
      expect(header).toHaveClass('bg-gray-200')
    })
  })

  describe('TableRow', () => {
    it('renders children correctly', () => {
      render(
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Test Content</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      )

      expect(screen.getByText('Test Content')).toBeInTheDocument()
    })

    it('applies correct styling classes', () => {
      render(
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Content</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      )

      const row = screen.getByText('Content').closest('tr')
      expect(row).toHaveClass('border-b', 'border-gray-300')
    })

    it('applies additional className when provided', () => {
      render(
        <Table>
          <TableBody>
            <TableRow className="custom-class">
              <TableCell>Content</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      )

      const row = screen.getByText('Content').closest('tr')
      expect(row).toHaveClass('custom-class')
    })
  })

  describe('TableHead', () => {
    it('renders children correctly', () => {
      render(
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Test Content</TableHead>
            </TableRow>
          </TableHeader>
        </Table>
      )

      expect(screen.getByText('Test Content')).toBeInTheDocument()
    })

    it('applies correct styling classes', () => {
      render(
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Content</TableHead>
            </TableRow>
          </TableHeader>
        </Table>
      )

      const head = screen.getByText('Content').closest('th')
      expect(head).toHaveClass('p-2', 'text-left')
    })
  })

  describe('TableBody', () => {
    it('renders children correctly', () => {
      render(
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Test Content</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      )

      expect(screen.getByText('Test Content')).toBeInTheDocument()
    })
  })

  describe('TableCell', () => {
    it('renders children correctly', () => {
      render(
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Test Content</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      )

      expect(screen.getByText('Test Content')).toBeInTheDocument()
    })

    it('applies correct styling classes', () => {
      render(
        <Table>
          <TableBody>
            <TableRow>
              <TableCell>Content</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      )

      const cell = screen.getByText('Content').closest('td')
      expect(cell).toHaveClass('p-2', 'border-r', 'border-gray-300')
    })
  })

  describe('Table Components Integration', () => {
    it('renders a complete table structure correctly', () => {
      render(
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Header 1</TableHead>
              <TableHead>Header 2</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell>Cell 1</TableCell>
              <TableCell>Cell 2</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      )

      expect(screen.getByText('Header 1')).toBeInTheDocument()
      expect(screen.getByText('Header 2')).toBeInTheDocument()
      expect(screen.getByText('Cell 1')).toBeInTheDocument()
      expect(screen.getByText('Cell 2')).toBeInTheDocument()
    })
  })
}) 