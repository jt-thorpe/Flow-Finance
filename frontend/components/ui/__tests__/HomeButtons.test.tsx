import { render, screen } from '@testing-library/react'
import AuthButtons from '../HomeButtons'

// Mock next/image since it's not available in the test environment
jest.mock('next/image', () => ({
  __esModule: true,
  default: (props: any) => {
    // eslint-disable-next-line @next/next/no-img-element
    return <img {...props} />
  },
}))

// Mock next/link to use a regular anchor tag
jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  ),
}))

describe('AuthButtons', () => {
  it('renders both register and login buttons', () => {
    render(<AuthButtons />)
    
    const registerLink = screen.getByRole('link', { name: /vercel logomark register/i })
    const loginLink = screen.getByRole('link', { name: /vercel logomark login/i })
    
    expect(registerLink).toBeInTheDocument()
    expect(loginLink).toBeInTheDocument()
  })

  it('has correct href attributes', () => {
    render(<AuthButtons />)
    
    const registerLink = screen.getByRole('link', { name: /vercel logomark register/i })
    const loginLink = screen.getByRole('link', { name: /vercel logomark login/i })
    
    expect(registerLink).toHaveAttribute('href', '/register')
    expect(loginLink).toHaveAttribute('href', '/login')
  })

  it('renders Vercel logo images', () => {
    render(<AuthButtons />)
    
    const images = screen.getAllByRole('img', { name: 'Vercel logomark' })
    expect(images).toHaveLength(2)
    
    images.forEach(img => {
      expect(img).toHaveAttribute('src', '/vercel.svg')
      expect(img).toHaveAttribute('width', '20')
      expect(img).toHaveAttribute('height', '20')
      expect(img).toHaveClass('dark:invert')
    })
  })

  it('renders with correct structure', () => {
    render(<AuthButtons />)
    
    // Check container exists
    const container = screen.getByRole('link', { name: /vercel logomark register/i }).parentElement
    expect(container).toBeTruthy()
    
    // Check links contain images and text
    const links = screen.getAllByRole('link')
    links.forEach(link => {
      const image = link.querySelector('img')
      expect(image).toBeInTheDocument()
      expect(image).toHaveAttribute('alt', 'Vercel logomark')
      
      // Verify text content is present
      const text = link.textContent
      expect(text).toMatch(/register|login/i)
    })
  })

  it('has accessible names including image alt text', () => {
    render(<AuthButtons />)
    
    const registerLink = screen.getByRole('link', { name: /vercel logomark register/i })
    const loginLink = screen.getByRole('link', { name: /vercel logomark login/i })
    
    expect(registerLink).toHaveAccessibleName('Vercel logomark Register')
    expect(loginLink).toHaveAccessibleName('Vercel logomark Login')
  })

  it('renders in a container', () => {
    render(<AuthButtons />)
    
    const container = screen.getByRole('link', { name: /vercel logomark register/i }).parentElement
    expect(container).toBeTruthy()
  })

  it('maintains consistent button order', () => {
    render(<AuthButtons />)
    
    const links = screen.getAllByRole('link')
    expect(links[0]).toHaveAccessibleName('Vercel logomark Register')
    expect(links[1]).toHaveAccessibleName('Vercel logomark Login')
  })
}) 