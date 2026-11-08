#!/usr/bin/env bun
/**
 * Cloud Syndicate Publisher (GitHub Actions Runner)
 * Automatically syncs local markdown documentation with Dev.to via REST API.
 */

import { readFileSync, readdirSync, existsSync } from "fs";
import { join } from "path";

const DOCS_DIR = join(import.meta.dir, "..", "docs");

interface DevToResponse {
  id: number;
  title: string;
  url: string;
}

async function getExistingTitles(apiKey: string): Promise<Set<string>> {
  try {
    const res = await fetch("https://dev.to/api/articles/me/all", {
      headers: { "api-key": apiKey }
    });
    if (!res.ok) return new Set();
    const list = (await res.json()) as DevToResponse[];
    return new Set(list.map(a => a.title.toLowerCase().trim()));
  } catch {
    return new Set();
  }
}

async function publishArticle(apiKey: string, title: string, markdown: string, tags: string[]): Promise<string | null> {
  const payload = {
    article: {
      title,
      published: true,
      body_markdown: markdown,
      tags
    }
  };

  try {
    const res = await fetch("https://dev.to/api/articles", {
      method: "POST",
      headers: {
        "api-key": apiKey,
        "Content-Type": "application/json",
        "User-Agent": "AutonomousCloudPublisher/1.0.0"
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.text();
      console.error(`[ERROR] HTTP ${res.status}: ${err}`);
      return null;
    }

    const data = (await res.json()) as DevToResponse;
    return data.url;
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(`[EXCEPTION]:`, msg);
    return null;
  }
}

async function main() {
  const apiKey = process.argv[2] || process.env.DEVTO_API_KEY;
  if (!apiKey) {
    console.error("DEVTO_API_KEY required.");
    process.exit(1);
  }

  const existing = await getExistingTitles(apiKey);
  console.log(`[CLOUD RUNNER] Found ${existing.size} existing published articles.`);

  const files = readdirSync(DOCS_DIR).filter(f => f.endsWith(".md"));

  for (const file of files) {
    const fullPath = join(DOCS_DIR, file);
    const content = readFileSync(fullPath, "utf-8");
    const firstLine = content.split("\n")[0] || "";
    const title = firstLine.replace(/^#\s*/, "").trim();

    if (existing.has(title.toLowerCase().trim())) {
      console.log(`[SKIP] Already live: "${title}"`);
      continue;
    }

    console.log(`[PUBLISHING] "${title}"...`);
    const tags = ["productivity", "tools", "technology", "programming"];
    const url = await publishArticle(apiKey, title, content, tags);

    if (url) {
      console.log(`[SUCCESS] Published: ${url}`);
    }

    // Cooldown delay
    await Bun.sleep(5000);
  }
}

void main();
