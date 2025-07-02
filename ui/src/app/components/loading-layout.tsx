"use client";

import { PageLayout } from "./page-layout";

export function LoadingLayout() {
  return (
    <PageLayout>
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-newspaper-black dark:text-white">Loading...</div>
      </div>
    </PageLayout>
  );
}
