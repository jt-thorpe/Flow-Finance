'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { FiMenu } from 'react-icons/fi';

const Navbar = () => {
    const pathname = usePathname();
    const [isOpen, setIsOpen] = useState(false);

    const navItems = [
        { name: 'Dashboard', path: '/dashboard' },
        { name: 'Transactions', path: '/transactions' },
        { name: 'Budgets', path: '/budgets' },
        { name: 'Insights', path: '/insights' },
        { name: 'Settings', path: '/settings' },
    ];

    return (
        <div>
            {/* Mobile Menu Button */}
            <button
                className="md:hidden p-4 text-gray-700 focus:outline-none"
                onClick={() => setIsOpen(!isOpen)}
            >
                <FiMenu size={24} />
            </button>

            {/* Sidebar Navigation */}
            <nav className={`bg-white shadow-md p-4 h-screen w-64 flex flex-col fixed left-0 top-0 transition-transform duration-300 md:translate-x-0 ${isOpen ? 'translate-x-0' : '-translate-x-full'} md:relative md:flex md:w-64`}>
                <ul className="flex flex-col space-y-4">
                    {navItems.map((item) => (
                        <li key={item.path}>
                            <Link href={item.path}>
                                <span className={`block px-4 py-2 rounded-lg text-gray-700 hover:bg-gray-200 transition ${pathname === item.path ? 'bg-green-400 text-white' : ''}`}>
                                    {item.name}
                                </span>
                            </Link>
                        </li>
                    ))}
                </ul>
            </nav>
        </div>
    );
};

export default Navbar;
