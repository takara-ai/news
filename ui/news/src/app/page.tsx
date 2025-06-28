"use client";

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

  return (
    <PageLayout>
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12"></div>
        <NewsPrompt onArticleGenerated={handleArticleGenerated} />
      </div>
    </PageLayout>
  );
}
