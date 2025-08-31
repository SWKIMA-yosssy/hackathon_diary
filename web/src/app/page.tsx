import SignIn from "@/components/SignInButton";
import SignOut from "@/components/SignoutButton";
import TestButtons from "@/components/TestButtons";
import { auth } from "@/lib/auth";

export default async function Home() {
  const session = await auth();

  return (
    <div>
      <h1>Hello world!</h1>
      {session ? (
        <div>
          <p>Logged in as {session.user?.name}</p>
          <p>{session.user?.email}</p>
        </div>
      ) : (
        <div>
          <p>Not logged in (anonymous access)</p>
        </div>
      )}
      <div>
        <TestButtons user={session?.user} />
        <div>{session ? <SignOut /> : <SignIn />}</div>
      </div>
    </div>
  );
}
