/**
 * HackMate v2.0 - Engagements List Page
 */

'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, StatusBadge, Button, Input } from '@/components/ui';
import { engagementsApi, type Engagement } from '@/lib/api';
import { formatRelativeTime } from '@/lib/utils';
import Link from 'next/link';
import {
    Target,
    Plus,
    Search,
    ArrowRight,
    Terminal,
    Filter,
    Trash2,
} from 'lucide-react';
import { useQueryClient, useMutation } from '@tanstack/react-query';

export default function EngagementsPage() {
    const [search, setSearch] = useState('');
    const [statusFilter, setStatusFilter] = useState<string>('');

    const { data: engagements, isLoading } = useQuery<Engagement[]>({
        queryKey: ['engagements', search, statusFilter],
        queryFn: async () => {
            const res = await engagementsApi.list({
                search: search || undefined,
                status: statusFilter || undefined,
            });
            return res.data;
        },
    });

    const queryClient = useQueryClient();

    const deleteMutation = useMutation({
        mutationFn: async (id: string) => {
            await engagementsApi.delete(id);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['engagements'] });
        },
    });

    const handleDelete = (e: React.MouseEvent, id: string) => {
        e.preventDefault();
        e.stopPropagation();
        if (confirm('Are you sure you want to delete this engagement? This action cannot be undone.')) {
            deleteMutation.mutate(id);
        }
    };

    const statusOptions = [
        { value: '', label: 'All Status' },
        { value: 'planning', label: 'Planning' },
        { value: 'active', label: 'Active' },
        { value: 'completed', label: 'Completed' },
        { value: 'on_hold', label: 'On Hold' },
    ];

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-primary flex items-center gap-3">
                        <Target size={28} />
                        Engagements
                    </h1>
                    <p className="text-muted-foreground mt-1">
                        $ ls -la /opt/hackmate/engagements/
                    </p>
                </div>
                <Link href="/engagements/new" className="btn-primary flex items-center gap-2">
                    <Plus size={16} />
                    New Engagement
                </Link>
            </div>

            {/* Filters */}
            <div className="flex gap-4">
                <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-primary/50" size={16} />
                    <Input
                        placeholder="Search engagements..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="pl-10"
                    />
                </div>
                <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                    className="input w-40"
                >
                    {statusOptions.map((opt) => (
                        <option key={opt.value} value={opt.value}>
                            {opt.label}
                        </option>
                    ))}
                </select>
            </div>

            {/* Engagement List */}
            <Card>
                {isLoading ? (
                    <div className="p-8 text-center text-muted-foreground">
                        <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto" />
                        <p className="mt-4">Loading engagements...</p>
                    </div>
                ) : engagements && engagements.length > 0 ? (
                    <div className="divide-y divide-primary/10">
                        {engagements.map((engagement) => (
                            <Link
                                key={engagement.id}
                                href={`/engagements/${engagement.id}`}
                                className="flex items-center justify-between p-4 hover:bg-primary/5 transition-colors group"
                            >
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 bg-primary/10 rounded border border-primary/20 flex items-center justify-center">
                                        <Target className="text-primary" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="font-semibold text-primary group-hover:text-primary-bright transition-colors">
                                            {engagement.name}
                                        </h3>
                                        <p className="text-sm text-muted-foreground font-mono">
                                            {engagement.target}
                                        </p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-6">
                                    <div className="text-right hidden md:block">
                                        <p className="text-xs text-muted-foreground">PHASES</p>
                                        <p className="text-sm font-mono text-primary">
                                            {engagement.completed_phases || 0}/{engagement.phase_count || 8}
                                        </p>
                                    </div>
                                    <div className="text-right hidden md:block">
                                        <p className="text-xs text-muted-foreground">FINDINGS</p>
                                        <p className="text-sm font-mono text-primary">
                                            {engagement.finding_count || 0}
                                        </p>
                                    </div>
                                    <StatusBadge status={engagement.status} />
                                    <span className="text-xs text-muted-foreground hidden lg:block">
                                        {formatRelativeTime(engagement.updated_at)}
                                    </span>
                                    <button
                                        onClick={(e) => handleDelete(e, engagement.id)}
                                        className="p-2 text-muted-foreground hover:text-red-500 transition-colors z-10"
                                        title="Delete Engagement"
                                    >
                                        <Trash2 size={16} />
                                    </button>
                                    <ArrowRight className="text-primary/50 group-hover:text-primary transition-colors" size={16} />
                                </div>
                            </Link>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-12">
                        <Terminal className="mx-auto text-primary/30" size={56} />
                        <h3 className="mt-4 font-medium text-primary">No engagements found</h3>
                        <p className="text-sm text-muted-foreground mt-1">
                            {search ? 'Try adjusting your search filters' : 'Create your first engagement to get started'}
                        </p>
                        <Link href="/engagements/new" className="btn-primary mt-4 inline-flex items-center gap-2">
                            <Plus size={16} />
                            Create Engagement
                        </Link>
                    </div>
                )}
            </Card>
        </div>
    );
}
