'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import { FiLogOut, FiMenu, FiX } from 'react-icons/fi';
import { handleLogout } from '../../lib/auth';

const Navbar = () => {
    const pathname = usePathname();
    const [isMobile, setIsMobile] = useState(false);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
            if (window.innerWidth >= 768) {
                setIsOpen(false); // Ensure menu is closed when resizing back to desktop
            }
        };
        handleResize();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    const navItems = [
        { name: 'Dashboard', path: '/dashboard' },
        { name: 'Budgets', path: '/budgets' },
        { name: 'Transactions', path: '/transactions' },
        { name: 'Insights', path: '/insights' },
        { name: 'Settings', path: '/settings' },
    ];

    return (
        <div>
            {/* Mobile Menu Button */}
            {isMobile && (
                <button
                    className="p-4 text-gray-700 focus:outline-none fixed top-4 left-4 z-50 bg-white shadow-md rounded-full"
                    onClick={() => setIsOpen(!isOpen)}
                >
                    {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
                </button>
            )}

            {/* Fixed Sidebar Navigation on Desktop */}
            <nav className={`bg-white shadow-md h-screen w-64 fixed left-0 top-0 p-6 transition-transform duration-300 ${isMobile ? '-translate-x-full' : 'translate-x-0'}`}>
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

                {/* Logout Button (Desktop) */}
                <button onClick={handleLogout} className="flex items-center space-x-2 px-4 py-2 mt-auto text-gray-700 hover:bg-gray-200 rounded-lg transition">
                    <FiLogOut size={20} />
                    <span>Logout</span>
                </button>
            </nav>

            {/* Overlay Navigation (Floating Menu on Mobile) */}
            {isMobile && isOpen && (
                <>
                    <div className="fixed inset-0 bg-black bg-opacity-50 z-40" onClick={() => setIsOpen(false)}></div>
                    <nav className="fixed top-12 left-12 w-64 bg-white shadow-md z-50 p-6 rounded-lg">
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

                        {/* Logout Button (Mobile)) */}
                        <button onClick={handleLogout} className="flex items-center space-x-2 px-4 py-2 mt-auto text-gray-700 hover:bg-gray-200 rounded-lg transition">
                            <FiLogOut size={20} />
                            <span>Logout</span>
                        </button>
                    </nav>
                </>
            )}
        </div>
    );
};

export default Navbar;
