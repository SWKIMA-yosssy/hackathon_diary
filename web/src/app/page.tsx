import SignIn from "@/components/SignInButton";
import SignOut from "@/components/SignoutButton";
import { auth } from "@/lib/auth";

export default async function Home() {
  const session = await auth();

  return (
    <div>
      <h1>Hello world!</h1>
      {session ? (
        <div>
          <div>{session.user?.name}</div>
          <SignOut />
        </div>
      ) : (
        <SignIn />
      )}
    </div>
  );
}
