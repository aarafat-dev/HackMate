/**
 * HackMate v2.0 - New Report Page
 */

'use client';

import { Suspense, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Card, Button, Input } from '@/components/ui';
import { reportsApi, engagementsApi, type Engagement } from '@/lib/api';
import { FileText, ArrowLeft, Terminal, AlertTriangle, Sparkles, CheckCircle2 } from 'lucide-react';
import Link from 'next/link';

function NewReportContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const engagementId = searchParams.get('engagement') || '';

    const [reportType, setReportType] = useState<'executive' | 'technical' | 'full'>('full');
    const [includeEvidence, setIncludeEvidence] = useState(true);
    const [includeRemediation, setIncludeRemediation] = useState(true);

    const { data: engagement, isLoading: engagementLoading } = useQuery<Engagement>({
        queryKey: ['engagement', engagementId],
        queryFn: async () => {
            const res = await engagementsApi.get(engagementId);
            return res.data;
        },
        enabled: !!engagementId,
    });

    const generateMutation = useMutation({
        mutationFn: async () => {
            return await reportsApi.generate(engagementId, {
                report_type: reportType,
                include_evidence: includeEvidence,
                include_remediation: includeRemediation,
            } as any);
        },
        onSuccess: () => {
            router.push(`/reports?engagement=${engagementId}`);
        },
    });

    if (!engagementId) {
        return (
            <div className="text-center py-12">
                <AlertTriangle className="mx-auto text-severity-critical" size={48} />
                <h2 className="mt-4 text-xl font-bold text-primary">No Engagement Selected</h2>
                <p className="text-muted-foreground mt-2">Please select an engagement to generate a report.</p>
                <Link href="/engagements" className="btn-primary mt-4 inline-block">
                    View Engagements
                </Link>
            </div>
        );
    }

    if (engagementLoading) {
        return (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full" />
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <Link
                href={`/engagements/${engagementId}`}
                className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors"
            >
                <ArrowLeft size={16} />
                Back to Engagement
            </Link>

            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-primary flex items-center gap-3">
                        <FileText size={28} />
                        Generate Report
                    </h1>
                    <p className="text-muted-foreground mt-1">
                        Creating professional documentation for <span className="text-primary font-mono">{engagement?.name}</span>
                    </p>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-2 space-y-6">
                    <Card title="Report Configuration" icon={<Terminal size={16} />}>
                        <div className="p-4 space-y-6">
                            <div className="space-y-3">
                                <label className="text-sm font-medium text-primary">Report Type</label>
                                <div className="grid grid-cols-3 gap-3">
                                    {(['executive', 'technical', 'full'] as const).map((type) => (
                                        <button
                                            key={type}
                                            onClick={() => setReportType(type)}
                                            className={`p-3 rounded border text-sm font-medium transition-all ${reportType === type
                                                    ? 'bg-primary/20 border-primary text-primary shadow-glow-sm'
                                                    : 'bg-black/40 border-primary/20 text-muted-foreground hover:border-primary/40'
                                                }`}
                                        >
                                            <span className="uppercase">{type}</span>
                                        </button>
                                    ))}
                                </div>
                                <p className="text-xs text-muted-foreground">
                                    {reportType === 'executive' && 'Focuses on high-level risk overview for management.'}
                                    {reportType === 'technical' && 'Detailed breakdown of vulnerabilities and technical steps.'}
                                    {reportType === 'full' && 'Comprehensive report including both executive and technical sections.'}
                                </p>
                            </div>

                            <div className="space-y-4">
                                <label className="text-sm font-medium text-primary">Content Options</label>
                                <div className="space-y-2">
                                    <label className="flex items-center gap-3 p-3 bg-black/20 rounded border border-primary/10 cursor-pointer hover:bg-black/30 transition-colors">
                                        <input
                                            type="checkbox"
                                            checked={includeEvidence}
                                            onChange={(e) => setIncludeEvidence(e.target.checked)}
                                            className="w-4 h-4 rounded border-primary bg-transparent text-primary focus:ring-primary"
                                        />
                                        <div className="flex-1">
                                            <p className="text-sm font-medium text-primary">Include Evidence</p>
                                            <p className="text-xs text-muted-foreground">Attach terminal outputs and screenshots to findings.</p>
                                        </div>
                                    </label>

                                    <label className="flex items-center gap-3 p-3 bg-black/20 rounded border border-primary/10 cursor-pointer hover:bg-black/30 transition-colors">
                                        <input
                                            type="checkbox"
                                            checked={includeRemediation}
                                            onChange={(e) => setIncludeRemediation(e.target.checked)}
                                            className="w-4 h-4 rounded border-primary bg-transparent text-primary focus:ring-primary"
                                        />
                                        <div className="flex-1">
                                            <p className="text-sm font-medium text-primary">Include Remediation Plan</p>
                                            <p className="text-xs text-muted-foreground">Add clear, actionable steps to fix identified issues.</p>
                                        </div>
                                    </label>
                                </div>
                            </div>

                            <Button
                                className="w-full h-12 text-lg"
                                onClick={() => generateMutation.mutate()}
                                disabled={generateMutation.isPending}
                            >
                                {generateMutation.isPending ? (
                                    <div className="flex items-center gap-2">
                                        <div className="animate-spin w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full" />
                                        ANALYZING DATA & GENERATING...
                                    </div>
                                ) : (
                                    <div className="flex items-center gap-2">
                                        <Sparkles size={20} />
                                        BUILD AI REPORT
                                    </div>
                                )}
                            </Button>
                        </div>
                    </Card>
                </div>

                <div className="space-y-6">
                    <Card title="Engagement Stats" icon={<CheckCircle2 size={16} />}>
                        <div className="p-4 space-y-4">
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-muted-foreground">Target</span>
                                <span className="text-primary font-mono">{engagement?.target}</span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-muted-foreground">Findings</span>
                                <span className="text-primary font-bold">{engagement?.finding_count || 0}</span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-muted-foreground">Status</span>
                                <span className="text-status-active uppercase text-xs">{engagement?.status}</span>
                            </div>
                        </div>
                    </Card>

                    <Card title="Hacker Tip" icon={<Sparkles size={16} />}>
                        <div className="p-4 text-xs text-muted-foreground leading-relaxed">
                            <p>
                                AI-generated reports are trained on PTES standards.
                                Make sure your terminal outputs are clean for the best
                                "Evidence" integration.
                            </p>
                        </div>
                    </Card>
                </div>
            </div>
        </div>
    );
}

export default function NewReportPage() {
    return (
        <Suspense fallback={<div className="text-primary/50">Loading form...</div>}>
            <NewReportContent />
        </Suspense>
    );
}
