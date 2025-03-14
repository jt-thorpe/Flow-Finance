import { useEffect, useState } from "react";

export const useResponsive = () => {
    const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
    const [isNavOpen, setIsNavOpen] = useState(false);

    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
            if (window.innerWidth >= 768) setIsNavOpen(false);
        };
        handleResize();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    return { isMobile, isNavOpen, setIsNavOpen };
};

export default useResponsive