import { NextResponse } from "next/server";
import { getToken } from "next-auth/jwt";

const BACKEND_URL = process.env.BACKEND_URL!;

export async function GET(req: Request) {
  const token = await getToken({ req: req as any, secret: process.env.AUTH_SECRET });
  const appJwt = (token as any)?.appJwt as string | undefined;

  if (!token || !appJwt) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const upstream = await fetch(`${BACKEND_URL}/api/secure-whoami`, {
    headers: { Authorization: `Bearer ${appJwt}` },
    cache: "no-store",
  });

  const data = await upstream.json().catch(() => ({}));
  return NextResponse.json(data, { status: upstream.status });
}

export async function POST(req: Request) {
  const token = await getToken({ req: req as any, secret: process.env.AUTH_SECRET });
  const appJwt = (token as any)?.appJwt as string | undefined;

  if (!token || !appJwt) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await req.text();

  const upstream = await fetch(`${BACKEND_URL}/api/secure-data`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${appJwt}`,
      "Content-Type": "application/json",
    },
    body,
    cache: "no-store",
  });

  const data = await upstream.json().catch(() => ({}));
  return NextResponse.json(data, { status: upstream.status });
}
