import { signIn } from "@lib/auth";

type SignInProps = {
  redirectTo?: string;
};

// SSR で動作するサーバーコンポーネント
export default function SignIn({ redirectTo }: SignInProps) {
  return (
    <form
      action={async () => {
        "use server";
        if (redirectTo) {
          await signIn("google", { redirectTo });
        } else {
          await signIn("google");
        }
      }}>
      <button type="submit">Google でログイン</button>
    </form>
  );
}
