import { render, screen } from '@testing-library/react'
import Table from '../Table'

describe('Table', () => {
  const mockHeaders = ['Name', 'Amount', 'Date']
  const mockData = [
    ['Groceries', '£100.00', '2024-03-27'],
    ['Transport', '£50.00', '2024-03-28'],
  ]

  it('renders headers correctly', () => {
    render(<Table headers={mockHeaders} data={mockData} />)
    
    mockHeaders.forEach(header => {
      expect(screen.getByRole('columnheader', { name: header })).toBeInTheDocument()
    })
  })

  it('renders data rows correctly', () => {
    render(<Table headers={mockHeaders} data={mockData} />)
    
    // Get all rows except header
    const dataRows = screen.getAllByRole('row').slice(1)
    
    // Check each row's cells
    dataRows.forEach((row, rowIndex) => {
      const cells = row.querySelectorAll('td')
      cells.forEach((cell, cellIndex) => {
        expect(cell).toHaveTextContent(mockData[rowIndex][cellIndex])
      })
    })
  })

  it('displays "No data available" message when data is empty', () => {
    render(<Table headers={mockHeaders} data={[]} />)
    
    expect(screen.getByText('No data available.')).toBeInTheDocument()
  })

  it('applies correct styling classes', () => {
    render(<Table headers={mockHeaders} data={mockData} />)
    
    // Check table container
    expect(screen.getByRole('table').parentElement).toHaveClass('overflow-x-auto')
    
    // Check table element
    expect(screen.getByRole('table')).toHaveClass('w-full', 'border-collapse', 'text-left')
    
    // Check header row
    expect(screen.getByRole('row', { name: /name amount date/i })).toHaveClass('bg-gray-200')
    
    // Check header cells
    const headerCells = screen.getAllByRole('columnheader')
    headerCells.forEach(cell => {
      expect(cell).toHaveClass('p-3', 'font-semibold')
    })
    
    // Check data rows
    const dataRows = screen.getAllByRole('row').slice(1) // Skip header row
    dataRows.forEach(row => {
      expect(row).toHaveClass('border-t')
    })
    
    // Check data cells
    const dataCells = screen.getAllByRole('cell')
    dataCells.forEach(cell => {
      expect(cell).toHaveClass('p-3')
    })
  })

  it('has correct accessibility attributes', () => {
    render(<Table headers={mockHeaders} data={mockData} />)
    
    // Check table role
    expect(screen.getByRole('table')).toBeInTheDocument()
    
    // Check header cells have columnheader role
    const headerCells = screen.getAllByRole('columnheader')
    expect(headerCells).toHaveLength(mockHeaders.length)
    
    // Check data cells using rows
    const dataRows = screen.getAllByRole('row').slice(1) // Skip header row
    dataRows.forEach(row => {
      const cells = row.querySelectorAll('td')
      expect(cells).toHaveLength(mockHeaders.length)
    })
    
    // Check total number of data cells
    const dataCells = screen.getAllByRole('cell')
    expect(dataCells).toHaveLength(mockData.length * mockHeaders.length)
  })

  it('handles different data types in cells', () => {
    const mixedData = [
      ['Cell Text', '123', 'true', 'null', 'undefined'],
    ]
    const mixedHeaders = ['Text', 'Number', 'Boolean', 'Null', 'Undefined']
    
    render(<Table headers={mixedHeaders} data={mixedData} />)
    
    // Get the first data row
    const dataRow = screen.getAllByRole('row')[1]
    const cells = dataRow.querySelectorAll('td')
    
    // Check each cell's content
    cells.forEach((cell, index) => {
      expect(cell).toHaveTextContent(mixedData[0][index])
    })
  })

  it('spans empty state message across all columns', () => {
    render(<Table headers={mockHeaders} data={[]} />)
    
    const emptyCell = screen.getByText('No data available.').closest('td')
    expect(emptyCell).toHaveAttribute('colSpan', mockHeaders.length.toString())
  })
}) 