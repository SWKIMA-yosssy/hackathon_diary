import { signOut } from "@lib/auth";

// SSR で動作するサーバーコンポーネント
export default function SignOut({ redirectTo }: { redirectTo?: string }) {
  return (
    <form
      action={async () => {
        "use server";
        await signOut({ redirectTo: redirectTo ?? "/" });
      }}>
      <button type="submit">サインアウト</button>
    </form>
  );
}
