import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Box, Text, Flex, useToast, VStack } from "@chakra-ui/react";
import UserColumnCard from "../Components/userColumnCard";
const SearchResultsPage = () => {
  const location = useLocation();
  const toast = useToast();
  const [allUsers, setAllUsers] = useState();
  const [searchTerms, setSearchTerms] = useState();
  const [newSearch, setNewSearch] = useState(false);

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
      console.log("hi");
      setAllUsers(() => {
        return results;
      });
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
    setAllUsers(() => {
      return null;
    });
    const queryParameters = new URLSearchParams(location.search);
    const search = queryParameters.get("search-term");
    setSearchTerms(() => {
      return search.trim().split(",");
    });
    getProfileInfo(search);
  }, [location.search]);
  return (
    <Box display="flex" flexDir={"column"} minW="100%" justifyContent={"start"}>
      {allUsers && searchTerms && (
        <>
          <Flex
            basis="30%"
            margin={2}
            dir="column"
            alignSelf={{ base: "center", sm: "flex-start" }}
            bg={"#BE3144"}
            padding={2}
            boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  #F05941"
            transition={"200ms"}
            _hover={{
              boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  #F05941",
            }}
            flexWrap={"warp"}
          >
            <Box alignSelf={"center"} minW={"10%"} flexShrink={0}>
              {searchTerms.length > 1 ? (
                <Text
                  fontFamily={"Poppins"}
                  fontWeight={"500"}
                  textColor="white"
                >
                  Search Terms:
                </Text>
              ) : (
                <Text
                  fontFamily={"Poppins"}
                  fontWeight={"500"}
                  textColor="white"
                >
                  Search Term:
                </Text>
              )}
            </Box>
            {searchTerms.map((term) => (
              <Box border="2px" borderColor="white" marginLeft={3}>
                <Text
                  textColor="white"
                  padding={2}
                  fontFamily={"Poppins"}
                  fontWeight={"700"}
                >
                  {term}
                </Text>
              </Box>
            ))}
          </Flex>
          <Box
            bg={"#BE3144"}
            minW={{ base: "70%", md: "75%" }}
            alignSelf={"center"}
            textAlign={"center"}
            boxShadow="4px 4px 0 0 #22092C, 8px 8px 0 0  #F05941"
            marginY={2}
            transition={"200ms"}
            _hover={{
              boxShadow: "6px 6px 0 0 #22092C, 10px 10px 0 0  #F05941",
            }}
          >
            <Text
              fontSize={"25px"}
              position="sticky"
              fontFamily="Poppins"
              margin={"10px"}
              fontWeight={"900"}
              color={"#22092C"}
            >
              All Results{" "}
            </Text>
          </Box>
          {console.log(allUsers)}
          <Flex
            flexWrap="wrap"
            justifyContent={"space-around"}
            maxW={"75%"}
            alignSelf={"center"}
          >
            {allUsers.map((user, index) => (
              <>
                <Box basis="50%" marginX={2} marginY={2} key={index}>
                  <UserColumnCard user={user} />
                </Box>
              </>
            ))}
          </Flex>
        </>
      )}
    </Box>
  );
};

export default SearchResultsPage;
