import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const { prompt } = await request.json();

    if (!prompt || typeof prompt !== "string") {
      return NextResponse.json(
        { error: "Prompt is required and must be a string" },
        { status: 400 }
      );
    }

    // TODO: Replace this with your actual external API call
    // For now, we'll return a mock response
    const mockArticle = {
      title: `Breaking: ${prompt}`,
      headerImage:
        "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&h=400&fit=crop",
      content: `In a significant development, ${prompt}. This story continues to unfold as authorities and experts weigh in on the implications.

Local officials have confirmed that the situation is being monitored closely. Citizens are advised to stay informed through official channels as more details emerge.

The impact of this development is expected to resonate across multiple sectors, with stakeholders already beginning to assess potential consequences.`,
      middleImage:
        "https://images.unsplash.com/photo-1586339949916-3e9457bef6d3?w=800&h=400&fit=crop",
      additionalContent: `As the story develops, experts predict that this could mark a turning point in how similar situations are handled in the future.

The broader implications extend beyond immediate concerns, potentially influencing policy decisions and public discourse in the weeks to come.

We will continue to monitor this developing story and provide updates as new information becomes available.`,
    };

    // Simulate API delay
    // await new Promise((resolve) => setTimeout(resolve, 2000));

    return NextResponse.json(mockArticle);
  } catch (error) {
    console.error("Error generating news article:", error);
    return NextResponse.json(
      { error: "Failed to generate article" },
      { status: 500 }
    );
  }
}
