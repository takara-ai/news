"use client";

interface Topic {
  id: string;
  label: string;
  prompt: string;
}

interface TopicNavigationProps {
  topics: Topic[];
  onTopicSelect: (prompt: string) => void;
  className?: string;
}

export function TopicNavigation({
  topics,
  onTopicSelect,
  className = "",
}: TopicNavigationProps) {
  return (
    <nav className={`topic-navigation ${className}`}>
      <ul className="flex flex-wrap justify-center gap-2 md:gap-4 text-sm">
        {topics.map((topic) => (
          <li key={topic.id}>
            <button
              onClick={() => onTopicSelect(topic.prompt)}
              className="flex items-center gap-1 px-3 py-2 text-newspaper-gray-700 dark:text-newspaper-gray-300 hover:text-newspaper-black dark:hover:text-white transition-colors cursor-pointer border-b-2 border-transparent hover:border-newspaper-black dark:hover:border-white"
            >
              {topic.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
