import NextAuth from "next-auth";
import Google from "next-auth/providers/google";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.AUTH_GOOGLE_ID!,
      clientSecret: process.env.AUTH_GOOGLE_SECRET!,
    }),
  ],
  session: { strategy: "jwt" },
  callbacks: {
    async jwt({ token, account }) {
      if (account?.provider === "google") {
        const idToken = (account as any).id_token as string | undefined;
        const accessToken = account.access_token as string | undefined;

        if (idToken) {
          try {
            const resp = await fetch(`${process.env.BACKEND_URL}/auth/exchange`, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "X-Google-IDToken": idToken,
                ...(accessToken ? { "X-Google-AccessToken": accessToken } : {}),
              },
              body: JSON.stringify({
                provider: "google",
                sub: token.sub,
                email: token.email,
              }),
            });

            if (resp.ok) {
              const data = await resp.json();
              (token as any).appJwt = data.appJwt;
              (token as any).appJwtExp = data.appJwtExp;
            } else {
              (token as any).appJwt = undefined;
              (token as any).appJwtExp = undefined;
            }
          } catch {
            (token as any).appJwt = undefined;
            (token as any).appJwtExp = undefined;
          }
        }
      }

      return token;
    },

    async session({ session, token }) {
      return session;
    },
  },
});
