import { NextResponse } from "next/server";
import { getToken } from "next-auth/jwt";

const BACKEND_URL = process.env.BACKEND_URL!;

async function forward(req: Request, method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE") {
  const url = new URL(req.url);
  const path = url.pathname.replace(/^\/api\/bff/, "");
  const qs = url.search;
  const target = `${BACKEND_URL}${path}${qs}`;

  const token = await getToken({ req: req as any, secret: process.env.AUTH_SECRET }).catch(() => null);
  const appJwt = (token as any)?.appJwt as string | undefined;

  const headers = new Headers(req.headers);
  headers.delete("host");
  headers.delete("connection");
  headers.delete("cookie");
  headers.delete("authorization");

  if (appJwt) {
    headers.set("authorization", `Bearer ${appJwt}`);
  }

  headers.set("x-bff", "nextjs");
  const ip = req.headers.get("x-forwarded-for") ?? "0.0.0.0";
  headers.set("x-forwarded-for", ip);

  const body = method === "GET" ? undefined : await req.arrayBuffer();

  const upstream = await fetch(target, {
    method,
    headers,
    body,
    cache: "no-store",
  });

  const respHeaders = new Headers(upstream.headers);
  return new NextResponse(upstream.body, {
    status: upstream.status,
    headers: respHeaders,
  });
}

export async function GET(req: Request, { params }: { params: { path: string[] } }) {
  return forward(req, "GET");
}
export async function POST(req: Request, { params }: { params: { path: string[] } }) {
  return forward(req, "POST");
}
export async function PUT(req: Request, { params }: { params: { path: string[] } }) {
  return forward(req, "PUT");
}
export async function PATCH(req: Request, { params }: { params: { path: string[] } }) {
  return forward(req, "PATCH");
}
export async function DELETE(req: Request, { params }: { params: { path: string[] } }) {
  return forward(req, "DELETE");
}
