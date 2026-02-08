/**
 * HackMate v2.0 - Scans Page
 */

'use client';

import { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { Card, StatusBadge, Button } from '@/components/ui';
import { scansApi, engagementsApi, type Scan, type Engagement } from '@/lib/api';
import { formatRelativeTime } from '@/lib/utils';
import { Radar, Zap, Clock, Terminal, Target } from 'lucide-react';

function ScansContent() {
    const searchParams = useSearchParams();
    const engagementId = searchParams.get('engagement') || '';

    const { data: scans, isLoading } = useQuery<Scan[]>({
        queryKey: ['scans', engagementId],
        queryFn: async () => {
            if (engagementId) {
                const res = await scansApi.list(engagementId);
                return res.data;
            } else {
                const res = await scansApi.listAll();
                return res.data;
            }
        },
    });

    const { data: engagements } = useQuery<Engagement[]>({
        queryKey: ['engagements'],
        queryFn: async () => {
            const res = await engagementsApi.list();
            return res.data;
        },
    });

    const getEngagementName = (id: string) => {
        return engagements?.find(e => e.id === id)?.name || id.substring(0, 8);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-primary flex items-center gap-3">
                        <Radar size={28} />
                        Scans
                    </h1>
                    <p className="text-muted-foreground mt-1">$ nmap -sV -p- /opt/hackmate/active_scans</p>
                </div>
            </div>

            <Card>
                <div className="p-4 border-b border-primary/10 bg-primary/5 flex items-center justify-between">
                    <h3 className="text-sm font-semibold text-primary uppercase tracking-wider">
                        {engagementId ? 'Recent Scans' : 'All Engagement Scans'}
                    </h3>
                    <div className="text-xs text-muted-foreground">Showing {scans?.length || 0} scans</div>
                </div>
                {isLoading ? (
                    <div className="p-12 text-center">
                        <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto" />
                        <p className="mt-4 text-muted-foreground font-mono text-sm">LOADING SCANS...</p>
                    </div>
                ) : scans && scans.length > 0 ? (
                    <div className="divide-y divide-primary/10">
                        {scans.map((scan) => (
                            <div key={scan.id} className="p-4 hover:bg-primary/5 transition-colors">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className="w-10 h-10 bg-primary/10 rounded flex items-center justify-center border border-primary/20">
                                            <Zap size={20} className="text-primary" />
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-2">
                                                <h4 className="font-bold text-primary">{scan.tool.toUpperCase()} Scan</h4>
                                                {!engagementId && (
                                                    <span className="flex items-center gap-1 text-[10px] text-primary/40 uppercase bg-primary/5 px-1.5 py-0.5 rounded border border-primary/10">
                                                        <Target size={10} />
                                                        {getEngagementName(scan.engagement_id)}
                                                    </span>
                                                )}
                                            </div>
                                            <p className="text-xs text-muted-foreground font-mono">ID: {scan.id.substring(0, 8)} • {scan.options || 'Default options'}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-6">
                                        <div className="text-right">
                                            <div className="flex items-center gap-1 text-xs text-muted-foreground">
                                                <Clock size={12} />
                                                {formatRelativeTime(scan.created_at)}
                                            </div>
                                            <p className="text-xs font-mono text-primary/50 mt-1">{scan.target}</p>
                                        </div>
                                        <StatusBadge status={scan.status} />
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="p-12 text-center">
                        <Terminal className="mx-auto text-primary/20" size={56} />
                        <h4 className="mt-4 text-primary font-medium">No Scans Found</h4>
                        <p className="text-sm text-muted-foreground mt-1">No automated scans have been launched yet.</p>
                        {engagementId && (
                            <Button className="mt-6" onClick={() => window.location.href = `/terminal?engagement=${engagementId}`}>
                                Open Terminal to Scan
                            </Button>
                        )}
                    </div>
                )}
            </Card>
        </div>
    );
}

export default function ScansPage() {
    return (
        <Suspense fallback={<div className="text-primary/50">Loading scans...</div>}>
            <ScansContent />
        </Suspense>
    );
}
