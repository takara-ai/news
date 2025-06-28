"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { NewsPrompt } from "./components/news-prompt";
import { PageLayout } from "./components/page-layout";
import { Article } from "./types/article";
import { storeArticle } from "./utils/article-utils";

export default function Home() {
  const router = useRouter();
  const [currentPrompt, setCurrentPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleArticleGenerated = (article: Article) => {
    const slug = storeArticle(article);
    router.push(`/n/${slug}`);
  };

  const handleTopicSelect = (prompt: string) => {
    if (!prompt.trim()) return;
    setCurrentPrompt(prompt);
    handlePromptSubmit(prompt);
  };

  const handlePromptSubmit = async (prompt: string) => {
    if (!prompt.trim()) return;
    setIsLoading(true);
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
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <PageLayout onTopicSelect={handleTopicSelect}>
      <div className="max-w-4xl mx-auto">
        <NewsPrompt
          onArticleGenerated={handleArticleGenerated}
          initialPrompt={currentPrompt}
          isLoading={isLoading}
          onSubmit={handlePromptSubmit}
        />
      </div>
    </PageLayout>
  );
}
