"use client";

import { useState } from "react";
import { NewsPrompt } from "./components/news-prompt";
import { NewsArticle } from "./components/news-article";
import { ThemeToggle } from "./components/theme-toggle";
import { Article } from "./types/article";

export default function Home() {
  const [currentArticle, setCurrentArticle] = useState<Article | null>(null);

  const handleNewArticle = () => {
    setCurrentArticle(null);
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
    <div className="min-h-screen bg-white dark:bg-newspaper-gray-900 transition-colors">
      {/* Header */}
      <header className="border-b-2 border-newspaper-black dark:border-newspaper-gray-700">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Top bar */}
          <div className="flex justify-between items-center py-3 text-sm border-b border-newspaper-gray-200 dark:border-newspaper-gray-700">
            <div className="byline">{getCurrentDate()}</div>
            <div className="flex items-center space-x-4">
              {currentArticle && (
                <button
                  onClick={handleNewArticle}
                  className="byline hover:text-newspaper-black dark:hover:text-white transition-colors"
                >
                  New Article
                </button>
              )}
              <ThemeToggle />
            </div>
          </div>

          {/* Masthead */}
          <div className="text-center py-8">
            <h1 className="masthead text-5xl md:text-7xl text-newspaper-black dark:text-white">
              The New World Times
            </h1>
            <div className="mt-2 text-sm byline">
              News for you, about anything you want
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {!currentArticle ? (
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12"></div>
            <NewsPrompt onArticleGenerated={setCurrentArticle} />
          </div>
        ) : (
          <NewsArticle article={currentArticle} />
        )}
      </main>
    </div>
  );
}
