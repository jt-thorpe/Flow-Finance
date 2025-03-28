// NavBar.test.tsx
import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import Navbar from '../NavBar';
import { usePathname } from 'next/navigation';
import { handleLogout } from '../../../lib/auth';

jest.mock('next/navigation', () => ({
  usePathname: jest.fn(),
}));

jest.mock('../../../lib/auth', () => ({
  handleLogout: jest.fn(),
}));

describe('Navbar', () => {
  beforeEach(() => {
    // Set desktop view as default.
    (window as any).innerWidth = 1024;
    act(() => window.dispatchEvent(new Event('resize')));
    (usePathname as jest.Mock).mockReturnValue('/dashboard');
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('renders desktop navigation', () => {
    render(<Navbar />);
    const nav = screen.getByRole('navigation');
    expect(nav).toHaveClass('translate-x-0'); // visible in desktop view
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Budgets')).toBeInTheDocument();
    // Mobile menu button should not appear in desktop.
    expect(screen.queryByRole('button', { name: /menu/i })).not.toBeInTheDocument();
  });

  test('renders mobile menu and toggles overlay', () => {
    // Simulate mobile view.
    (window as any).innerWidth = 500;
    act(() => window.dispatchEvent(new Event('resize')));
    render(<Navbar />);
    const menuButton = screen.getByTestId('mobile-menu-button');
    expect(menuButton).toBeInTheDocument();
    // Initially, overlay should not be present.
    expect(screen.queryByTestId('mobile-overlay')).not.toBeInTheDocument();
    
    // Open mobile menu.
    fireEvent.click(menuButton);
    expect(screen.getByTestId('mobile-overlay')).toBeInTheDocument();
    
    // Click overlay to close menu.
    fireEvent.click(screen.getByTestId('mobile-overlay'));
    expect(screen.queryByTestId('mobile-overlay')).not.toBeInTheDocument();
  });

  test('active nav item is highlighted', () => {
    (usePathname as jest.Mock).mockReturnValue('/transactions');
    render(<Navbar />);
    const activeLink = screen.getByText('Transactions');
    expect(activeLink).toHaveClass('bg-green-400');
    expect(activeLink).toHaveClass('text-white');
  });

  test('clicking logout button calls handleLogout', () => {
    render(<Navbar />);
    const logoutButton = screen.getByText('Logout');
    fireEvent.click(logoutButton);
    expect(handleLogout).toHaveBeenCalled();
  });
});
