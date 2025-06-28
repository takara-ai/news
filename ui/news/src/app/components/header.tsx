"use client";

import Link from "next/link";
import { ThemeToggle } from "./theme-toggle";
import { getCurrentDate } from "../utils/date-utils";
import { TopicNavigation } from "./topic-navigation";
import { TOPIC_CONFIG } from "../config/topics";

interface HeaderProps {
  showNewArticleButton?: boolean;
  onNewArticle?: () => void;
  onTopicSelect?: (prompt: string) => void;
}

export function Header({
  showNewArticleButton = false,
  onNewArticle,
  onTopicSelect,
}: HeaderProps) {
  return (
    <header>
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Top bar */}
        <div className="flex justify-between items-center py-3 text-sm border-b border-newspaper-gray-200 dark:border-newspaper-gray-700">
          <div className="byline text-newspaper-gray-600 dark:text-newspaper-gray-400">
            {getCurrentDate()}
          </div>
          <div className="flex items-center space-x-4">
            {showNewArticleButton && onNewArticle && (
              <button
                onClick={onNewArticle}
                className="byline text-newspaper-gray-600 dark:text-newspaper-gray-400 hover:text-newspaper-black dark:hover:text-white transition-colors cursor-pointer"
              >
                New Article
              </button>
            )}
            <ThemeToggle />
          </div>
        </div>

        {/* Masthead */}
        <div className="text-center py-8">
          <Link href="/" className="block">
            <h1 className="masthead font-chomsky text-5xl md:text-7xl text-newspaper-black dark:text-white hover:text-newspaper-gray-700 dark:hover:text-newspaper-gray-300 transition-colors cursor-pointer">
              The New World Times
            </h1>
          </Link>
          <div className="mt-2 text-sm byline text-newspaper-gray-600 dark:text-newspaper-gray-400">
            News for you, about anything you want
          </div>
        </div>

        {/* Topic Navigation */}
        <div className="mb-2">
          <TopicNavigation
            topics={TOPIC_CONFIG}
            onTopicSelect={onTopicSelect || (() => {})}
            className="mb-0"
          />
        </div>
      </div>
      {/* Bottom border */}
      <div className="border-b-2 border-newspaper-black dark:border-newspaper-gray-700" />
    </header>
  );
}
