import { Topic } from "../components/topic-navigation";

// Main topic configurations - easily customizable
export const TOPIC_CONFIG: Topic[] = [
  {
    id: "us",
    label: "U.S.",
    prompt: "Write a news article about current U.S. politics and government",
    subTopics: [
      {
        id: "politics",
        label: "Politics",
        prompt: "Write a news article about U.S. politics and elections",
      },
      {
        id: "nyregion",
        label: "New York",
        prompt: "Write a news article about New York City or New York state",
      },
      {
        id: "california",
        label: "California",
        prompt: "Write a news article about California news and events",
      },
      {
        id: "education",
        label: "Education",
        prompt: "Write a news article about education policy and schools",
      },
      {
        id: "health",
        label: "Health",
        prompt: "Write a news article about healthcare and public health",
      },
      {
        id: "obituaries",
        label: "Obituaries",
        prompt:
          "Write a news article about a notable person who recently passed away",
      },
      {
        id: "science",
        label: "Science",
        prompt:
          "Write a news article about scientific discoveries and research",
      },
      {
        id: "climate",
        label: "Climate",
        prompt:
          "Write a news article about climate change and environmental issues",
      },
      {
        id: "weather",
        label: "Weather",
        prompt:
          "Write a news article about weather events and natural disasters",
      },
      {
        id: "sports",
        label: "Sports",
        prompt: "Write a news article about U.S. sports and athletics",
      },
      {
        id: "business",
        label: "Business",
        prompt: "Write a news article about U.S. business and economy",
      },
      {
        id: "technology",
        label: "Tech",
        prompt: "Write a news article about technology and innovation",
      },
    ],
  },
  {
    id: "world",
    label: "World",
    prompt:
      "Write a news article about international affairs and global events",
    subTopics: [
      {
        id: "africa",
        label: "Africa",
        prompt: "Write a news article about events in Africa",
      },
      {
        id: "americas",
        label: "Americas",
        prompt: "Write a news article about events in the Americas",
      },
      {
        id: "asia",
        label: "Asia",
        prompt: "Write a news article about events in Asia",
      },
      {
        id: "australia",
        label: "Australia",
        prompt: "Write a news article about events in Australia",
      },
      {
        id: "canada",
        label: "Canada",
        prompt: "Write a news article about events in Canada",
      },
      {
        id: "europe",
        label: "Europe",
        prompt: "Write a news article about events in Europe",
      },
      {
        id: "middleeast",
        label: "Middle East",
        prompt: "Write a news article about events in the Middle East",
      },
    ],
  },
  {
    id: "business",
    label: "Business",
    prompt: "Write a news article about business, finance, and the economy",
    subTopics: [
      {
        id: "economy",
        label: "Economy",
        prompt: "Write a news article about economic trends and policies",
      },
      {
        id: "media",
        label: "Media",
        prompt: "Write a news article about media and entertainment industry",
      },
      {
        id: "markets",
        label: "Finance and Markets",
        prompt: "Write a news article about financial markets and investing",
      },
      {
        id: "dealbook",
        label: "DealBook",
        prompt: "Write a news article about business deals and corporate news",
      },
      {
        id: "personaltech",
        label: "Personal Tech",
        prompt: "Write a news article about consumer technology",
      },
      {
        id: "energy",
        label: "Energy Transition",
        prompt: "Write a news article about energy and renewable resources",
      },
      {
        id: "money",
        label: "Your Money",
        prompt:
          "Write a news article about personal finance and money management",
      },
    ],
  },
  {
    id: "arts",
    label: "Arts",
    prompt: "Write a news article about arts, culture, and entertainment",
    subTopics: [
      {
        id: "books",
        label: "Book Review",
        prompt: "Write a news article about books and literature",
      },
      {
        id: "movies",
        label: "Movies",
        prompt: "Write a news article about film and cinema",
      },
      {
        id: "music",
        label: "Music",
        prompt: "Write a news article about music and musicians",
      },
      {
        id: "television",
        label: "Television",
        prompt: "Write a news article about TV shows and streaming",
      },
      {
        id: "theater",
        label: "Theater",
        prompt: "Write a news article about theater and performing arts",
      },
      {
        id: "popculture",
        label: "Pop Culture",
        prompt: "Write a news article about popular culture and trends",
      },
      {
        id: "design",
        label: "Visual Arts",
        prompt: "Write a news article about art and design",
      },
    ],
  },
  {
    id: "lifestyle",
    label: "Lifestyle",
    prompt:
      "Write a news article about lifestyle, health, and personal interests",
    subTopics: [
      {
        id: "well",
        label: "Well",
        prompt: "Write a news article about health and wellness",
      },
      {
        id: "travel",
        label: "Travel",
        prompt: "Write a news article about travel and tourism",
      },
      {
        id: "style",
        label: "Style",
        prompt: "Write a news article about fashion and style",
      },
      {
        id: "realestate",
        label: "Real Estate",
        prompt: "Write a news article about real estate and housing",
      },
      {
        id: "food",
        label: "Food",
        prompt: "Write a news article about food, cooking, and restaurants",
      },
      {
        id: "love",
        label: "Love",
        prompt: "Write a news article about relationships and dating",
      },
    ],
  },
  {
    id: "opinion",
    label: "Opinion",
    prompt: "Write an opinion piece about current events and social issues",
    subTopics: [
      {
        id: "editorials",
        label: "Editorials",
        prompt: "Write an editorial about a current issue",
      },
      {
        id: "guestessays",
        label: "Guest Essays",
        prompt: "Write a guest opinion piece about a topic of interest",
      },
      {
        id: "letters",
        label: "Letters",
        prompt: "Write a letter to the editor about a current issue",
      },
    ],
  },
  {
    id: "technology",
    label: "Technology",
    prompt: "Write a news article about technology and innovation",
    subTopics: [
      {
        id: "ai",
        label: "Artificial Intelligence",
        prompt: "Write a news article about AI and machine learning",
      },
      {
        id: "cybersecurity",
        label: "Cybersecurity",
        prompt: "Write a news article about cybersecurity and digital privacy",
      },
      {
        id: "startups",
        label: "Startups",
        prompt: "Write a news article about tech startups and entrepreneurship",
      },
      {
        id: "socialmedia",
        label: "Social Media",
        prompt: "Write a news article about social media and online platforms",
      },
    ],
  },
  {
    id: "sports",
    label: "Sports",
    prompt: "Write a news article about sports and athletics",
    subTopics: [
      {
        id: "nfl",
        label: "NFL",
        prompt: "Write a news article about NFL football",
      },
      {
        id: "nba",
        label: "NBA",
        prompt: "Write a news article about NBA basketball",
      },
      {
        id: "mlb",
        label: "MLB",
        prompt: "Write a news article about Major League Baseball",
      },
      {
        id: "soccer",
        label: "Soccer",
        prompt: "Write a news article about soccer and football",
      },
      {
        id: "olympics",
        label: "Olympics",
        prompt: "Write a news article about the Olympics",
      },
    ],
  },
];

// Helper function to get topics by category
export const getTopicsByCategory = (category: string): Topic | undefined => {
  return TOPIC_CONFIG.find((topic) => topic.id === category);
};

// Helper function to get all sub-topics
export const getAllSubTopics = (): Topic[] => {
  return TOPIC_CONFIG.flatMap((topic) => topic.subTopics || []);
};

// Helper function to search topics
export const searchTopics = (query: string): Topic[] => {
  const lowercaseQuery = query.toLowerCase();
  return TOPIC_CONFIG.filter(
    (topic) =>
      topic.label.toLowerCase().includes(lowercaseQuery) ||
      topic.prompt.toLowerCase().includes(lowercaseQuery) ||
      topic.subTopics?.some(
        (sub) =>
          sub.label.toLowerCase().includes(lowercaseQuery) ||
          sub.prompt.toLowerCase().includes(lowercaseQuery)
      )
  );
};
