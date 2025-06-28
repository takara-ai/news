"use client";

import { ReactNode } from "react";
import { Header } from "./header";

interface PageLayoutProps {
  children: ReactNode;
  showNewArticleButton?: boolean;
  onNewArticle?: () => void;
}

export function PageLayout({
  children,
  showNewArticleButton = false,
  onNewArticle,
}: PageLayoutProps) {
  return (
    <div className="min-h-svh dark:bg-newspaper-gray-900 transition-colors flex flex-col">
      <Header
        showNewArticleButton={showNewArticleButton}
        onNewArticle={onNewArticle}
      />
      <main className="px-4 sm:px-6 lg:px-8 py-12 flex-1">
        <div className="max-w-6xl mx-auto">{children}</div>
      </main>
    </div>
  );
}
