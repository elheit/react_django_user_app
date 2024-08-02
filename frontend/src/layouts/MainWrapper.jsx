import { useEffect, useState } from "react";
// responsible to check and refresh tokens in cookies
import { setUser } from "../utils/auth";

const MainWrapper = ({ children }) => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const handler = async () => {
      await setUser();
      console.log('====> hello inside')
      setLoading(false);
    };

    handler();
  }, []);

  return <>{loading ? <p>Loading Wait ....</p> : children}</>;
};

export default MainWrapper;
