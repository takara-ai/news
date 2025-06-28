"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { NewsArticle } from "../../components/news-article";
import { ThemeToggle } from "../../components/theme-toggle";
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

  const getCurrentDate = () => {
    return new Date().toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-svh dark:bg-newspaper-gray-900 transition-colors flex flex-col">
        <header className="border-b-2 border-newspaper-black dark:border-newspaper-gray-700">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-3 text-sm border-b border-newspaper-gray-200 dark:border-newspaper-gray-700">
              <div className="byline text-newspaper-gray-600 dark:text-newspaper-gray-400">
                {getCurrentDate()}
              </div>
              <div className="flex items-center space-x-4">
                <ThemeToggle />
              </div>
            </div>
            <div className="text-center py-8">
              <Link href="/" className="block">
                <h1 className="masthead text-5xl md:text-7xl text-newspaper-black dark:text-white hover:text-newspaper-gray-700 dark:hover:text-newspaper-gray-300 transition-colors cursor-pointer">
                  The New World Times
                </h1>
              </Link>
            </div>
          </div>
        </header>
        <main className="flex-1 flex items-center justify-center">
          <div className="text-newspaper-black dark:text-white">Loading...</div>
        </main>
      </div>
    );
  }

  if (!article) {
    return null;
  }

  return (
    <div className="min-h-svh dark:bg-newspaper-gray-900 transition-colors flex flex-col">
      {/* Header */}
      <header className="border-b-2 border-newspaper-black dark:border-newspaper-gray-700">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Top bar */}
          <div className="flex justify-between items-center py-3 text-sm border-b border-newspaper-gray-200 dark:border-newspaper-gray-700">
            <div className="byline text-newspaper-gray-600 dark:text-newspaper-gray-400">
              {getCurrentDate()}
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={handleNewArticle}
                className="byline text-newspaper-gray-600 dark:text-newspaper-gray-400 hover:text-newspaper-black dark:hover:text-white transition-colors cursor-pointer"
              >
                New Article
              </button>
              <ThemeToggle />
            </div>
          </div>

          {/* Masthead */}
          <div className="text-center py-8">
            <Link href="/" className="block">
              <h1 className="masthead text-5xl md:text-7xl text-newspaper-black dark:text-white hover:text-newspaper-gray-700 dark:hover:text-newspaper-gray-300 transition-colors cursor-pointer">
                The New World Times
              </h1>
            </Link>
            <div className="mt-2 text-sm byline text-newspaper-gray-600 dark:text-newspaper-gray-400">
              News for you, about anything you want
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="px-4 sm:px-6 lg:px-8 py-12 flex-1">
        <div className="max-w-6xl mx-auto">
          <NewsArticle article={article} />
        </div>
      </main>
    </div>
  );
}
