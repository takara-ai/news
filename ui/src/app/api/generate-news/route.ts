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

    // Call the Flask API
    const flaskResponse = await fetch("http://127.0.0.1:5000/get-news", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });

    if (!flaskResponse.ok) {
      const errorData = await flaskResponse.json();
      return NextResponse.json(
        { error: errorData.error || "An error occurred while fetching from API." },
        { status: flaskResponse.status }
      );
    }

    const data = await flaskResponse.json();

    // Return the article from the Flask API
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error generating news article:", error);
    return NextResponse.json(
      { error: "An error occurred while generating the news article." },
      { status: 500 }
    );
  }
}
