import { NextRequest, NextResponse } from "next/server";
import OpenAI from "openai";

async function validateImageUrl(url: string): Promise<boolean> {
  try {
    const response = await fetch(url, {
      method: "HEAD",
      headers: { "User-Agent": "Mozilla/5.0" },
      signal: AbortSignal.timeout(5000),
    });
    const contentType = response.headers.get("content-type");
    return response.ok && contentType
      ? contentType.startsWith("image/")
      : false;
  } catch {
    return false;
  }
}

async function getFreeImages(
  prompt: string
): Promise<{ headerImage?: string; middleImage?: string }> {
  try {
    // Use Unsplash search directly (no API key needed for basic usage)
    const searchQuery = encodeURIComponent(prompt);
    const response = await fetch(
      `https://unsplash.com/napi/search/photos?query=${searchQuery}&per_page=10&page=1`,
      {
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible; NewsApp/1.0)",
          Accept: "application/json",
        },
        signal: AbortSignal.timeout(3000), // 3 second timeout
      }
    );

    if (response.ok) {
      const data = await response.json();

      if (data.results && data.results.length > 0) {
        const validImages = [];

        // Take first 4 images and validate them
        for (const result of data.results.slice(0, 4)) {
          if (
            result.urls?.regular &&
            (await validateImageUrl(result.urls.regular))
          ) {
            validImages.push(result.urls.regular);
            if (validImages.length >= 2) break;
          }
        }

        return {
          headerImage: validImages[0],
          middleImage: validImages[1],
        };
      }
    }
  } catch (error) {
    console.error("Unsplash direct search failed:", error);
  }

  return {};
}

async function getDuckDuckGoImages(
  prompt: string
): Promise<{ headerImage?: string; middleImage?: string }> {
  try {
    // Use DuckDuckGo instant answer API (more reliable)
    const searchQuery = encodeURIComponent(prompt);
    const response = await fetch(
      `https://api.duckduckgo.com/?q=${searchQuery}&format=json&no_html=1&skip_disambig=1&t=newsapp`,
      {
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible; NewsApp/1.0)",
        },
        signal: AbortSignal.timeout(5000), // 5 second timeout
      }
    );

    if (response.ok) {
      const data = await response.json();

      // Extract image URLs from related topics or abstract
      const imageUrls = [];

      // Check abstract source
      if (data.AbstractSource) {
        imageUrls.push(data.AbstractSource);
      }

      // Check related topics
      if (data.RelatedTopics) {
        for (const topic of data.RelatedTopics.slice(0, 3)) {
          if (topic.Icon?.URL) {
            imageUrls.push(topic.Icon.URL);
          }
        }
      }

      // Validate and return first 2 working images
      const validImages = [];
      for (const imageUrl of imageUrls) {
        if (await validateImageUrl(imageUrl)) {
          validImages.push(imageUrl);
          if (validImages.length >= 2) break;
        }
      }

      return {
        headerImage: validImages[0],
        middleImage: validImages[1],
      };
    }
  } catch (error) {
    console.error("DuckDuckGo image search failed:", error);
  }

  return {};
}

async function getBingImages(
  prompt: string
): Promise<{ headerImage?: string; middleImage?: string }> {
  try {
    // Use Bing Image Search API
    const searchQuery = encodeURIComponent(prompt);
    const response = await fetch(
      `https://api.bing.microsoft.com/v7.0/images/search?q=${searchQuery}&count=10&safeSearch=strict&imageType=photo`,
      {
        headers: {
          "Ocp-Apim-Subscription-Key": process.env.BING_SEARCH_KEY || "",
          "User-Agent": "Mozilla/5.0",
        },
      }
    );

    if (response.ok) {
      const data = await response.json();
      const images = data.value || [];

      // Take first two valid images
      const validImages = [];
      for (const img of images.slice(0, 6)) {
        if (img.contentUrl && (await validateImageUrl(img.contentUrl))) {
          validImages.push(img.contentUrl);
          if (validImages.length >= 2) break;
        }
      }

      return {
        headerImage: validImages[0],
        middleImage: validImages[1],
      };
    }
  } catch (error) {
    console.error("Bing image search failed:", error);
  }

  // Fallback to Unsplash if Bing fails
  return await getUnsplashFallback(prompt);
}

async function getUnsplashFallback(
  prompt: string
): Promise<{ headerImage?: string; middleImage?: string }> {
  try {
    const response = await fetch(
      `https://api.unsplash.com/search/photos?query=${encodeURIComponent(
        prompt
      )}&per_page=2`,
      {
        headers: {
          Authorization: `Client-ID ${
            process.env.UNSPLASH_ACCESS_KEY || "demo"
          }`,
          "User-Agent": "Mozilla/5.0",
        },
      }
    );

    if (response.ok) {
      const data = await response.json();
      const images = data.results || [];

      return {
        headerImage: images[0]?.urls?.regular,
        middleImage: images[1]?.urls?.regular,
      };
    }
  } catch (error) {
    console.error("Unsplash fallback failed:", error);
  }

  return {};
}

async function findWorkingImages(
  prompt: string
): Promise<{ headerImage?: string; middleImage?: string }> {
  // Try Pixabay first (free, reliable)
  const pixabayImages = await getFreeImages(prompt);

  if (pixabayImages.headerImage || pixabayImages.middleImage) {
    console.log("Found Pixabay images:", pixabayImages);
    return pixabayImages;
  }

  // Fallback to Unsplash
  const unsplashImages = await getUnsplashFallback(prompt);
  console.log("Using Unsplash fallback:", unsplashImages);
  return unsplashImages;
}

async function generateArticleWithoutImages(prompt: string) {
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  });

  const response = await openai.responses.create({
    model: "gpt-4.1",
    input: `Write a short, factual news analysis article (max 200 words) in the style and cadence of The New York Times about: "${prompt}". Focus on context, implications, and analysis. Use a measured, authoritative tone. Reference historical trends or broader consequences where relevant. Attribute analysis to credible sources or the reporter. Avoid sensationalism and extra commentary. Return ONLY a valid, minified JSON object with the following fields: title, content, additionalContent. Do not include markdown, links, or any extra formatting. Do not include any text outside the JSON object. Example: {\"title\":\"...\",\"content\":\"...\",\"additionalContent\":\"...\"}`,
    text: {
      format: {
        type: "text",
      },
    },
    reasoning: {},
    tools: [
      {
        type: "web_search_preview",
        user_location: {
          type: "approximate",
        },
        search_context_size: "high",
      },
    ],
    temperature: 1,
    max_output_tokens: 2048,
    top_p: 1,
    store: true,
  });

  let outputText = response.output_text || "{}";
  outputText = outputText.replace(/^```json\s*|^```\s*|\s*```$/gim, "").trim();

  try {
    return JSON.parse(outputText);
  } catch (e) {
    return {
      title: "Error",
      content: outputText || "Failed to parse article.",
    };
  }
}

export async function POST(request: NextRequest) {
  try {
    const { prompt } = await request.json();

    console.log("Prompt received:", prompt);

    if (!prompt || typeof prompt !== "string") {
      return NextResponse.json(
        { error: "Prompt is required and must be a string" },
        { status: 400 }
      );
    }

    // Call the Flask API
    const flaskResponse = await fetch("http://127.0.0.1:5000/get-news", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });

    let articleData;
    if (flaskResponse.ok) {
      try {
        articleData = await flaskResponse.json();
      } catch (jsonErr) {
        console.error("Failed to parse Flask response:", jsonErr);
        return NextResponse.json(
          { error: "Failed to parse article response" },
          { status: 500 }
        );
      }
    } else {
      // Fallback to OpenAI if Flask API fails
      articleData = await generateArticleWithoutImages(prompt);
    }

    // Fetch images separately using our TypeScript image search
    const images = await findWorkingImages(prompt);

    // Merge article data with images
    const finalArticle = { ...articleData, ...images };
    console.log("Final article with images:", finalArticle);

    return NextResponse.json(finalArticle, { status: 200 });
  } catch (error) {
    console.error("Error generating news article:", error);
    return NextResponse.json(
      { error: "Failed to generate article" },
      { status: 500 }
    );
  }
}
