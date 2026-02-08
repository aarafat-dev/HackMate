/**
 * HackMate v2.0 - Badge Component
 * Styled badges for status and severity.
 */

import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface BadgeProps {
    children: ReactNode;
    variant?: 'default' | 'success' | 'warning' | 'danger' | 'info' | 'neutral';
    className?: string;
}

export function Badge({ children, variant = 'default', className }: BadgeProps) {
    const variants = {
        default: 'badge-success',
        success: 'badge-success',
        warning: 'badge-warning',
        danger: 'badge-danger',
        info: 'badge-info',
        neutral: 'badge-neutral',
    };

    return (
        <span className={cn('badge', variants[variant], className)}>
            {children}
        </span>
    );
}

// Severity badge
export function SeverityBadge({ severity }: { severity: string }) {
    const severityClasses: Record<string, string> = {
        critical: 'severity-critical',
        high: 'severity-high',
        medium: 'severity-medium',
        low: 'severity-low',
        info: 'severity-info',
    };

    return (
        <span className={cn('badge', severityClasses[severity] || severityClasses.info)}>
            {severity.toUpperCase()}
        </span>
    );
}

// Status badge
export function StatusBadge({ status }: { status: string }) {
    const statusClasses: Record<string, string> = {
        planning: 'status-planning',
        active: 'status-active',
        completed: 'status-completed',
        on_hold: 'status-hold',
        in_progress: 'status-active',
        not_started: 'status-planning',
    };

    const displayName = status.replace('_', ' ').toUpperCase();

    return (
        <span className={cn('badge', statusClasses[status] || 'badge-neutral')}>
            {displayName}
        </span>
    );
}
