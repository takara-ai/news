"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { Sun, Moon, Monitor } from "lucide-react";

export function ThemeToggle() {
  const { setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleToggle = () => {
    if (!mounted) return;

    if (resolvedTheme === "light") setTheme("dark");
    else if (resolvedTheme === "dark") setTheme("system");
    else setTheme("light");
  };

  // Show a fallback button during mounting to prevent layout shift
  const getIcon = () => {
    if (!mounted) return <Sun className="h-5 w-5" />;

    if (resolvedTheme === "light") return <Sun className="h-5 w-5" />;
    if (resolvedTheme === "dark") return <Moon className="h-5 w-5" />;
    return <Monitor className="h-5 w-5" />;
  };

  return (
    <button
      onClick={handleToggle}
      aria-label="Toggle theme"
      className="rounded-md p-2 hover:bg-newspaper-gray-100 dark:hover:bg-newspaper-gray-800 transition-colors text-newspaper-black dark:text-white disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
      disabled={!mounted}
    >
      {getIcon()}
    </button>
  );
}
