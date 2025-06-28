"use client";

import { useRouter } from "next/navigation";
import Link from "next/link";
import { NewsPrompt } from "./components/news-prompt";
import { ThemeToggle } from "./components/theme-toggle";
import { Article } from "./types/article";
import { storeArticle } from "./utils/article-utils";

export default function Home() {
  const router = useRouter();

  const handleArticleGenerated = (article: Article) => {
    const slug = storeArticle(article);
    router.push(`/n/${slug}`);
  };

  const getCurrentDate = () => {
    return new Date().toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

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
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12"></div>
            <NewsPrompt onArticleGenerated={handleArticleGenerated} />
          </div>
        </div>
      </main>
    </div>
  );
}
