"use client";

import { useState, useEffect } from "react";
import { Newspaper, Loader2 } from "lucide-react";
import { Article } from "../types/article";

interface NewsPromptProps {
  onArticleGenerated: (article: Article) => void;
  initialPrompt?: string;
  isLoading?: boolean;
  onSubmit?: (prompt: string) => Promise<void>;
}

export function NewsPrompt({
  onArticleGenerated,
  initialPrompt = "",
  isLoading: externalIsLoading = false,
  onSubmit,
}: NewsPromptProps) {
  const [prompt, setPrompt] = useState(initialPrompt);
  const [internalIsLoading, setInternalIsLoading] = useState(false);

  // Use external loading state if provided, otherwise use internal
  const isLoading = onSubmit ? externalIsLoading : internalIsLoading;

  // Update prompt when initialPrompt changes
  useEffect(() => {
    if (initialPrompt) {
      setPrompt(initialPrompt);
    }
  }, [initialPrompt]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isLoading) return;

    if (onSubmit) {
      // Use external submit handler
      await onSubmit(prompt.trim());
    } else {
      // Use internal submit handler (original behavior)
      setInternalIsLoading(true);
      try {
        const response = await fetch("/api/generate-news", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ prompt: prompt.trim() }),
        });

        if (!response.ok) {
          throw new Error("Failed to generate article");
        }

        const article = await response.json();
        onArticleGenerated(article);
        setPrompt("");
      } catch (error) {
        console.error("Error generating article:", error);
        // Handle error appropriately
      } finally {
        setInternalIsLoading(false);
      }
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto text-center pt-32">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="What story would you like to read today?"
            className="w-full p-4 pr-16 text-center border-newspaper-gray-300 dark:border-newspaper-gray-600 rounded-lg focus:ring-0    dark:bg-newspaper-gray-800 text-newspaper-black dark:text-white placeholder-newspaper-gray-500 dark:placeholder-newspaper-gray-400 font-sans text-lg"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!prompt.trim() || isLoading}
            className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 bg-newspaper-black hover:bg-newspaper-gray-800 disabled:bg-newspaper-gray-400 disabled:cursor-not-allowed rounded-md text-white transition-colors cursor-pointer"
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Newspaper className="h-5 w-5" />
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
