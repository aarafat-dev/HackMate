/**
 * HackMate v2.0 - Button Component
 * Multiple button variants with glow effects.
 */

import { cn } from '@/lib/utils';
import { ButtonHTMLAttributes, forwardRef } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
    size?: 'sm' | 'md' | 'lg';
    loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = 'primary', size = 'md', loading, disabled, children, ...props }, ref) => {
        const variants = {
            primary: 'btn-primary',
            secondary: 'btn-secondary',
            ghost: 'btn-ghost',
            danger: 'btn-danger',
        };

        const sizes = {
            sm: 'px-3 py-1.5 text-xs',
            md: 'px-5 py-2.5 text-sm',
            lg: 'px-6 py-3 text-base',
        };

        return (
            <button
                ref={ref}
                disabled={disabled || loading}
                className={cn(
                    variants[variant],
                    sizes[size],
                    loading && 'opacity-70',
                    className
                )}
                {...props}
            >
                {loading ? (
                    <span className="flex items-center gap-2">
                        <svg
                            className="animate-spin h-4 w-4"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                        >
                            <circle
                                className="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                strokeWidth="4"
                            />
                            <path
                                className="opacity-75"
                                fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            />
                        </svg>
                        Processing...
                    </span>
                ) : (
                    children
                )}
            </button>
        );
    }
);

Button.displayName = 'Button';
