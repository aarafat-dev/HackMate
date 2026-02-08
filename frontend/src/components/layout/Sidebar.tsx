/**
 * HackMate v2.0 - Sidebar Component
 * Main navigation sidebar with hacker aesthetic.
 */

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
    Shield,
    Target,
    Terminal,
    Bug,
    Radar,
    FileText,
    MessageSquare,
    Settings,
    Plus,
} from 'lucide-react';

interface NavItem {
    name: string;
    href: string;
    icon: React.ReactNode;
}

const navigation: NavItem[] = [
    { name: 'Dashboard', href: '/', icon: <Shield size={18} /> },
    { name: 'Engagements', href: '/engagements', icon: <Target size={18} /> },
];

const toolNavigation: NavItem[] = [
    { name: 'Terminal', href: '/terminal', icon: <Terminal size={18} /> },
    { name: 'Findings', href: '/findings', icon: <Bug size={18} /> },
    { name: 'Scans', href: '/scans', icon: <Radar size={18} /> },
    { name: 'Reports', href: '/reports', icon: <FileText size={18} /> },
    { name: 'AI Assistant', href: '/ai', icon: <MessageSquare size={18} /> },
];

export function Sidebar() {
    const pathname = usePathname();

    const NavLink = ({ item }: { item: NavItem }) => {
        const isActive = pathname === item.href ||
            (item.href !== '/' && pathname.startsWith(item.href));

        return (
            <Link
                href={item.href}
                className={cn(
                    'flex items-center gap-3 px-3 py-2.5 text-sm rounded transition-all',
                    isActive
                        ? 'bg-primary/20 text-primary glow border-l-2 border-primary'
                        : 'text-muted-foreground hover:text-primary hover:bg-primary/10'
                )}
            >
                {item.icon}
                <span>{item.name}</span>
            </Link>
        );
    };

    return (
        <aside className="w-64 h-screen bg-black/50 backdrop-blur-sm border-r border-primary/20 flex flex-col">
            {/* Logo */}
            <div className="p-4 border-b border-primary/20">
                <Link href="/" className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-primary/20 rounded border border-primary/50 flex items-center justify-center overflow-hidden">
                        <img
                            src="/logo.png"
                            alt="HackMate Logo"
                            className="w-full h-full object-cover"
                        />
                    </div>
                    <div>
                        <h1 className="text-primary font-bold text-lg tracking-wider">HACKMATE</h1>
                        <p className="text-xs text-primary/50">v2.0</p>
                    </div>
                </Link>
            </div>

            {/* New Engagement Button */}
            <div className="p-4">
                <Link
                    href="/engagements/new"
                    className="btn-primary w-full flex items-center justify-center gap-2 text-sm"
                >
                    <Plus size={16} />
                    New Engagement
                </Link>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-3 space-y-1 overflow-y-auto">
                <p className="px-3 py-2 text-xs text-primary/40 uppercase tracking-wider">
                    Navigation
                </p>
                {navigation.map((item) => (
                    <NavLink key={item.name} item={item} />
                ))}

                <p className="px-3 py-2 mt-4 text-xs text-primary/40 uppercase tracking-wider">
                    Tools
                </p>
                {toolNavigation.map((item) => (
                    <NavLink key={item.name} item={item} />
                ))}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-primary/20">
                <div className="px-3 text-xs text-primary/30">
                    <code>$ whoami</code>
                    <br />
                    <span className="text-primary/50">pentester@hackmate</span>
                </div>
            </div>
        </aside>
    );
}
