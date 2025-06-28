"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { NewsArticle } from "../../components/news-article";
import { PageLayout } from "../../components/page-layout";
import { LoadingLayout } from "../../components/loading-layout";
import { Article } from "../../types/article";
import { getArticle } from "../../utils/article-utils";

export default function ArticlePage() {
  const params = useParams();
  const router = useRouter();
  const [article, setArticle] = useState<Article | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const slug = params.slug as string;
        const articleData = getArticle(slug);
        if (articleData) {
          setArticle(articleData);
        } else {
          // If no stored article, redirect back to home
          router.push("/");
        }
      } catch (error) {
        console.error("Error fetching article:", error);
        router.push("/");
      } finally {
        setIsLoading(false);
      }
    };

    if (params.slug) {
      fetchArticle();
    }
  }, [params.slug, router]);

  const handleNewArticle = () => {
    router.push("/");
  };

  if (isLoading) {
    return <LoadingLayout />;
  }

  if (!article) {
    return null;
  }

  return (
    <PageLayout showNewArticleButton onNewArticle={handleNewArticle}>
      <NewsArticle article={article} />
    </PageLayout>
  );
}
