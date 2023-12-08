import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { useToast } from "@chakra-ui/react";
const SearchResultsPage = () => {
  const location = useLocation();
  const toast = useToast();
  const getProfileInfo = async (search) => {
    try {
      //Make cal to the spotify api to get the profile
      const response = await fetch(
        `/api/spotify/get-all-users?search=${search}`,
        {
          headers: new Headers({ "content-type": "application/json" }),
          method: "GET",
        }
      );

      const data = await response.json();

      const results = await data;
      if (!response.ok) {
        throw new Error(`${data.error}`);
      }

      return results;
    } catch (error) {
      toast({
        title: "Error Occured!!",
        status: "error",
        description: error.message,
        duration: 5000,
        isClosable: true,
        position: "bottom",
      });
    }
  };
  useEffect(() => {
    const queryParameters = new URLSearchParams(location.search);
    const search = queryParameters.get("search-term");
    getProfileInfo(search);
  }, [location.search]);
  return <div>SearchResultsPage</div>;
};

export default SearchResultsPage;
