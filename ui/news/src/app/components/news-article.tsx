"use client";

import Image from "next/image";
import { Article } from "../types/article";
import { getShortDate } from "../utils/date-utils";

interface NewsArticleProps {
  article: Article;
}

export function NewsArticle({ article }: NewsArticleProps) {
  const renderMarkdownLinks = (text: string) => {
    // Regex to match markdown links [text](url)
    const markdownLinkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;

    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = markdownLinkRegex.exec(text)) !== null) {
      // Add text before the link
      if (match.index > lastIndex) {
        parts.push(text.slice(lastIndex, match.index));
      }

      // Add the link
      const linkText = match[1];
      const linkUrl = match[2];
      parts.push(
        <a
          key={match.index}
          href={linkUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 dark:text-blue-400 hover:underline font-medium"
        >
          {linkText}
        </a>
      );

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text after the last link
    if (lastIndex < text.length) {
      parts.push(text.slice(lastIndex));
    }

    return parts.length > 0 ? parts : text;
  };

  const renderContent = (content: string) => {
    const paragraphs = content.split("\n\n");
    return paragraphs.map((paragraph, index) => (
      <p
        key={index}
        className="article-content mb-6 text-newspaper-black dark:text-white first:first-letter:float-left first:first-letter:text-6xl first:first-letter:font-bold first:first-letter:mr-2 first:first-letter:mt-1 first:first-letter:leading-none"
      >
        {renderMarkdownLinks(paragraph)}
      </p>
    ));
  };

  return (
    <article className="max-w-4xl mx-auto">
      {/* Article Header */}
      <header className="mb-8 pb-6 border-b border-newspaper-gray-200 dark:border-newspaper-gray-700">
        <div className="section-tag mb-4 text-newspaper-gray-600 dark:text-newspaper-gray-400">
          BREAKING NEWS
        </div>
        <h1 className="text-4xl md:text-6xl font-display font-bold text-newspaper-black dark:text-white leading-tight mb-6">
          {article.title}
        </h1>

        {/* Byline */}
        <div className="flex flex-wrap items-center gap-4 text-sm text-newspaper-gray-600 dark:text-newspaper-gray-400">
          <div className="byline">By The New World Times Staff</div>
          <div className="byline">{getShortDate()}</div>
          <div className="byline">5 MIN READ</div>
        </div>
      </header>

      {/* Header Image */}
      {article.headerImage && (
        <figure className="mb-8">
          <div className="relative aspect-video w-full overflow-hidden">
            <Image
              src={article.headerImage}
              alt="Article header"
              fill
              className="object-cover"
              priority
            />
          </div>
          <figcaption className="mt-3 text-sm text-newspaper-gray-600 dark:text-newspaper-gray-400 font-sans">
            A scene related to the developing story.{" "}
            <span className="font-medium">The New World Times</span>
          </figcaption>
        </figure>
      )}

      {/* Article Body */}
      <div className="prose prose-lg max-w-none">
        <div className="text-lg leading-newspaper text-newspaper-black dark:text-white font-serif">
          {renderContent(article.content)}
        </div>
      </div>

      {/* Middle Image */}
      {article.middleImage && (
        <figure className="my-12">
          <div className="relative aspect-video w-full overflow-hidden">
            <Image
              src={article.middleImage}
              alt="Article middle image"
              fill
              className="object-cover"
            />
          </div>
          <figcaption className="mt-3 text-sm text-newspaper-gray-600 dark:text-newspaper-gray-400 font-sans">
            Additional context for the ongoing story.{" "}
            <span className="font-medium">The New World Times</span>
          </figcaption>
        </figure>
      )}

      {/* Additional Content */}
      {article.additionalContent && (
        <div className="prose prose-lg max-w-none">
          <div className="text-lg leading-newspaper text-newspaper-black dark:text-white font-serif">
            {renderContent(article.additionalContent)}
          </div>
        </div>
      )}

      {/* Article Footer */}
      <footer className="mt-12 pt-8 border-t border-newspaper-gray-200 dark:border-newspaper-gray-700">
        <div className="text-sm text-newspaper-gray-600 dark:text-newspaper-gray-400 font-sans">
          <p className="mb-2">
            <strong>Correction:</strong> This article was generated
            automatically. The New World Times maintains the highest standards
            of accuracy in all reporting.
          </p>
          <p>
            Follow <strong>@NewWorldTimes</strong> for breaking news and
            updates.
          </p>
        </div>
      </footer>
    </article>
  );
}
