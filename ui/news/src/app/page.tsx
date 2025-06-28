"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { NewsPrompt } from "./components/news-prompt";
import { PageLayout } from "./components/page-layout";
import { Article } from "./types/article";
import { storeArticle } from "./utils/article-utils";

export default function Home() {
  const router = useRouter();

  const handleArticleGenerated = (article: Article) => {
    const slug = storeArticle(article);
    router.push(`/n/${slug}`);
  };

  const handleTopicSelect = async (prompt: string) => {
    if (!prompt.trim()) return;
    // Call the same API as NewsPrompt
    try {
      const response = await fetch("/api/generate-news", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });
      if (!response.ok) throw new Error("Failed to generate article");
      const article = await response.json();
      const slug = storeArticle(article);
      router.push(`/n/${slug}`);
    } catch (error) {
      // Optionally handle error
      console.error(error);
    }
  };

  return (
    <PageLayout onTopicSelect={handleTopicSelect}>
      <div className="max-w-4xl mx-auto">
        <NewsPrompt onArticleGenerated={handleArticleGenerated} />
      </div>
    </PageLayout>
  );
}
