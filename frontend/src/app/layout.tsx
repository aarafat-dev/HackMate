import type { Metadata } from "next";
import { Providers } from "@/components/layout/Providers";
import { Sidebar } from "@/components/layout/Sidebar";
import "./globals.css";

export const metadata: Metadata = {
  title: "HackMate v2.0 - Penetration Testing Platform",
  description: "Professional penetration testing platform with AI assistance",
  keywords: ["penetration testing", "security", "hacking", "PTES", "vulnerability"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground antialiased">
        <Providers>
          <div className="flex min-h-screen bg-grid">
            <Sidebar />
            <main className="flex-1 overflow-auto">
              <div className="container mx-auto p-6">
                {children}
              </div>
            </main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
