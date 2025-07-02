import { Article } from "../types/article";

export function generateSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .trim();
}

export function storeArticle(article: Article): string {
  const slug = generateSlug(article.title);
  localStorage.setItem(`article_${slug}`, JSON.stringify(article));
  return slug;
}

export function getArticle(slug: string): Article | null {
  const stored = localStorage.getItem(`article_${slug}`);
  return stored ? JSON.parse(stored) : null;
}
