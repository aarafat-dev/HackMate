/**
 * HackMate v2.0 - Dashboard Page
 * Main dashboard with stats and recent activity.
 */

'use client';

import { useQuery } from '@tanstack/react-query';
import { Card, StatusBadge, SeverityBadge } from '@/components/ui';
import { engagementsApi, type Engagement, type EngagementStats } from '@/lib/api';
import { formatRelativeTime } from '@/lib/utils';
import Link from 'next/link';
import {
  Shield,
  Target,
  Bug,
  AlertTriangle,
  CheckCircle2,
  ArrowRight,
  Terminal,
  Radar,
} from 'lucide-react';

export default function DashboardPage() {
  // Fetch stats
  const { data: stats } = useQuery<EngagementStats>({
    queryKey: ['engagementStats'],
    queryFn: async () => {
      const res = await engagementsApi.getStats();
      return res.data;
    },
  });

  // Fetch recent engagements
  const { data: engagements } = useQuery<Engagement[]>({
    queryKey: ['recentEngagements'],
    queryFn: async () => {
      const res = await engagementsApi.list({ limit: 5 });
      return res.data;
    },
  });

  const statCards = [
    {
      title: 'Total Engagements',
      value: stats?.total_engagements || 0,
      icon: <Target className="text-primary" size={24} />,
      color: 'primary',
    },
    {
      title: 'Active Engagements',
      value: stats?.active_engagements || 0,
      icon: <Radar className="text-status-active" size={24} />,
      color: 'active',
    },
    {
      title: 'Total Findings',
      value: stats?.total_findings || 0,
      icon: <Bug className="text-severity-medium" size={24} />,
      color: 'medium',
    },
    {
      title: 'Critical Findings',
      value: stats?.critical_findings || 0,
      icon: <AlertTriangle className="text-severity-critical" size={24} />,
      color: 'critical',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-primary flex items-center gap-3">
            <div className="w-8 h-8 rounded border border-primary/30 flex items-center justify-center overflow-hidden bg-primary/10">
              <img src="/logo.png" alt="Logo" className="w-full h-full object-cover" />
            </div>
            Dashboard
          </h1>
          <p className="text-muted-foreground mt-1">
            $ cat /var/log/hackmate/overview.log
          </p>
        </div>
        <Link href="/engagements/new" className="btn-primary flex items-center gap-2">
          <Target size={16} />
          New Engagement
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat) => (
          <Card key={stat.title} className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">{stat.title}</p>
                <p className="text-3xl font-bold text-primary mt-1">{stat.value}</p>
              </div>
              <div className="p-3 bg-black/40 rounded-lg border border-primary/20">
                {stat.icon}
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Recent Engagements */}
      <Card title="Recent Engagements" icon={<Target size={16} />}>
        {engagements && engagements.length > 0 ? (
          <div className="space-y-3">
            {engagements.map((engagement) => (
              <Link
                key={engagement.id}
                href={`/engagements/${engagement.id}`}
                className="flex items-center justify-between p-3 bg-black/40 rounded border border-primary/10 hover:border-primary/30 transition-colors group"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-primary/10 rounded flex items-center justify-center">
                    <Target className="text-primary" size={20} />
                  </div>
                  <div>
                    <h3 className="font-medium text-primary group-hover:text-primary-bright">
                      {engagement.name}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {engagement.target}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <StatusBadge status={engagement.status} />
                  <span className="text-xs text-muted-foreground">
                    {formatRelativeTime(engagement.updated_at)}
                  </span>
                  <ArrowRight className="text-primary/50 group-hover:text-primary transition-colors" size={16} />
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Terminal className="mx-auto text-primary/30" size={48} />
            <p className="mt-4 text-muted-foreground">No engagements found.</p>
            <p className="text-sm text-primary/50 mt-1">
              $ hackmate --init-engagement &lt;target&gt;
            </p>
            <Link href="/engagements/new" className="btn-secondary mt-4 inline-block">
              Create Your First Engagement
            </Link>
          </div>
        )}
      </Card>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link href="/terminal" className="terminal-card p-4 hover:shadow-glow-sm transition-all group">
          <div className="flex items-center gap-3">
            <Terminal className="text-primary" size={24} />
            <div>
              <h3 className="font-medium">Terminal</h3>
              <p className="text-sm text-muted-foreground">Execute commands</p>
            </div>
          </div>
        </Link>

        <Link href="/findings" className="terminal-card p-4 hover:shadow-glow-sm transition-all group">
          <div className="flex items-center gap-3">
            <Bug className="text-severity-high" size={24} />
            <div>
              <h3 className="font-medium">Findings</h3>
              <p className="text-sm text-muted-foreground">View vulnerabilities</p>
            </div>
          </div>
        </Link>

        <Link href="/ai" className="terminal-card p-4 hover:shadow-glow-sm transition-all group">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="text-status-active" size={24} />
            <div>
              <h3 className="font-medium">AI Assistant</h3>
              <p className="text-sm text-muted-foreground">Get guidance</p>
            </div>
          </div>
        </Link>
      </div>
    </div>
  );
}
