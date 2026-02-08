/**
 * HackMate v2.0 - Card Component
 * Terminal-styled card with neon border.
 */

import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface CardProps {
    children: ReactNode;
    className?: string;
    title?: string;
    icon?: ReactNode;
    actions?: ReactNode;
    noPadding?: boolean;
}

export function Card({ children, className, title, icon, actions, noPadding }: CardProps) {
    return (
        <div
            className={cn(
                'terminal-card',
                className
            )}
        >
            {(title || icon || actions) && (
                <div className="terminal-card-header">
                    <div className="terminal-card-title">
                        {icon}
                        <span>{title}</span>
                    </div>
                    {actions && <div className="ml-auto">{actions}</div>}
                </div>
            )}
            {noPadding ? children : <div className="p-4">{children}</div>}
        </div>
    );
}

export function CardHeader({ children, className }: { children: ReactNode; className?: string }) {
    return <div className={cn('terminal-card-header', className)}>{children}</div>;
}

export function CardTitle({ children, className }: { children: ReactNode; className?: string }) {
    return <div className={cn('terminal-card-title', className)}>{children}</div>;
}

export function CardContent({ children, className }: { children: ReactNode; className?: string }) {
    return <div className={cn('p-4', className)}>{children}</div>;
}
