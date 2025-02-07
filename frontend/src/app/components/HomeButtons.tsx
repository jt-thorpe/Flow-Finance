import Image from "next/image";
import Link from "next/link";

const AuthButtons = () => {
    return (
        <div className="flex gap-4">
            {[
                { href: "/register", label: "Register" },
                { href: "/login", label: "Login" },
            ].map(({ href, label }) => (
                <Link
                    key={href}
                    href={href}
                    className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
                >
                    <Image
                        className="dark:invert"
                        src="/vercel.svg"
                        alt="Vercel logomark"
                        width={20}
                        height={20}
                    />
                    {label}
                </Link>
            ))}
        </div>
    );
};

export default AuthButtons;
