#!/usr/bin/env bun
/**
 * Autonomous Search Engine Pinger & IndexNow Broadcaster
 * Pings Google, Bing, and IndexNow API to force immediate crawler discovery.
 */

const HOST = "mahesawastu8.github.io";
const KEY = "8f3b2a9e1d7c4b5a6f8e0d2c4b6a8e0f";
const SITEMAP_URL = `https://${HOST}/awesome-developer-stack/sitemap.xml`;

const URL_LIST = [
  `https://${HOST}/awesome-developer-stack/`,
  `https://${HOST}/awesome-developer-stack/docs/raycast-vs-alfred-2026.html`,
  `https://${HOST}/awesome-developer-stack/docs/best-ai-presentation-tools-2026.html`,
  `https://${HOST}/awesome-developer-stack/docs/hostinger-vs-bluehost-2026.html`,
  `https://${HOST}/awesome-developer-stack/docs/best-ai-video-generators-2026.html`,
  `https://${HOST}/awesome-developer-stack/docs/typefully-vs-buffer-2026.html`,
  `https://${HOST}/awesome-developer-stack/docs/best-ai-seo-writers-2026.html`
];

async function submitIndexNow() {
  console.log("📡 Submitting URLs to IndexNow (Bing, Yandex, Seznam)...");
  const payload = {
    host: HOST,
    key: KEY,
    keyLocation: `https://${HOST}/awesome-developer-stack/${KEY}.txt`,
    urlList: URL_LIST
  };

  try {
    const res = await fetch("https://api.indexnow.org/indexnow", {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify(payload)
    });
    console.log(`✅ IndexNow Response: HTTP ${res.status} (${res.status === 200 || res.status === 202 ? "Accepted / Queued for Indexing" : "Status noted"})`);
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error("IndexNow error:", msg);
  }
}

async function pingGoogle() {
  console.log("📡 Pinging Google Sitemap Endpoint...");
  const url = `https://www.google.com/ping?sitemap=${encodeURIComponent(SITEMAP_URL)}`;
  try {
    const res = await fetch(url);
    console.log(`✅ Google Ping Response: HTTP ${res.status}`);
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    console.log("Google ping notice:", msg);
  }
}

async function pingBing() {
  console.log("📡 Pinging Bing Sitemap Endpoint...");
  const url = `https://www.bing.com/ping?sitemap=${encodeURIComponent(SITEMAP_URL)}`;
  try {
    const res = await fetch(url);
    console.log(`✅ Bing Ping Response: HTTP ${res.status}`);
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    console.log("Bing ping notice:", msg);
  }
}

async function main() {
  console.log("======================================================");
  console.log("⚡ FORCE-INDEXING SEARCH ENGINE PINGER (INDEXNOW + GOOGLE)");
  console.log("======================================================");
  await submitIndexNow();
  await pingGoogle();
  await pingBing();
  console.log("\n🚀 All indexing pings sent. Search engine crawlers dispatched!");
}

void main();
