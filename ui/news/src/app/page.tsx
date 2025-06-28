"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { NewsPrompt, NewsPromptRef } from "./components/news-prompt";
import { PageLayout } from "./components/page-layout";
import { Article } from "./types/article";
import { storeArticle } from "./utils/article-utils";

export default function Home() {
  const router = useRouter();
  const [currentPrompt, setCurrentPrompt] = useState("");
  const newsPromptRef = useRef<NewsPromptRef>(null);

  const handleArticleGenerated = (article: Article) => {
    const slug = storeArticle(article);
    setCurrentPrompt("");
    router.push(`/n/${slug}`);
  };

  const handleTopicSelect = (prompt: string) => {
    if (!prompt.trim()) return;
    // Populate the prompt box and trigger generation
    setCurrentPrompt(prompt.trim());
    // Use setTimeout to ensure the prompt is set before triggering submission
    setTimeout(() => {
      newsPromptRef.current?.submitForm();
    }, 0);
  };

  return (
    <PageLayout onTopicSelect={handleTopicSelect}>
      <div className="max-w-4xl mx-auto">
        <NewsPrompt
          ref={newsPromptRef}
          onArticleGenerated={handleArticleGenerated}
          initialPrompt={currentPrompt}
        />
      </div>
    </PageLayout>
  );
}
