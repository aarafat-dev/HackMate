/**
 * HackMate v2.0 - New Engagement Page
 */

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useMutation } from '@tanstack/react-query';
import { Card, Button, Input } from '@/components/ui';
import { engagementsApi } from '@/lib/api';
import { Target, ArrowLeft, Rocket } from 'lucide-react';
import Link from 'next/link';

export default function NewEngagementPage() {
    const router = useRouter();
    const [name, setName] = useState('');
    const [target, setTarget] = useState('');
    const [scope, setScope] = useState('');
    const [errors, setErrors] = useState<Record<string, string>>({});

    const createMutation = useMutation({
        mutationFn: async () => {
            const res = await engagementsApi.create({ name, target, scope: scope || undefined });
            return res.data;
        },
        onSuccess: (data) => {
            router.push(`/engagements/${data.id}`);
        },
        onError: (error: Error) => {
            setErrors({ submit: error.message });
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        // Validation
        const newErrors: Record<string, string> = {};
        if (!name.trim()) newErrors.name = 'Engagement name is required';
        if (!target.trim()) newErrors.target = 'Target is required';

        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }

        setErrors({});
        createMutation.mutate();
    };

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            {/* Header */}
            <div>
                <Link
                    href="/engagements"
                    className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors"
                >
                    <ArrowLeft size={16} />
                    Back to Engagements
                </Link>
                <h1 className="text-2xl font-bold text-primary flex items-center gap-3 mt-4">
                    <Target size={28} />
                    New Engagement
                </h1>
                <p className="text-muted-foreground mt-1">
                    $ hackmate --create-engagement
                </p>
            </div>

            {/* Form */}
            <Card className="p-6">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <Input
                        label="Engagement Name *"
                        placeholder="e.g., ACME Corp Q1 2024 Assessment"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        error={errors.name}
                    />

                    <Input
                        label="Primary Target *"
                        placeholder="e.g., example.com or 192.168.1.0/24"
                        value={target}
                        onChange={(e) => setTarget(e.target.value)}
                        error={errors.target}
                    />

                    <div className="space-y-1.5">
                        <label className="block text-sm text-primary/80">Scope Description</label>
                        <textarea
                            placeholder="Define the scope of the engagement (optional)..."
                            value={scope}
                            onChange={(e) => setScope(e.target.value)}
                            rows={4}
                            className="input resize-none"
                        />
                    </div>

                    {errors.submit && (
                        <div className="p-3 bg-severity-critical/10 border border-severity-critical/30 rounded text-severity-critical text-sm">
                            {errors.submit}
                        </div>
                    )}

                    <div className="flex gap-4">
                        <Button
                            type="submit"
                            loading={createMutation.isPending}
                            className="flex-1"
                        >
                            <Rocket size={16} className="mr-2" />
                            Create Engagement
                        </Button>
                        <Link href="/engagements" className="btn-secondary">
                            Cancel
                        </Link>
                    </div>
                </form>
            </Card>

            {/* Tips */}
            <Card className="p-4 border-primary/20">
                <p className="text-sm text-primary/70">
                    <span className="text-primary font-semibold">[TIP]</span> After creating,
                    you&apos;ll start in Phase 1: Pre-Engagement Interactions. Make sure you have
                    proper authorization before proceeding.
                </p>
            </Card>
        </div>
    );
}
