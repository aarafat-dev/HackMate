/**
 * HackMate v2.0 - Input Component
 * Terminal-styled input with variants.
 */

import { cn } from '@/lib/utils';
import { InputHTMLAttributes, forwardRef } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
    error?: string;
    label?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ className, error, label, ...props }, ref) => {
        return (
            <div className="space-y-1.5">
                {label && (
                    <label className="block text-sm text-primary/80">{label}</label>
                )}
                <input
                    ref={ref}
                    className={cn(
                        'input',
                        error && 'input-error',
                        className
                    )}
                    {...props}
                />
                {error && <p className="text-xs text-severity-critical">{error}</p>}
            </div>
        );
    }
);

Input.displayName = 'Input';
