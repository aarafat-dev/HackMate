/**
 * HackMate v2.0 - Findings Page
 */

'use client';

import { useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { Card, SeverityBadge, StatusBadge, Input, Button } from '@/components/ui';
import { findingsApi, engagementsApi, type Finding, type Engagement } from '@/lib/api';
import { formatRelativeTime, cn } from '@/lib/utils';
import { Bug, Search, Plus, ChevronDown, ChevronRight, Target } from 'lucide-react';

function FindingsContent() {
    const searchParams = useSearchParams();
    const engagementId = searchParams.get('engagement') || '';
    const [search, setSearch] = useState('');
    const [severityFilter, setSeverityFilter] = useState('');
    const [statusFilter, setStatusFilter] = useState('');
    const [expandedId, setExpandedId] = useState<string | null>(null);

    const { data: findings, isLoading } = useQuery<Finding[]>({
        queryKey: ['findings', engagementId, severityFilter, statusFilter, search],
        queryFn: async () => {
            if (engagementId) {
                const res = await findingsApi.list(engagementId, {
                    severity: severityFilter || undefined,
                    status: statusFilter || undefined,
                    search: search || undefined,
                });
                return res.data;
            } else {
                const res = await findingsApi.listAll({
                    severity: severityFilter || undefined,
                    status: statusFilter || undefined,
                    search: search || undefined,
                });
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

    const severityOptions = [
        { value: '', label: 'All Severities' },
        { value: 'critical', label: 'Critical' },
        { value: 'high', label: 'High' },
        { value: 'medium', label: 'Medium' },
        { value: 'low', label: 'Low' },
        { value: 'info', label: 'Info' },
    ];

    const statusOptions = [
        { value: '', label: 'All Status' },
        { value: 'open', label: 'Open' },
        { value: 'confirmed', label: 'Confirmed' },
        { value: 'false_positive', label: 'False Positive' },
        { value: 'remediated', label: 'Remediated' },
    ];

    const groupedFindings = findings?.reduce((acc, finding) => {
        const sev = finding.severity;
        if (!acc[sev]) acc[sev] = [];
        acc[sev].push(finding);
        return acc;
    }, {} as Record<string, Finding[]>);

    const severityOrder = ['critical', 'high', 'medium', 'low', 'info'];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-primary flex items-center gap-3">
                        <Bug size={28} />
                        Findings
                    </h1>
                    <p className="text-muted-foreground mt-1">$ cat /var/log/hackmate/findings.log</p>
                </div>
                {engagementId && (
                    <Button className="flex items-center gap-2">
                        <Plus size={16} />
                        Add Finding
                    </Button>
                )}
            </div>

            <div className="space-y-6">
                <div className="flex gap-4">
                    <div className="flex-1 relative">
                        <Bug className="absolute left-3 top-1/2 -translate-y-1/2 text-primary/50" size={16} />
                        <Input placeholder="Search findings..." value={search} onChange={(e) => setSearch(e.target.value)} className="pl-10" />
                    </div>
                    <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)} className="input w-40">
                        {severityOptions.map((opt) => (<option key={opt.value} value={opt.value}>{opt.label}</option>))}
                    </select>
                    <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)} className="input w-40">
                        {statusOptions.map((opt) => (<option key={opt.value} value={opt.value}>{opt.label}</option>))}
                    </select>
                </div>

                <div className="grid grid-cols-5 gap-4">
                    {severityOrder.map((sev) => (
                        <Card key={sev} className="p-3">
                            <div className="flex items-center justify-between">
                                <span className={cn('text-sm font-medium', sev === 'critical' ? 'text-severity-critical' : sev === 'high' ? 'text-severity-high' : sev === 'medium' ? 'text-severity-medium' : sev === 'low' ? 'text-severity-low' : 'text-severity-info')}>
                                    {sev.toUpperCase()}
                                </span>
                                <span className="text-xl font-bold text-primary">{groupedFindings?.[sev]?.length || 0}</span>
                            </div>
                        </Card>
                    ))}
                </div>

                {findings && findings.length > 0 && (
                    <Card title="Last Finding" icon={<Bug size={16} className="text-primary" />}>
                        <div className="p-4 bg-primary/5 border border-primary/20 rounded-lg flex items-center justify-between">
                            <div className="flex items-center gap-4">
                                <SeverityBadge severity={findings[0].severity} />
                                <div>
                                    <h4 className="font-bold text-primary text-lg">{findings[0].title}</h4>
                                    <p className="text-sm text-muted-foreground">{getEngagementName(findings[0].engagement_id)} • Discovered {formatRelativeTime(findings[0].created_at)}</p>
                                </div>
                            </div>
                            <Button size="sm" onClick={() => setExpandedId(findings[0].id)}>
                                View Details
                            </Button>
                        </div>
                    </Card>
                )}

                <Card>
                    {isLoading ? (
                        <div className="p-8 text-center">
                            <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto" />
                            <p className="mt-4 text-muted-foreground">Loading findings...</p>
                        </div>
                    ) : findings && findings.length > 0 ? (
                        <div className="divide-y divide-primary/10">
                            {findings.map((finding) => (
                                <div key={finding.id}>
                                    <div className="flex items-center justify-between p-4 cursor-pointer hover:bg-primary/5 transition-colors" onClick={() => setExpandedId(expandedId === finding.id ? null : finding.id)}>
                                        <div className="flex items-center gap-4">
                                            {expandedId === finding.id ? <ChevronDown className="text-primary" size={16} /> : <ChevronRight className="text-primary/50" size={16} />}
                                            <SeverityBadge severity={finding.severity} />
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <h4 className="font-medium text-primary">{finding.title}</h4>
                                                    {!engagementId && (
                                                        <span className="flex items-center gap-1 text-[10px] text-primary/40 uppercase bg-primary/5 px-1.5 py-0.5 rounded border border-primary/10">
                                                            <Target size={10} />
                                                            {getEngagementName(finding.engagement_id)}
                                                        </span>
                                                    )}
                                                </div>
                                                <p className="text-xs text-muted-foreground">{finding.affected_component || 'Unknown'} • {formatRelativeTime(finding.created_at)}</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <StatusBadge status={finding.status} />
                                            {finding.cvss_score && <span className="text-sm font-mono text-primary">CVSS: {finding.cvss_score}</span>}
                                        </div>
                                    </div>
                                    {expandedId === finding.id && (
                                        <div className="px-4 pb-4 pl-12 space-y-3 bg-black/20">
                                            {finding.description && (<div><p className="text-xs text-primary/50 uppercase mb-1">Description</p><p className="text-sm text-foreground/80">{finding.description}</p></div>)}
                                            {finding.evidence && (<div><p className="text-xs text-primary/50 uppercase mb-1">Evidence</p><pre className="text-xs bg-black/40 p-3 rounded overflow-x-auto">{finding.evidence}</pre></div>)}
                                            {finding.remediation && (<div><p className="text-xs text-primary/50 uppercase mb-1">Remediation</p><p className="text-sm text-foreground/80">{finding.remediation}</p></div>)}
                                            {finding.cve_id && <p className="text-xs text-primary">CVE: {finding.cve_id}</p>}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="p-8 text-center">
                            <Bug className="mx-auto text-primary/30" size={48} />
                            <h3 className="mt-4 font-medium text-primary">No Findings</h3>
                            <p className="text-sm text-muted-foreground mt-1">{search || severityFilter || statusFilter ? 'No findings match your filters' : 'No vulnerabilities discovered yet'}</p>
                        </div>
                    )}
                </Card>
            </div>
        </div>
    );
}

export default function FindingsPage() {
    return (
        <Suspense fallback={<div className="text-primary/50">Loading findings...</div>}>
            <FindingsContent />
        </Suspense>
    );
}
